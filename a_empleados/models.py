from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class EmpleadoManager(BaseUserManager):
    def create_user(self, email, nombre, password=None, **extra_fields):
        if not email:
            raise ValueError('El email es obligatorio')
        email = self.normalize_email(email)
        empleado = self.model(email=email, nombre=nombre, **extra_fields)
        empleado.set_password(password)
        empleado.save(using=self._db)
        return empleado
    
    def create_superuser(self, email, nombre, password=None, **extra_fields):
        # Configurar campos para superusuario
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('estado', 'activo')
        
        # Puedes establecer valores predeterminados para campos obligatorios
        # si no se proporcionan al crear un superusuario desde la línea de comandos
        if 'puesto' not in extra_fields:
            extra_fields['puesto'] = 'Administrador'
        
        if 'fecha_contratacion' not in extra_fields:
            from datetime import date
            extra_fields['fecha_contratacion'] = date.today()
        
        if 'sucursal_id' not in extra_fields:
            # Necesitas obtener una sucursal válida o crearla
            from a_sucursales.models import Sucursal
            sucursal, created = Sucursal.objects.get_or_create(
                nombre="Sucursal Principal",
                defaults={
                    'direccion': 'Dirección administrativa',
                    'telefono': '000000000',
                    # Añade aquí otros campos obligatorios de Sucursal
                }
            )
            extra_fields['sucursal'] = sucursal
            
        return self.create_user(email, nombre, password, **extra_fields)

class Empleado(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    nombre = models.CharField(max_length=100)
    puesto = models.CharField(max_length=50)
    fecha_contratacion = models.DateField()
    estado = models.CharField(max_length=20, default='activo')
    sucursal = models.ForeignKey('a_sucursales.Sucursal', on_delete=models.CASCADE)
    
    # Campos necesarios para el admin de Django
    is_staff = models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.')
    is_active = models.BooleanField(default=True, help_text='Designates whether this user should be treated as active.')

    objects = EmpleadoManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nombre']

    def __str__(self):
        return f"{self.nombre} ({self.puesto})"
