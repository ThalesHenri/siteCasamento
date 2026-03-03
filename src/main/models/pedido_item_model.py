from django.db import models
from .pedido_model import Pedido
from .presente_model import Presente


class PedidoItem(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='items')
    presente = models.ForeignKey(Presente, on_delete=models.CASCADE)
    quantidade = models.IntegerField(default=1)
    valor = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f"{self.presente} - {self.quantidade}"