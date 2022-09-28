from math import prod
from django.shortcuts import render
from django.views.generic import TemplateView
from . models import *

class HomeView(TemplateView):
    template_name = 'home.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['produto_list'] = Produto.objects.all().order_by('-id')
        return context


class TodosProdutosView(TemplateView):
    template_name = 'todosprodutos.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['todascategorias'] = Categoria.objects.all()
        return context


class ProdutoDetalheView(TemplateView):
    template_name = 'produtodetalhe.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        url_slug = self.kwargs['slug']
        produto = Produto.objects.get(slug=url_slug)
        context['produto'] = produto
        return context  



class AddCarrinhoView(TemplateView):
    template_name = 'addcarrinho.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # captura o produto pelo id passado na url
        produto_id = self.kwargs['produto_id']
        # atribui o id do banco ao id da url
        produto_obj = Produto.objects.get(id=produto_id)
        # se o produto que foi capturado na url, já estiver na sessão do carrinho ele adciona, senão ele vai criar o carrinho 
        carrinho_id = self.request.session.get('carrinho_id', None)
        #se existir o carrinho, senão vai criar o carrinho
        if carrinho_id:
            carrinho_obj = Carro.objects.get(id=carrinho_id) 
        else:
            carrinho_obj = Carro.objects.create(total=0)
            #adciona o produto a sessão do carrinho, se ele não estiver criado
            self.request.session['carrinho_id'] = carrinho_obj.id


class SobreView(TemplateView):
    template_name = 'sobre.html'


class ContatoView(TemplateView):
    template_name = 'contato.html'




    