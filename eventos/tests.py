from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.test import TestCase

from .models import PerfilOrganizador, Evento, Participante, Inscricao


class SignalInscricaoTestCase(TestCase):
    def setUp(self):
        """Prepara os objetos utilizados nos testes."""
        self.usuario = User.objects.create_user(
            username="organizadora",
            password="senha-teste-123",
        )

        self.perfil = PerfilOrganizador.objects.create(
            usuario=self.usuario,
            telefone="51999999999",
            empresa="Empresa Teste",
        )

        self.evento = Evento.objects.create(
            nome="Evento de Teste",
            descricao="Evento utilizado nos testes do Signal",
            data=timezone.now(),
            local="Porto Alegre",
            vagas_total=5,
            vagas_disponiveis=5,
            ativo=True,
            organizador=self.perfil,
        )

        self.participante = Participante.objects.create(
            nome="Participante Teste",
            email="participante@teste.com",
        )

    def test_nova_inscricao_ativa_diminui_vagas(self):
        Inscricao.objects.create(
            evento=self.evento,
            participante=self.participante,
            status="ATIVA",
        )

        self.evento.refresh_from_db()
        self.assertEqual(self.evento.vagas_disponiveis, 4)

    def test_cancelamento_de_inscricao_devolve_vaga(self):
        inscricao = Inscricao.objects.create(
            evento=self.evento,
            participante=self.participante,
            status="ATIVA",
        )

        inscricao.status = "CANCELADA"
        inscricao.save()

        self.evento.refresh_from_db()
        self.assertEqual(self.evento.vagas_disponiveis, 5)

    def test_reativacao_de_inscricao_consume_vaga(self):
        inscricao = Inscricao.objects.create(
            evento=self.evento,
            participante=self.participante,
            status="ATIVA",
        )

        inscricao.status = "CANCELADA"
        inscricao.save()

        inscricao.status = "ATIVA"
        inscricao.save()

        self.evento.refresh_from_db()
        self.assertEqual(self.evento.vagas_disponiveis, 4)

    def test_nao_permite_inscricao_sem_vagas(self):
        self.evento.vagas_disponiveis = 0
        self.evento.save(update_fields=["vagas_disponiveis"])

        with self.assertRaises(ValidationError):
            Inscricao.objects.create(
                evento=self.evento,
                participante=self.participante,
                status="ATIVA",
            )

    def test_salvar_sem_mudar_status_nao_altera_vagas(self):
        inscricao = Inscricao.objects.create(
            evento=self.evento,
            participante=self.participante,
            status="ATIVA",
        )

        inscricao.save()

        self.evento.refresh_from_db()
        self.assertEqual(self.evento.vagas_disponiveis, 4)
