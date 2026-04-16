# views de configurações e das páginas
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from ..models.presente_model import Presente

class HomeView(View):
    template_name = 'main/index.html'

    def get(self, request):
        # passamos flag de presença para exibição na landing page
        status = None
        if request.user.is_authenticated:
            status = request.user.presenca_confirmada
        confirmada = request.GET.get('confirmada')
        return render(request, self.template_name, {"presenca_confirmada": status, "confirmada": confirmada})
    

class ListaDePresentesView(View):
    template_name = 'main/lista_de_presentes.html'

    def get(self, request):
        # buscar todos os presentes cadastrados
        presentes = Presente.objects.all()
        return render(request, self.template_name, {"presentes": presentes})


class StoryView(View):
    template_name = 'main/story.html'

    def get(self, request):
        # exemplo de história simples; poderia ser carregada de modelo ou JSON
        historia = (
            "A história de Ailka e Vinícius começou em 2019 e, curiosamente, não foi amor à primeira vista - "
            "pelo menos não da parte de Ailka, rs. Muito pelo contrário. No primeiro contato, Ailka fazia muitas "
            "perguntas, enquanto Vinícius, extremamente tímido, respondia apenas com \"sim\" ou \"não\". E a impressão "
            "inicial dela? De que ele era um pouco antipático.\n\n"
            "Naquele período, Vinícius estava focado na preparação para a EsPCEx, e os dois não chegaram a se aproximar. "
            "Algum tempo depois, quando ele retornou e começou a fazer cursinho, decidiu convidá-la para sair. Combinaram "
            "um almoço no Subway, em uma terça-feira, já que Ailka teria aula à tarde e precisaria voltar para a escola. "
            "Porém, na segunda-feira anterior ao encontro, veio o anúncio da pandemia - e, com isso, os planos foram "
            "cancelados e o contato interrompido novamente.\n\n"
            "Eles passaram quase um ano sem se ver e se falar.\n\n"
            "Por volta de setembro de 2020, os caminhos dos dois se cruzaram mais uma vez. Vinícius já havia sido aprovado "
            "novamente e vivia aquele momento entre a conquista e a mudança para Campinas. Foi então que, de forma inesperada, "
            "o famoso jogo Among Us entrou na história.\n\n"
            "Os dois participavam do mesmo grupo de WhatsApp, que se reunia todas as noites para jogar e, entre uma partida e "
            "outra, voltaram a conversar. Com o passar das semanas, o jogo se tornou apenas um pretexto para conversas que "
            "pareciam não ter fim.\n\n"
            "O que começou como uma simples partida acabou se transformando no início de uma grande história de amor.\n\n"
            "Desde então, Ailka e Vinícius não se desgrudaram mais. Nem mesmo os quase cinco anos de relacionamento à distância "
            "- com ele vivendo intensamente a rotina da formação militar na AMAN - foram capazes de afastá-los. No fundo, ambos "
            "sempre souberam que era para ser.\n\n"
            "Cada despedida, cada reencontro, cada viagem, cada abraço apertado, cada lágrima e cada oração fizeram parte dessa "
            "caminhada. E, em todos esses momentos, tiveram a certeza de que Deus os sustentava.\n\n"
            "Hoje, vivem a realização de um sonho.\n\n"
            "Ao longo desses cinco anos, Ailka e Vinícius enfrentaram desafios, mas também experimentaram inúmeras respostas de "
            "oração. E, se você está aqui, é porque, de alguma forma, fez parte dessa história.\n\n"
            "Eles agradecem profundamente por todo apoio, carinho e presença. Agora, convidam você a celebrar esse sonho junto com "
            "eles ❤️"
        )
        return render(request, self.template_name, {"historia": historia})


# confirmação de presença
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@method_decorator(login_required(login_url='login'), name='dispatch')
class ConfirmarPresencaView(View):
    template_name = 'main/confirmar_presenca.html'

    def get(self, request):
        return render(request, self.template_name, {"presenca_confirmada": request.user.presenca_confirmada})

    def post(self, request):
        usuario = request.user
        usuario.presenca_confirmada = True
        usuario.save()
        messages.success(request, 'Presença confirmada com sucesso!')
        return redirect(f"{reverse('home')}?confirmada=1")

