from django.urls import path
from .views import *

app_name = 'lojaapp'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('sobre/', SobreView.as_view(), name='sobre'),
    path('contato/', ContatoView.as_view(), name='contato'),
    path('todos-produtos/', TodosProdutosView.as_view(), name='todos-produtos'),
    path('produto/<slug:slug>', ProdutoDetalheView.as_view(), name='produto-detalhe'),
    
]