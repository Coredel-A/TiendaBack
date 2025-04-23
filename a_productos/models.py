from django.db import models
# Create your models here.

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre
    
class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    especificaciones = models.TextField()
    marca = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    imagenes = models.TextField()
    estado = models.CharField(max_length=20, choices=[
        ('activo', 'Activo'),
        ('descontinuado', 'Descontinuado'),
        ('agotado', 'Agotado'),
    ])

    def __str__(self):
        return self.nombre