from rest_framework import viewsets
from .models import Evento, Participante, Inscricao
from .serializers import EventoSerializer, ParticipanteSerializer, InscricaoSerializer
from django.db.models import Count, Q
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class EventoViewSet(viewsets.ModelViewSet):
    queryset = Evento.objects.all()
    serializer_class = EventoSerializer
    permission_classes = [IsAuthenticated]


class ParticipanteViewSet(viewsets.ModelViewSet):
    queryset = Participante.objects.all()
    serializer_class = ParticipanteSerializer

class InscricaoViewSet(viewsets.ModelViewSet):
    queryset = Inscricao.objects.all()
    serializer_class = InscricaoSerializer

#consultas avançadas - uso do related_name 
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def relatorio_eventos(request):
    eventos = Evento.objects.annotate(
        inscricoes_ativas=Count(
            'inscricoes',
            filter=Q(inscricoes__status='ATIVA')
        )
    ).values(
        'id',
        'nome',
        'inscricoes_ativas'
    )

    return Response(eventos)
