from multiprocessing import context
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View, CreateView, FormView, DetailView, ListView
from django.urls import reverse_lazy
from . forms import Checar_PedidoForm, ClienteRegistrarForm, ClienteEntrarForm
from . models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.core.paginator import Paginator


class LojaMixin(object):
    def dispatch(self, request, *args, **kwargs):
        carro_id = request.session.get('carro_id')
        if carro_id:
            carro_obj = Carro.objects.get(id=carro_id)
            if request.user.is_authenticated and request.user.cliente:
                carro_obj.cliente = request.user.cliente
                carro_obj.save()
        return super().dispatch(request, *args, **kwargs)


class HomeView(LojaMixin, TemplateView):
    template_name = 'home.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #context['produto_list'] = Produto.objects.all().order_by('-id')
        all_produtos = Produto.objects.all().order_by('-id')
        paginator = Paginator(all_produtos, 4)
        page_number = self.request.GET.get('page')
        produto_list = paginator.get_page(page_number)
        context['produto_list'] = produto_list
        return context


class TodosProdutosView(LojaMixin, TemplateView):
    template_name = 'todosprodutos.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['todascategorias'] = Categoria.objects.all()
        return context


class ProdutoDetalheView(LojaMixin, TemplateView):
    template_name = 'produtodetalhe.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        url_slug = self.kwargs['slug']
        produto = Produto.objects.get(slug=url_slug)
        context['produto'] = produto
        return context  



class AddCarrinhoView(LojaMixin, TemplateView):
    template_name = 'addcarrinho.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # captura o produto pelo id passado na url
        produto_id = self.kwargs['produto_id']
        # atribui o id do banco ao id da url
        produto_obj = Produto.objects.get(id=produto_id)
        # se o produto que foi capturado na url, j?? estiver na sess??o do carrinho ele adciona, sen??o ele vai criar o carrinho 
        carrinho_id = self.request.session.get('carrinho_id', None)
        #se existir o carrinho, sen??o vai criar o carrinho
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
            #adciona o produto a sess??o do carrinho, se ele n??o estiver criado
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


class ManipularCarrinhoView(LojaMixin, View):
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


class LimparCarrinhoView(LojaMixin, View):
    def get(self, request, *args, **kwargs):
        carrinho_id = request.session.get('carrinho_id', None)
        if carrinho_id:
            carro = Carro.objects.get(id=carrinho_id)
            carro.carroproduto_set.all().delete()
            carro.total = 0
            carro.save()
        return redirect('lojaapp:meucarrinho')



class MeuCarrinhoView(LojaMixin, TemplateView):
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



class CheckOutView(LojaMixin, CreateView):
    template_name = 'processar.html'
    form_class = Checar_PedidoForm
    success_url = reverse_lazy('lojaapp:home')


    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.cliente:
            pass
        else:
            return redirect('/entrar/?next=/checkout/')
        return super().dispatch(request, *args, **kwargs)


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



class PagamentoView(View):
   
   def get(self, request, *args, **kwargs):
    context = {

    }
    return render(request, 'pagamento.html', context)



class ClienteRegistrarView(CreateView):
    template_name = 'registrarcliente.html'
    form_class = ClienteRegistrarForm
    success_url = reverse_lazy('lojaapp:home')

    #valida o formul??rio, limpa e armazena os dados requisitados na vari??vel user
    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        email = form.cleaned_data.get('email')
        user = User.objects.create_user(username, email, password)
        #instancia o usuario do formul??rio passando a vari??vel user que foi criada por n??s
        form.instance.user = user 
        login(self.request, user)
        return super().form_valid(form)


    def get_success_url(self):
        if 'next' in self.request.GET:
            next_url = self.request.GET.get('next')
            return next_url
        else:
            return self.success_url


# class ClienteSairView(View):
#     def pegar(self, request):
#         logout(request)
#         return redirect('lojaapp:home')
    

def usuario_logout(request):
    logout(request)
    return redirect('lojaapp:home')


