from django.contrib import admin
from .models import Categoria
from .models import Producto

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre']
    search_fields = ['nombre']

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre','marca','modelo','precio','categoria','estado']
    search_fields = ['nombre','marca','modelo']
    list_filter = ['estado','categoria']

    