from django import forms
from .models import Agenda

class AgendaForm(forms.ModelForm):
    class Meta:
        model = Agenda
        fields = [
            'aluguel', 'cliente', 'data_evento',
            'horario_inicio', 'horario_fim',
            'descricao', 'status'
        ]
        widgets = {
            'data_evento': forms.DateInput(attrs={'type': 'date'}),
            'horario_inicio': forms.TimeInput(attrs={'type': 'time'}),
            'horario_fim': forms.TimeInput(attrs={'type': 'time'}),
            'descricao': forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            'data_evento': 'Data do Evento',
            'horario_inicio': 'Horário de Início',
            'horario_fim': 'Horário de Fim',
            'descricao': 'Descrição',
            'status': 'Status do Agendamento',
        }