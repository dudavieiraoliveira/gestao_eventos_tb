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
