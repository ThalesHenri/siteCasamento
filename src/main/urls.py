from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    HomeView, StoryView, ListaDePresentesView, ConfirmarPresencaView,
    RegisterView, LoginView, LogoutView,
    AddToCartView, CarrinhoView, RemoveFromCartView, PedidoConfirmacaoView
)


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('nosso-amor/', StoryView.as_view(), name='story'),
    path('lista_de_presentes/', ListaDePresentesView.as_view(), name='lista_de_presentes'),
    path('confirmar_presenca/', ConfirmarPresencaView.as_view(), name='confirmar_presenca'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    
    # Cart routes
    path('carrinho/adicionar/<int:presente_id>/', AddToCartView.as_view(), name='adicionar_carrinho'),
    path('carrinho/', CarrinhoView.as_view(), name='carrinho'),
    path('carrinho/remover/<int:presente_id>/', RemoveFromCartView.as_view(), name='remover_carrinho'),
    path('pedido/confirmacao/<int:pedido_id>/', PedidoConfirmacaoView.as_view(), name='pedido_confirmacao'),
]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)