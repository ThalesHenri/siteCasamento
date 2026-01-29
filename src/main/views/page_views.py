#views de configuraçoes e das paginas
from django.shortcuts import render
from django.views import View

class HomeView(View):
    template_name = 'main/index.html'
    def get(self, request):
        return render(request, self.template_name)
    
    
class ListaDePresentesView(View):
    template_name = 'main/lista_de_presentes.html'
    def get(self, request):
        return render(request, self.template_name)