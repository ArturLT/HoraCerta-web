from django.db import models
from datetime import date # Importe o módulo date

class Item(models.Model):
    TIPO_CHOICES = [
        ('receita', 'Receita'),
        ('despesa', 'Despesa'),
        ('investimento', 'Investimento'),
    ]

    usuario = models.ForeignKey('accounts.User', on_delete=models.CASCADE)

    valor = models.DecimalField(max_digits=1000000, decimal_places=2)
    data_transacao = models.DateField(default=date.today) 
    recorrente = models.BooleanField(default=False)
    
    descricao = models.TextField(max_length=200)
    tipo = models.CharField(max_length=50, choices=TIPO_CHOICES)

    def __str__(self):
        return f"{self.tipo} - {self.valor} - {self.data_transacao} - {self.usuario.nome} - {self.recorrente} - {self.descricao}"