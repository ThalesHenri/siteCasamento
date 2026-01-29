from django.urls import path
from .views import HomeView, ListaDePresentesView


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('lista_de_presentes/', ListaDePresentesView.as_view(), name='lista_de_presentes'),
]