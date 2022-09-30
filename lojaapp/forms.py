from tkinter import Widget
from django import forms
from . models import Pedido_order, Cliente
from django.forms import ModelForm, PasswordInput, TextInput, EmailInput

class Checar_Pedido_Form(forms.ModelForm):
    class Meta:
        model = Pedido_order
        fields = ('ordenado_por', 'telefone', 'email', 'endereco_envio',)
        widgets = {
            'ordenado_por': TextInput(attrs={
                'class': 'form-control',
                'style': 'max-with: 300px',
                'placeholder': 'ordenado por',
            }),
            'telefone': TextInput(attrs={
                'class': 'form-control',
                'style': 'max-with: 300px',
                'placeholder': 'telefone',
            }),
            'email': EmailInput(attrs={
                'class': 'form-control',
                'style': 'max-with: 300px',
                'placeholder': 'email',
            }),
            'endereco_envio': TextInput(attrs={
                'class': 'form-control',
                'style': 'max-with: 300px',
                'placeholder': 'endereco para envio',
            }),

        }


class CadastrarClienteForm(forms.ModelForm):
    usuario = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'usuario', 'class': 'form-control', 'style': 'with: 300px; display: flex; '}))
    senha = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'senha', 'class': 'form-control', 'style': 'with: 300px; display: flex; '}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'placeholder': 'email', 'class': 'form-control', 'style': 'with: 300px; display: flex; '}) )

    class Meta:
        model = Cliente
        fields = ('usuario', 'senha', 'email', 'nome_completo', 'endereco',)
        widgets = {
            
            'nome_completo': TextInput(attrs={
                'class': 'form-control',
                'style': 'max-with: 300px',
                'placeholder': 'nome_completo',
            }),
            'endereco': TextInput(attrs={
                'class': 'form-control',
                'style': 'max-with: 300px',
                'placeholder': 'endereco',
            }),
        }





     