import mercadopago
from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from ..models.presente_model import Presente
from ..models.pedido_model import Pedido
from ..models.pedido_item_model import PedidoItem

@login_required(login_url='login')
def gerar_pix(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id, convidado=request.user)
    # Certifique-se de que as linhas abaixo tenham 4 espaços de recuo
    total = sum(
        (item.valor or Decimal("0.00")) * (item.quantidade or 0)
        for item in pedido.items.all()
    )
    return render(request, 'main/qr_code.html', {
        'pedido': pedido,
        'total': total
    })
@method_decorator(login_required(login_url='login'), name='dispatch')
class AddToCartView(View):
    def post(self, request, presente_id):
        presente = get_object_or_404(Presente, id=presente_id)
        if 'carrinho' not in request.session:
            request.session['carrinho'] = {}
        carrinho = request.session['carrinho']
        id_str = str(presente_id)
        if id_str in carrinho:
            carrinho[id_str]['quantidade'] += 1
        else:
            carrinho[id_str] = {'nome': presente.nome, 'preco': str(presente.preco), 'quantidade': 1}
        request.session.modified = True
        messages.success(request, f'{presente.nome} adicionado!')
        return redirect('lista_de_presentes')

@method_decorator(login_required(login_url='login'), name='dispatch')
class CarrinhoView(View):
    def get(self, request):
        carrinho = request.session.get('carrinho', {})
        itens, total = [], Decimal('0')
        for k, v in carrinho.items():
            subtotal = Decimal(v['preco']) * v['quantidade']
            total += subtotal
            itens.append({'id': k, 'quantidade': v['quantidade'], 'preco': v['preco'], 'subtotal': subtotal})
        return render(request, 'main/carrinho.html', {'itens': itens, 'total': total})

    def post(self, request):
        carrinho = request.session.get('carrinho', {})
        if not carrinho: return redirect('carrinho')
        pedido = Pedido.objects.create(convidado=request.user)
        for k, v in carrinho.items():
            PedidoItem.objects.create(pedido=pedido, presente_id=int(k), quantidade=v['quantidade'], valor=Decimal(v['preco']))
        request.session['carrinho'] = {}
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
    def get(self, request, pedido_id):
        pedido = get_object_or_404(Pedido, id=pedido_id, convidado=request.user)
        itens = pedido.items.all()
        total = sum(i.valor * i.quantidade for i in itens)
        return render(request, 'main/pedido_confirmacao.html', {'pedido': pedido, 'itens': itens, 'total': total})

class PagamentoView(View):
    def __init__(self):
        self.sdk = mercadopago.SDK("APP_USR-3855686192526448-031011-1bd32502cd9e0ea24ff3ea2f18db2a04-3257118066")

    def get(self, request, pedido_id):
        pedido = get_object_or_404(Pedido, id=pedido_id, convidado=request.user)
        total = sum(i.valor * i.quantidade for i in pedido.items.all())
        pref = {
            "items": [{"title": "Presente", "quantity": 1, "unit_price": float(total), "currency_id": "BRL"}],
            "back_urls": {"success": f"http://127.0.0.1:8000/pedido/confirmacao/{pedido.id}"}
        }
        res = self.sdk.preference().create(pref)
        return redirect(res["response"]["init_point"])