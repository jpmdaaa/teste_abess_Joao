from django.db import models

class Cotacao(models.Model):
    data = models.DateField()
    moeda = models.CharField(max_length=10)
    valor = models.DecimalField(max_digits=10, decimal_places=4)

    class Meta:
        unique_together = ('data', 'moeda')

    def __str__(self):
        return f'{self.data} - {self.moeda}: {self.valor}'
