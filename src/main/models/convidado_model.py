from django.db import models
from main.models.user_model import User

class Convidado(models.Model):
    user = models.OnetoOneField(User, on_delete=models.CASCADE)
    telefone = models.CharField(max_length=20)