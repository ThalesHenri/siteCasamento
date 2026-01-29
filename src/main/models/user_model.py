from django.contrib.auth.models import AbstractUser
from django.db import models
class User(AbstractUser):
    TIPO_USUARIO_ESCOLHAS = [
        ('convidado','Convidado'),
        ('admin','Administrador'),
    ]
    email = models.EmailField(unique=True)
    tipo_usuario = models.CharField(max_length=20, choices=TIPO_USUARIO_ESCOLHAS, default='convidado')
    
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']