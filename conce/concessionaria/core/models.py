from django.db import models

class Carro(models.Model):
    marca = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    ano = models.IntegerField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    cor = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.marca} {self.modelo} ({self.ano}) - {self.cor}"

class Venda(models.Model):
    carro = models.ForeignKey(Carro, on_delete=models.CASCADE)
    cliente_nome = models.CharField(max_length=100)
    valor_venda = models.DecimalField(max_digits=10, decimal_places=2)
    data_venda = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Venda de {self.carro} para {self.cliente_nome}"
