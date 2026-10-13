from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import EventoViewSet, ParticipanteViewSet, InscricaoViewSet, relatorio_eventos

router = DefaultRouter()
router.register("eventos", EventoViewSet, basename="evento")
router.register("participantes", ParticipanteViewSet, basename="participante")
router.register("inscricoes", InscricaoViewSet, basename="inscricao")

urlpatterns = [
    path("relatorios/eventos/", relatorio_eventos, name="relatorio-eventos"),
] + router.urls
