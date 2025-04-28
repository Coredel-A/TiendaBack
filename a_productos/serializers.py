from rest_framework import serializers
from .models import Categoria, Producto

class CategoriaSerializer(serializers.ModelSerializer):
    imagen = serializers.ImageField(required=False)  

    class Meta:
        model = Categoria
        fields = ['id', 'nombre', 'descripcion', 'imagen']

class ProductoSerializer(serializers.ModelSerializer):
    categoria = CategoriaSerializer(read_only=True)
    categoria_id = serializers.PrimaryKeyRelatedField(
        queryset=Categoria.objects.all(), source='categoria', write_only=True
    )
    imagen = serializers.ImageField(required=False, allow_null=True)  # Permitir null y ausencia de imagen

    class Meta:
        model = Producto
        fields = [
            'id', 'nombre', 'descripcion', 'especificaciones', 'marca',
            'modelo', 'precio', 'imagen', 'estado', 'categoria', 'categoria_id'
        ]
