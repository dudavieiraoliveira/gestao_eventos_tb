from rest_framework.routers import DefaultRouter
from .views import EventoViewSet, ParticipanteViewSet, InscricaoViewSet

router = DefaultRouter()
router.register("eventos", EventoViewSet, basename="evento")
router.register("participantes", ParticipanteViewSet, basename="participante")
router.register("inscricoes", InscricaoViewSet, basename="inscricao")

urlpatterns = router.urls
