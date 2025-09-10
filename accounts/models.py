from django.db import models

class User(models.Model):
    nome = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=128)
    nome_empresa = models.CharField(max_length=150, blank=True, null=True)

    def __str__(self):
        return self.nome