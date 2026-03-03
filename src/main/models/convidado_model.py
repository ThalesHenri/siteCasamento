from django.db import models
from django.contrib.auth.models import AbstractUser


class Convidado(AbstractUser):
    


    telefone = models.CharField(max_length=20, blank=True)
    presenca_confirmada = models.BooleanField(
        default=False,
        help_text="Marque se o convidado confirmou presença",
    )

    class Meta:
        verbose_name = "convidado"
        verbose_name_plural = "convidados"

    def __str__(self):
        return self.get_full_name() or self.username