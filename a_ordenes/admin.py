from django.contrib import admin
from .models import Orden, OrdenDetalle

class OrdenDetalleInline(admin.TabularInline):
    model = OrdenDetalle
    extra = 0

@admin.register(Orden)
class OrdenAdmin(admin.ModelAdmin):
    list_display = ['id','usuario','fecha_creacion','estado','total']
    list_filter = ['estado','forma_pago']
    search_fields = ['usuario__nombre','usuario__email']
    date_hierarchy = 'fecha_creacion'
    inlines = [OrdenDetalleInline]

@admin.register(OrdenDetalle)
class OrdenDetalleAdmin(admin.ModelAdmin):
    list_display = ['orden','producto','cantidad','precio_unitario']
    search_fields = ['orden__usuario__nombre', 'producto__nombre']
