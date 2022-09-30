import email
from math import prod
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View, CreateView
from django.urls import reverse_lazy
from . forms import Checar_Pedido_Form, CadastrarClienteForm
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
            cp_obj.quantidade -= 1
            cp_obj.subtotal -= cp_obj.avaliacao
            cp_obj.save()
            carro_obj.total -= cp_obj.avaliacao
            carro_obj.save()
            if cp_obj.quantidade == 0:
                cp_obj.delete()

        elif acao == 'rmv':
            carro_obj.total -= cp_obj.subtotal
            carro_obj.save()
            cp_obj.delete()
            
        else:
            pass
        return redirect('lojaapp:meucarrinho')


class LimparCarrinhoView(View):
    def get(self, request, *args, **kwargs):
        carrinho_id = request.session.get('carrinho_id', None)
        if carrinho_id:
            carro = Carro.objects.get(id=carrinho_id)
            carro.carroproduto_set.all().delete()
            carro.total = 0
            carro.save()
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



class CheckOutView(CreateView):
    template_name = 'processar.html'
    form_class = Checar_Pedido_Form
    success_url = reverse_lazy('lojaapp:home')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        carrinho_id = self.request.session.get('carrinho_id', None)
        if carrinho_id:
            carrinho = Carro.objects.get(id=carrinho_id) 
        else:
            carrinho = None
        context['carrinho'] = carrinho
        return context


    def form_valid(self, form):
        carro_id = self.request.session.get('carrinho_id')
        if carro_id:
            carro_obj = Carro.objects.get(id=carro_id)
            form.instance.carro = carro_obj
            form.instance.subtotal = carro_obj.total
            form.instance.desconto = 0
            form.instance.total = carro_obj.total
            form.instance.pedido_status = "Pedido Recebido"
            del self.request.session['carrinho_id']
        else:
            return redirect('lojaapp:home')
        return super().form_valid(form)



class RegistrarClienteView(CreateView):
    template_name = 'registrarcliente.html'
    form_class = CadastrarClienteForm
    success_url = reverse_lazy('lojaapp:home')

    #valida o formulário, limpa e armazena os dados requisitados na variável user
    def form_valid(self, form):
        usuario = form.cleaned_data.get('usuario')
        senha = form.cleaned_data.get('senha')
        email = form.cleaned_data.get('email')
        user = User.objects.create_user(usuario, senha, email)
        #instancia o usuario do formulário passando a variável user que foi criada por nós
        form.instance.user = user 
        return super().form_valid(form)



class SobreView(TemplateView):
    template_name = 'sobre.html'


class ContatoView(TemplateView):
    template_name = 'contato.html'




    