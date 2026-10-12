
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import F
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .models import Evento, Inscricao


@receiver(pre_save, sender=Inscricao)
def guardar_status_anterior(sender, instance, **kwargs):
    if instance.pk:
        try:
            inscricao_antiga = Inscricao.objects.get(pk=instance.pk)
            instance._status_anterior = inscricao_antiga.status
        except Inscricao.DoesNotExist:
            instance._status_anterior = None
    else:
        instance._status_anterior = None

    vai_ativar = (
        instance.status == 'ATIVA'
        and getattr(instance, '_status_anterior', None) != 'ATIVA'
    )

    if vai_ativar:
        evento = Evento.objects.get(pk=instance.evento_id)

        if evento.vagas_disponiveis <= 0:
            raise ValidationError(
                'Não há vagas disponíveis para este evento.'
            )


@receiver(post_save, sender=Inscricao)
def atualizar_vagas_apos_salvar(sender, instance, created, **kwargs):
    status_anterior = getattr(instance, '_status_anterior', None)
    status_atual = instance.status

    if created and status_atual == 'ATIVA':
        variacao = -1

    elif (
        not created
        and status_anterior == 'ATIVA'
        and status_atual == 'CANCELADA'
    ):
        variacao = 1

    elif (
        not created
        and status_anterior == 'CANCELADA'
        and status_atual == 'ATIVA'
    ):
        variacao = -1

    else:
        return

    with transaction.atomic():
        Evento.objects.filter(pk=instance.evento_id).update(
            vagas_disponiveis=F('vagas_disponiveis') + variacao
        )
