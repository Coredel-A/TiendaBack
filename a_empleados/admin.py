from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Empleado
# Register your models here.

@admin.register(Empleado)
class EmpleadoAdmin(BaseUserAdmin):
    model = Empleado
    list_display = ['email','nombre','puesto','estado','sucursal','fecha_contratacion']
    list_filter = ['estado','puesto','sucursal']
    search_fields = ['email','nombre']
    ordering = ['email']

    fieldsets =(
        (None, {'fields': ('email', 'password')}),
        ('Informacion Personal', {'fields': ('nombre','puesto','fecha_contratacion','estado','sucursal')}),
        ('permisos', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'nombre', 'password1', 'password2', 'puesto', 'fecha_contratacion', 'estado', 'sucursal'),
        }),
    )

