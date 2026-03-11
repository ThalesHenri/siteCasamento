from django.db import models
from .pedido_model import Pedido
from .presente_model import Presente


class PedidoItem(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='items')
    presente = models.ForeignKey(Presente, on_delete=models.CASCADE)
    quantidade = models.IntegerField(default=1)
    # permitir valores maiores (por exemplo R$ 3000,00 ou mais).
    # max_digits inclui todas as casas significativas; com 2 casas decimais, 5
    # dígitos só suportava até 999.99, o que causava InvalidOperation ao tentar
    # gravar ou ler 3000.00. Expandimos para 10 para cobrir a maioria dos usos.
    valor = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f"{self.presente} - {self.quantidade}"

    def clean(self):
        """Valida o campo *valor* antes de salvar no banco.
        O Django chama `clean()` durante o processo de validação de formulários e
        também quando `full_clean()` é executado (por exemplo, no admin). Se o
        valor não puder ser convertido para `Decimal` um `ValidationError` é
        lançado, evitando que dados inválidos sejam persistidos.
        """
        from decimal import Decimal, InvalidOperation
        from django.core.exceptions import ValidationError

        if self.valor is None:
            self.valor = Decimal("0.00")
        else:
            try:
                self.valor = Decimal(self.valor)
            except (InvalidOperation, TypeError):
                raise ValidationError({
                    "valor": "Valor inválido para este item."
                })
