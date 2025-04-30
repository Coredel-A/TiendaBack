from django.db import models

class Sucursal(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.TextField()
    pais = models.CharField(max_length=50)
    telefono = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.nombre} - {self.pais}"