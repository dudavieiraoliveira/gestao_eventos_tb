from rest_framework import serializers
from .models import Evento, Participante, Inscricao


class ParticipanteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participante
        fields = ["id", "nome", "email"]


class EventoSerializer(serializers.ModelSerializer):
    # serializer aninhado - requisito
    # ao consultar um evento, a API poderá apresentar 
    # os dados dos participantes, em vez de somente seus IDs.
    participantes = ParticipanteSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Evento
        fields = [
            "id",
            "nome",
            "descricao",
            "data",
            "local",
            "vagas_total",
            "vagas_disponiveis",
            "ativo",
            "organizador",
            "participantes",
        ]


class InscricaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inscricao
        fields = [
            "id",
            "evento",
            "participante",
            "data_inscricao",
            "status",
        ]

