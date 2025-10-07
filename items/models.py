from django.db import models

class Item_aluguel(models.Model):
    nome = models.CharField(max_length=150)
    quantidade_total = models.PositiveSmallIntegerField()
    diaria = models.DecimalField(max_digits=10, decimal_places=2)
    usuario = models.ForeignKey('accounts.User', on_delete=models.CASCADE)

def __str__(self):
    return f"{self.nome} - {self.quantidade_total} disponiveis"


