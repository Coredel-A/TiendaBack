from django.db import models
from django.db import models
from a_productos.models import Producto
from a_sucursales.models import Sucursal
# Create your models here.

class Inventario(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)
    cantidad = models.PositiveBigIntegerField()

    class Meta:
        unique_together = ('producto','sucursal')
    
    def __str__(self):
        return f"{self.producto.nombre} - {self.sucursal.nombre} ({self.cantidad})"
