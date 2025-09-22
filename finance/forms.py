from django.db import models
from .models import Item
from django import forms

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['valor', 'data_transacao', 'recorrente', 'descricao', 'tipo']
        widgets = {
            'data_transacao': forms.DateInput(attrs={'type': 'date'}),
            'recorrente': forms.CheckboxInput(),
            'descricao': forms.Textarea(attrs={'rows': 3}),
            'tipo': forms.Select(choices=Item.TIPO_CHOICES),
        }
        labels = {
            'valor': 'Valor',
            'data_transacao': 'Data da Transação',
            'recorrente': 'Recorrente',
            'descricao': 'Descrição',
            'tipo': 'Tipo',
        }
        help_texts = {
            'valor': 'Insira o valor da transação.',
            'data_transacao': 'Selecione a data da transação.',
            'recorrente': 'Marque se a transação é recorrente.',
            'descricao': 'Adicione uma descrição para a transação.',
            'tipo': 'Selecione o tipo de transação.',
        }