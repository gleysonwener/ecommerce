from django.urls import path
from .views import *

app_name = 'lojaapp'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('sobre/', SobreView.as_view(), name='sobre'),
    path('contato/', ContatoView.as_view(), name='contato'),
    path('todos-produtos/', TodosProdutosView.as_view(), name='todos-produtos'),
    path('produto/<slug:slug>', ProdutoDetalheView.as_view(), name='produto-detalhe'),
    path('addcarrinho-<int:produto_id>/', AddCarrinhoView.as_view(), name='addcarrinho'),
    path('meucarrinho/', MeuCarrinhoView.as_view(), name='meucarrinho'),
    path('manipular-carrinho/<int:cp_id>/', ManipularCarrinhoView.as_view(), name='manipular-carrinho'),
    path('limpar-carrinho/', LimparCarrinhoView.as_view(), name='limparcarrinho'),
    path('checkout/', CheckOutView.as_view(), name='checkout'),
    path('registrar-cliente/', ClienteRegistrarView.as_view(), name='registrarcliente'),
    path('sair/', usuario_logout, name='clientesair'),
    path('entrar/', ClienteEntrarView.as_view(), name='clienteentrar'),
    path('perfil/', ClientePerfilView.as_view(), name='clienteperfil'),
    path('perfil/pedido-<int:pk>/', ClientePedidoDetalhe.as_view(), name='clientepedidodetalhe'),
    path('admin-login/', AdminLoginView.as_view(), name='adminlogin'),
    path('admin-home/', AdminHomeView.as_view(), name='adminhome'),
    path('admin-pedido/<int:pk>/', AdminPedidoDetaheView.as_view(), name='adminpedidodetalhe'),    
    path('admin-todos-pedidos/', AdminPedidoListaView.as_view(), name='adminpedidolista'),    
    path('admin-pedido-<int:pk>-mudar/', AdminPedidoMudarStatusView.as_view(), name='adminpedidomudarstatus'),
]   