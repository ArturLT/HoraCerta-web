from django.db import models
from accounts.models import User
from clients.models import Cliente
from items.models import Item_aluguel
from datetime import date

class Aluguel(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    data_inicio = models.DateField()
    data_fim = models.DateField()
    dias = models.PositiveIntegerField(default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def calcular_total(self):
        if(self.data_fim == self.data_inicio):
            self.dias = 1
        else:
            self.dias = (self.data_fim - self.data_inicio).days
        total = sum(item.subtotal(self.dias) for item in self.itens.all())
        self.total = total
        return total
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)   
        self.total = self.calcular_total()
        self.dias = (self.data_fim - self.data_inicio).days
        super().save(update_fields=['total', 'dias'])


    def __str__(self):
        return f"Aluguel de {self.cliente.nome} ({self.data_inicio.strftime('%d/%m/%Y')} - {self.data_fim.strftime('%d/%m/%Y')})"

class ItemAlugado(models.Model):
    aluguel = models.ForeignKey(Aluguel, on_delete=models.CASCADE, related_name='itens')
    item = models.ForeignKey(Item_aluguel, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()
    valor_diaria = models.DecimalField(max_digits=10, decimal_places=2)

    def subtotal(self, dias):
        return self.quantidade * self.valor_diaria * dias

    def __str__(self):
        return f"{self.item.nome} x{self.quantidade} (R$ {self.valor_diaria}/dia)"
