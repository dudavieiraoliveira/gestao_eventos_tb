from django.db import models
from django.contrib.auth.models import User

#relação 1:1
class PerfilOrganizador(models.Model):
    usuario = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )
    telefone = models.CharField(max_length=20)
    empresa = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return self.usuario.username


class Participante(models.Model):
    nome = models.CharField(max_length=150)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.nome

# classe Manager - guarda consultas personalizadas
class EventoManager(models.Manager):
    def disponiveis(self):
        return self.filter(
            ativo=True,
            vagas_disponiveis__gt=0
        )
    
class Evento(models.Model):
    # faz a ligação com nossa classe EventoManager
    objects = EventoManager()

# relação 1:N + related_name (acesso)
# (um evento pode ter apenas um organizador /
# um organizador pode ter vários eventos)

    organizador = models.ForeignKey(
    PerfilOrganizador,
    on_delete=models.CASCADE,
    related_name='eventos',
    null=True,
    blank=True,
)
    
# relação N:N + related_name (acesso) + through (identifica tabela intermediária)
# (um evento pode ter vários participantes /
# um participante pode ter vários eventos)

    participantes = models.ManyToManyField(
    Participante,
    through='Inscricao',
    related_name='eventos'
)
    nome = models.CharField(max_length=150)
    descricao = models.TextField()
    data = models.DateTimeField()
    local = models.CharField(max_length=200)
    vagas_total = models.PositiveIntegerField()
    vagas_disponiveis = models.PositiveIntegerField()
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome

# classe intermediária da relação N:N (eventos : participantes)
class Inscricao(models.Model):

    # relaçãos N:1 + related_name (acesso)
    evento = models.ForeignKey(
        Evento,
        on_delete=models.CASCADE,
        related_name='inscricoes'
    )
    participante = models.ForeignKey(
        Participante,
        on_delete=models.CASCADE,
        related_name='inscricoes'
    )
    data_inscricao = models.DateTimeField(auto_now_add=True)

    STATUS_CHOICES = [
        ('ATIVA', 'Ativa'),
        ('CANCELADA', 'Cancelada'),
    ]

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='ATIVA'
    )
    # classe meta define regras e configurações sobre os dados
    class Meta:
        # valida que o mesmo participante só pode ter uma inscrição para o eventos
        unique_together = ('evento', 'participante')

    def __str__(self):
        return f'{self.participante} - {self.evento}'