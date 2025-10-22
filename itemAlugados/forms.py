# items_alugados/forms.py
from django import forms
from django.forms import inlineformset_factory, BaseInlineFormSet
from .models import Aluguel, ItemAlugado
from clients.models import Cliente
from items.models import Item_aluguel


class AluguelForm(forms.ModelForm):
    class Meta:
        model = Aluguel
        fields = ['cliente', 'data_inicio', 'data_fim']
        widgets = {
            'data_inicio': forms.DateInput(attrs={'type': 'date'}),
            'data_fim': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        usuario = kwargs.pop('usuario', None)
        super().__init__(*args, **kwargs)
        if usuario:
            self.fields['cliente'].queryset = Cliente.objects.filter(usuario=usuario)
        self.fields['cliente'].label = "Cliente"
        self.fields['data_inicio'].label = "Data de início"
        self.fields['data_fim'].label = "Data de devolução"


class ItemAlugadoForm(forms.ModelForm):
    # Adicionamos 'valor_diaria' como campo HiddenInput. 
    # Isso garante que ele seja renderizado no template para o JS ler.
    
    class Meta:
        model = ItemAlugado
        # Incluímos 'valor_diaria' na lista de fields
        fields = ['item', 'quantidade']
        widgets = {
            'quantidade': forms.NumberInput(attrs={'min': 1}),
        }

    def __init__(self, *args, **kwargs):
        usuario = kwargs.pop('usuario', None)
        super().__init__(*args, **kwargs)
        if usuario:
            self.fields['item'].queryset = Item_aluguel.objects.filter(usuario=usuario)
        self.fields['item'].label = "Item a ser alugado"
        self.fields['quantidade'].label = "Quantidade"


class BaseItemAlugadoFormSet(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        self.usuario = kwargs.pop('usuario', None)
        super().__init__(*args, **kwargs)

    def _construct_form(self, i, **kwargs):
        """Passa o usuário para cada form individual."""
        kwargs['usuario'] = self.usuario
        return super()._construct_form(i, **kwargs)


ItemAlugadoFormSet = inlineformset_factory(
    Aluguel,
    ItemAlugado,
    form=ItemAlugadoForm,
    formset=BaseItemAlugadoFormSet,
)