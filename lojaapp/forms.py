from tkinter import Widget
from django import forms
from . models import Pedido_order
from django.forms import ModelForm, TextInput, EmailInput

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
            'email': TextInput(attrs={
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