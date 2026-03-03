# views de configurações e das páginas
from django.shortcuts import render, redirect
from django.views import View

from ..models.presente_model import Presente

class HomeView(View):
    template_name = 'main/index.html'

    def get(self, request):
        # passamos flag de presença para exibição na landing page
        status = None
        if request.user.is_authenticated:
            status = request.user.presenca_confirmada
        return render(request, self.template_name, {"presenca_confirmada": status})
    

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
        historia = ("Ailka e Vínicius se conheceram em uma viagem ao litoral em 2020. "
                    "Desde então, compartilharam muitas aventuras, risos e desafios. "
                    "Este site celebra a jornada deles e convida você a fazer parte desse dia especial.")
        return render(request, self.template_name, {"historia": historia})


# confirmação de presença
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@method_decorator(login_required(login_url='login'), name='dispatch')
class ConfirmarPresencaView(View):
    template_name = 'main/confirmar_presenca.html'

    def get(self, request):
        return render(request, self.template_name, {"confirmado": request.user.presenca_confirmada})

    def post(self, request):
        usuario = request.user
        usuario.presenca_confirmada = True
        usuario.save()
        messages.success(request, 'Presença confirmada com sucesso!')
        return redirect('home')

