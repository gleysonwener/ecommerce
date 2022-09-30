from math import prod
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View
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
            produto_no_carro = carrinho_obj.carroproduto_set.filter(produto=produto_obj)
            if produto_no_carro.exists():
                carroproduto = produto_no_carro.last()
                carroproduto.quantidade += 1
                carroproduto.subtotal += produto_obj.venda
                carroproduto.save()
                carrinho_obj.total += produto_obj.venda
                carrinho_obj.save()

            else:
                carroproduto = CarroProduto.objects.create(
                    carro = carrinho_obj,
                    produto = produto_obj,
                    avaliacao = produto_obj.venda,
                    quantidade = 1,
                    subtotal = produto_obj.venda,
                )
                carrinho_obj.total += produto_obj.venda
                carrinho_obj.save()

        else:
            carrinho_obj = Carro.objects.create(total=0)
            #adciona o produto a sessão do carrinho, se ele não estiver criado
            self.request.session['carrinho_id'] = carrinho_obj.id
            carroproduto = CarroProduto.objects.create(
                    carro = carrinho_obj,
                    produto = produto_obj,
                    avaliacao = produto_obj.venda,
                    quantidade = 1,
                    subtotal = produto_obj.venda,
                )
            carrinho_obj.total += produto_obj.venda
            carrinho_obj.save()

        return context


class ManipularCarrinhoView(View):
    def get(self, request, *args, **kwargs):
        cp_id = self.kwargs['cp_id']
        acao = request.GET.get('acao')
        cp_obj = CarroProduto.objects.get(id=cp_id)
        carro_obj = cp_obj.carro
      
        if acao == 'inc':
            cp_obj.quantidade += 1
            cp_obj.subtotal += cp_obj.avaliacao
            cp_obj.save()
            carro_obj.total += cp_obj.avaliacao
            carro_obj.save()

        elif acao == 'dcr':
            pass
        elif acao == 'rmv':
            pass
        else:
            pass
        return redirect('lojaapp:meucarrinho')



class MeuCarrinhoView(TemplateView):
    template_name = 'meucarrinho.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        carrinho_id = self.request.session.get('carrinho_id', None)
        if carrinho_id:
            carrinho = Carro.objects.get(id=carrinho_id) 
        else:
            carrinho = None
        context['carrinho'] = carrinho
        return context


class SobreView(TemplateView):
    template_name = 'sobre.html'


class ContatoView(TemplateView):
    template_name = 'contato.html'




    