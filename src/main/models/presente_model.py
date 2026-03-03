from django.db import models
from django.contrib.auth.models import AbstractUser

class Presente(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    foto = models.ImageField(upload_to='presentes/', null=True, blank=True)
    
    def __str__(self):
        return self.nome


