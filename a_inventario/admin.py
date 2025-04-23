from django.contrib import admin
from .models import Inventario
# Register your models here.

@admin.register(Inventario)
class InventarioAdmin(admin.ModelAdmin):
    list_display = ['producto','sucursal','cantidad']
    search_fields = ['producto__nombre','sucursal__nombre']
    list_filter = ['sucursal']
