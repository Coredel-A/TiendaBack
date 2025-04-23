from rest_framework import serializers
from .models import Inventario
from a_productos.models import Producto
from a_sucursales.models import Sucursal

class InventarioSerializer(serializers.ModelSerializer):
    producto = serializers.StringRelatedField(read_only=True)
    producto_id = serializers.PrimaryKeyRelatedField(
        queryset=Producto.objects.all(), source='producto',write_only=True
    )

    sucursal = serializers.StringRelatedField(read_only=True)
    sucursal_id = serializers.PrimaryKeyRelatedField(
        queryset=Sucursal.objects.all(), source='sucursal', write_only=True
    )

    class Meta:
        model = Inventario
        fields = ['id','producto','producto_id','sucursal','sucursal_id','cantidad']