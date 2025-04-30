from django.db import models
from django.db import models
from a_usuarios.models import Usuario, DireccionEnvio
from a_productos.models import Producto
from a_sucursales.models import Sucursal

class Orden(models.Model):
    ESTADOS = [
        ('carrito','Carrito'),
        ('pendiente','Pendiente'),
        ('pagado','Pagado'),
        ('enviado','Enviado'),
        ('entregado','Entregado'),
        ('cancelado','Cancelado'),
    ]

    TIPO_ENVIO = [
        ('envio', 'Envío a domicilio'),
        ('recoger', 'Recoger en sucursal'),
    ]


    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='carrito')
    tipo_envio = models.CharField(max_length=50, choices=TIPO_ENVIO)
    forma_pago = models.CharField(max_length=50)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    seguimiento = models.CharField(max_length=100, blank=True)
    direccion_envio = models.ForeignKey(DireccionEnvio, null=True, blank=True, on_delete=models.SET_NULL)
    sucursal_retiro = models.ForeignKey(Sucursal, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"Orden *{self.id} - {self.usuario.nombre} - {self.estado}"
    
class OrdenDetalle(models.Model):
    orden = models.ForeignKey(Orden, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre} (Orden *{self.orden.id})"
