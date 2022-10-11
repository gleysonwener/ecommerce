from tkinter import Widget
from django import forms
from . models import Pedido_order, Cliente
from django.forms import ModelForm, PasswordInput, TextInput, EmailInput
from django.contrib.auth.models import User

class Checar_PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido_order
        fields = ['ordenado_por', 'telefone', 'email', 'endereco_envio']
        # widgets = {
        #     'ordenado_por': TextInput(attrs={
        #         'class': 'form-control',
        #         'style': 'max-with: 300px',
        #         'placeholder': 'ordenado por',
        #     }),
        #     'telefone': TextInput(attrs={
        #         'class': 'form-control',
        #         'style': 'max-with: 300px',
        #         'placeholder': 'telefone',
        #     }),
        #     'email': EmailInput(attrs={
        #         'class': 'form-control',
        #         'style': 'max-with: 300px',
        #         'placeholder': 'email',
        #     }),
        #     'endereco_envio': TextInput(attrs={
        #         'class': 'form-control',
        #         'style': 'max-with: 300px',
        #         'placeholder': 'endereco para envio',
        #     }),

        # }


class ClienteRegistrarForm(forms.ModelForm):
    # usuario = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'usuario', 'class': 'form-control', 'style': 'with: 300px; display: flex; '}))
    # senha = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'senha', 'class': 'form-control', 'style': 'with: 300px; display: flex; '}))
    # email = forms.CharField(widget=forms.EmailInput(attrs={'placeholder': 'email', 'class': 'form-control', 'style': 'with: 300px; display: flex; '}) )

    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())
    email = forms.CharField(widget=forms.EmailInput())
    
    class Meta:
        model = Cliente
        fields = ['username', 'password', 'email', 'nome_completo', 'endereco']
        # widgets = {
            
        #     'nome_completo': TextInput(attrs={
        #         'class': 'form-control',
        #         'style': 'max-with: 300px',
        #         'placeholder': 'nome_completo',
        #     }),
        #     'endereco': TextInput(attrs={
        #         'class': 'form-control',
        #         'style': 'max-with: 300px',
        #         'placeholder': 'endereco',
        #     }),
        # }


    def clean_username(self):
        unome = self.cleaned_data.get('username')
        if User.objects.filter(username=unome).exists():
            raise forms.ValidationError('Este cliente já existe no banco de dados.')
        return unome


class ClienteEntrarForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())