class ClienteEntrarView(FormView):
    template_name = 'clienteentrar.html'
    form_class = ClienteEntrarForm
    success_url = reverse_lazy('lojaapp:home')

    def form_valid(self, form):
        unome = form.cleaned_data.get('username')
        pword = form.cleaned_data.get('password')
        usr = authenticate(username=unome, password=pword)
        if usr is not None and Cliente.objects.filter(user=usr).exists():
            login(self.request, usr)
        else:
            return render(self.request, self.template_name, {"form": self.form_class, "error": "Usu??rio ou senha n??o correspondem"})
        return super().form_valid(form)


    def get_success_url(self):
        if 'next' in self.request.GET:
            next_url = self.request.GET.get('next')
            return next_url
        else:
            return self.success_url


class SobreView(LojaMixin, TemplateView):
    template_name = 'sobre.html'


class ContatoView(LojaMixin, TemplateView):
    template_name = 'contato.html'




class ClientePerfilView(TemplateView):
    template_name = "clienteperfil.html"
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and Cliente.objects.filter(user=request.user).exists():
            pass
        else:
            return redirect('/entrar/?next=/perfil/')
        return super().dispatch(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        cliente = self.request.user.cliente
        context['cliente'] = cliente

        pedidos = Pedido_order.objects.filter(carro__cliente=cliente).order_by("-id")
        # pedidos = Pedido_order.objects.all()
        context['pedidos'] = pedidos

        return context




class ClientePedidoDetalhe(DetailView):
    template_name = 'clientepedidodetalhe.html'
    model = Pedido_order
    context_object_name = 'pedido_obj'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and Cliente.objects.filter(user=request.user).exists():
            order_id = self.kwargs["pk"]
            pedido = Pedido_order.objects.get(id=order_id)
            if request.user.cliente != pedido.carro.cliente:
                return redirect('lojaapp:clienteperfil')
        else:
            return redirect('/entrar/?next=/perfil/')
        return super().dispatch(request, *args, **kwargs)


#classe do administrador


class AdminLoginView(FormView):
    template_name = 'admin_paginas/adminlogin.html'
    form_class = ClienteEntrarForm
    success_url = reverse_lazy('lojaapp:adminhome')

    def form_valid(self, form):
        unome = form.cleaned_data.get('username')
        pword = form.cleaned_data.get('password')
        usr = authenticate(username=unome, password=pword)
        if usr is not None and Admin.objects.filter(user=usr).exists():
            login(self.request, usr)
        else:
            return render(self.request, self.template_name, {"form": self.form_class, "error": "Usu??rio ou senha n??o correspondem"})
        return super().form_valid(form)


class AdminRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and Admin.objects.filter(user=request.user).exists():
            pass
        else:
            return redirect('/admin-login/')
        return super().dispatch(request, *args, **kwargs)



class AdminHomeView(AdminRequiredMixin, TemplateView):
    template_name = 'admin_paginas/adminhome.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['PedidosPendentes'] = Pedido_order.objects.filter(pedido_status='Pedido Recebido').order_by("-id")
        return context


class AdminPedidoDetaheView(AdminRequiredMixin, DetailView):
    template_name = 'admin_paginas/adminpedidodetahe.html'
    model = Pedido_order
    context_object_name = 'pedido_obj'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['todosstatus'] = PEDIDO_STATUS
        
        return context

    

 
class AdminPedidoListaView(AdminRequiredMixin, ListView):
    template_name = 'admin_paginas/adminpedidolista.html'
    queryset = Pedido_order.objects.all().order_by("-id")
    context_object_name = 'todospedido'      


 
class AdminPedidoMudarStatusView(AdminRequiredMixin, View):
     
    def post(self, request, *args, **kwargs):
        pedido_id = self.kwargs["pk"]
        pedido_obj = Pedido_order.objects.get(id=pedido_id)
        novo_status = request.POST.get('status')
        pedido_obj.pedido_status = novo_status
        pedido_obj.save()

        return redirect(reverse_lazy('lojaapp:adminpedidodetalhe', kwargs={"pk" : self.kwargs["pk"]}))


class PesquisarView(TemplateView):
    template_name = 'pesquisar.html'
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        kw = self.request.GET.get('keyword')
        result = Produto.objects.filter(
            Q(titulo__icontains=kw) | Q(descricao__icontains=kw) | Q(return_devolucao__icontains=kw))
        context['result'] = result
        return context

