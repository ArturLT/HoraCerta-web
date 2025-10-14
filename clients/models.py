from django.db import models


class Cliente(models.Model):
    usuario = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    nome = models.CharField(max_length=150)
    cpf = models.CharField(max_length=14, unique=True)
    telefone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    endereco = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"{self.nome} ({self.cpf})"
