from django.db import models
class Pedido(models.Model):
    convidado = models.ForeignKey('main.Convidado', on_delete=models.CASCADE)
    data_compra = models.DateTimeField(auto_now_add=True)
    pago = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Pedido de {self.convidado},data {self.data_compra}"