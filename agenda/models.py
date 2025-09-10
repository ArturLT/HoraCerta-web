from django.db import models

class Evento(models.Model):

    usuario = models.ForeignKey('accounts.User', on_delete=models.CASCADE)


    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    data_hora_inicio = models.DateTimeField()
    data_hora_fim = models.DateTimeField()

    def __str__(self):
        return self.titulo