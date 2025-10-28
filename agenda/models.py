from django.db import models
from accounts.models import User
from clients.models import Cliente
from items.models import Item_aluguel
from itemAlugados.models import Aluguel

class Agenda(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    aluguel = models.ForeignKey(Aluguel, on_delete=models.CASCADE, related_name='agendas')
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    data_evento = models.DateField()
    horario_inicio = models.TimeField(null=True, blank=True)
    horario_fim = models.TimeField(null=True, blank=True)
    descricao = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('pendente', 'Pendente'),
            ('confirmado', 'Confirmado'),
            ('cancelado', 'Cancelado')
        ],
        default='pendente'
    )

    class Meta:
        ordering = ['data_evento', 'horario_inicio']
        verbose_name = 'Agenda'
        verbose_name_plural = 'Agendas'

    def __str__(self):
        return f"{self.data_evento.strftime('%d/%m/%Y')} - {self.cliente.nome} ({self.status})"
