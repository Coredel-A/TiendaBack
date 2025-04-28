from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario

class UsuarioAdmin(UserAdmin):
    model = Usuario
    list_display = ('email', 'nombre', 'rol', 'estado', 'is_staff')
    list_filter = ('rol', 'estado', 'is_staff')
    fieldsets = (
        (None, {'fields': ('email', 'nombre', 'password')}),
        ('Información personal', {'fields': ('telefono', 'rol', 'puesto', 'sucursal', 'estado')}),
        ('Permisos', {'fields': ('is_staff', 'is_superuser', 'is_active', 'groups', 'user_permissions')}),
        ('Fechas importantes', {'fields': ('last_login', 'fecha_registro')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'nombre', 'password1', 'password2', 'rol', 'estado', 'is_staff', 'is_superuser'),
        }),
    )
    search_fields = ('email', 'nombre')
    ordering = ('email',)

admin.site.register(Usuario, UsuarioAdmin)
