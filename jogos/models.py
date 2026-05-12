from django.db import models

class Jogo(models.Model):
    nome = models.CharField(max_length=255)
    tipo = models.CharField(max_length=100)
    nota = models.DecimalField(max_digits=3, decimal_places=1)
    review = models.TextField()

    def __str__(self):
        return self.nome