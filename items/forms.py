from django.db import models
from .models import Item_aluguel
from django import forms

class aluguelForm (forms.ModelForm):
    class Meta:
        model = Item_aluguel
        fields = ['nome', 'quantidade_total', 'diaria' ]
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Cadeira de Ferro'}),
            'quantidade_total': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'diaria': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Ex: 50.00'}),
        }
        labels = {
            'nome': 'Nome do Item',
            'quantidade_total': 'Quantidade Disponível',
            'diaria': 'Valor de Aluguel por Dia (R$)',
        }