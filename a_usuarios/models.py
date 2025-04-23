from django.db import models
from django.contrib.auth.hashers import make_password
from django.utils import timezone

class Usuario(models.Model):
    ESTADOS = [
        ('activo','Activo'),
        ('inactivo','Inactivo'),
        ('suspendido','Suspendido')
    ]
    nombre = models.CharField(max_length=100, default='Desconocido')
    email = models.EmailField()    
    telefono = models.CharField(max_length=15, blank=True, null=True)
    password = models.CharField(max_length=128)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='activo')
    fecha_registro = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.nombre
    
    def set_password(self, raw_password):
        self.password = make_password(raw_password)