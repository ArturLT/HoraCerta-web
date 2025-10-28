from django.db.models.signals import post_save
from django.dispatch import receiver
from itemAlugados.models import Aluguel
from .models import Agenda

@receiver(post_save, sender=Aluguel)
def criar_agenda_automatica(sender, instance, created, **kwargs):
    if created:
        Agenda.objects.create(
            usuario=instance.usuario,
            aluguel=instance,
            cliente=instance.cliente,
            data_evento=instance.data_inicio,
            descricao=f"Agendamento automático para o aluguel de {instance.cliente.nome}"
        )
