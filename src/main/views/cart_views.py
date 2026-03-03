from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from decimal import Decimal

from ..models.presente_model import Presente
from ..models.pedido_model import Pedido
from ..models.pedido_item_model import PedidoItem


@method_decorator(login_required(login_url='login'), name='dispatch')
class AddToCartView(View):
    def post(self, request, presente_id):
        try:
            presente = Presente.objects.get(id=presente_id)
        except Presente.DoesNotExist:
            messages.error(request, 'Presente não encontrado.')
            return redirect('lista_de_presentes')

        # Inicializar o carrinho na sessão se não existir
        if 'carrinho' not in request.session:
            request.session['carrinho'] = {}

        carrinho = request.session['carrinho']
        presente_id_str = str(presente_id)

        # Se o item já está no carrinho, aumentar quantidade
        if presente_id_str in carrinho:
            carrinho[presente_id_str]['quantidade'] += 1
        else:
            # Adicionar novo item ao carrinho
            carrinho[presente_id_str] = {
                'nome': presente.nome,
                'preco': str(presente.preco),
                'quantidade': 1,
            }

        request.session.modified = True
        messages.success(request, f'{presente.nome} adicionado ao carrinho!')
        return redirect('lista_de_presentes')


@method_decorator(login_required(login_url='login'), name='dispatch')
class CarrinhoView(View):
    template_name = 'main/carrinho.html'

    def get(self, request):
        carrinho = request.session.get('carrinho', {})
        itens = []
        total = Decimal('0')
        
        # Criar lista de chaves para remover (evita modificar dict enquanto itera)
        chaves_para_remover = []

        for presente_id_str, item in carrinho.items():
            try:
                presente = Presente.objects.get(id=int(presente_id_str))
                quantidade = item['quantidade']
                subtotal = Decimal(str(item['preco'])) * Decimal(str(quantidade))
                total += subtotal
                
                itens.append({
                    'id': presente_id_str,
                    'present': presente,
                    'quantidade': quantidade,
                    'preco': Decimal(str(item['preco'])),
                    'subtotal': subtotal,
                })
            except (Presente.DoesNotExist, ValueError, TypeError, KeyError):
                # Marcar item para remoção
                chaves_para_remover.append(presente_id_str)

        # Remover itens inválidos após iteração
        for chave in chaves_para_remover:
            if chave in carrinho:
                del carrinho[chave]
        
        if chaves_para_remover:
            request.session.modified = True

        return render(request, self.template_name, {
            'itens': itens,
            'total': total,
            'carrinho_vazio': len(itens) == 0,
        })

    def post(self, request):
        # Criar pedido a partir do carrinho
        carrinho = request.session.get('carrinho', {})

        if not carrinho:
            messages.error(request, 'Seu carrinho está vazio.')
            return redirect('carrinho')

        # Criar novo pedido
        pedido = Pedido.objects.create(convidado=request.user)

        # Adicionar itens ao pedido
        items_added = 0
        for presente_id_str, item in carrinho.items():
            try:
                # Converter string id para integer
                presente = Presente.objects.get(id=int(presente_id_str))
                quantidade = item.get('quantidade', 1)
                valor = Decimal(str(item.get('preco', '0')))

                if quantidade > 0 and valor > 0:
                    PedidoItem.objects.create(
                        pedido=pedido,
                        presente=presente,
                        quantidade=quantidade,
                        valor=valor,
                    )
                    items_added += 1
            except (Presente.DoesNotExist, ValueError, TypeError):
                # Ignorar items inválidos
                pass

        # Se nenhum item foi adicionado, deletar o pedido vazio
        if items_added == 0:
            pedido.delete()
            messages.error(request, 'Nenhum item foi adicionado. Carrinho inválido.')
            return redirect('carrinho')

        # Limpar o carrinho
        request.session['carrinho'] = {}
        request.session.modified = True

        messages.success(request, 'Pedido criado com sucesso!')
        return redirect('pedido_confirmacao', pedido_id=pedido.id)


@method_decorator(login_required(login_url='login'), name='dispatch')
class RemoveFromCartView(View):
    def post(self, request, presente_id):
        carrinho = request.session.get('carrinho', {})
        presente_id_str = str(presente_id)

        if presente_id_str in carrinho:
            try:
                presente = Presente.objects.get(id=presente_id)
                del carrinho[presente_id_str]
                request.session.modified = True
                messages.success(request, f'{presente.nome} removido do carrinho.')
            except Presente.DoesNotExist:
                messages.error(request, 'Presente não encontrado.')
        else:
            messages.error(request, 'Item não está no carrinho.')

        return redirect('carrinho')


@method_decorator(login_required(login_url='login'), name='dispatch')
class PedidoConfirmacaoView(View):
    template_name = 'main/pedido_confirmacao.html'

    def get(self, request, pedido_id):
        try:
            pedido = Pedido.objects.get(id=pedido_id, convidado=request.user)
        except Pedido.DoesNotExist:
            messages.error(request, 'Pedido não encontrado.')
            return redirect('home')

        itens = list(pedido.items.all())
        
        # Verificar se o pedido tem itens
        if not itens:
            messages.error(request, 'Pedido vazio. Por favor, tente novamente.')
            pedido.delete()
            return redirect('carrinho')
        
        # Calcular total de forma segura
        total = Decimal('0')
        for item in itens:
            try:
                subtotal = Decimal(str(item.valor)) * Decimal(str(item.quantidade))
                total += subtotal
            except (ValueError, TypeError):
                subtotal = Decimal('0')

        return render(request, self.template_name, {
            'pedido': pedido,
            'itens': itens,
            'total': total,
        })

