from rest_framework import serializers
from .models import Orden, OrdenDetalle
from a_productos.models import Producto
from a_usuarios.models import Usuario

class OrdenDetalleSerializer(serializers.ModelSerializer):
    producto = serializers.StringRelatedField(read_only=True)
    producto_id = serializers.PrimaryKeyRelatedField(
        queryset=Producto.objects.all(), source='producto', write_only=True
    )

    class Meta:
        model = OrdenDetalle
        fields = ['id','producto','producto_id','cantidad','precio_unitario']

class OrdenSerializer(serializers.ModelSerializer):
    usuario = serializers.StringRelatedField(read_only=True)
    usuario_id = serializers.PrimaryKeyRelatedField(
        queryset=Usuario.objects.all(), source='usuario', write_only=True
    )

    detalles = OrdenDetalleSerializer(many=True)

    class Meta:
        model = Orden
        fields = [
            'id','usuario','usuario_id','fecha_creacion','estado',
            'tipo_envio','forma_pago','total','seguimiento','detalles'
        ]
    
    def create(self, validated_data):
        detalles_data = validated_data.pop('detalles')
        
        # Inicializamos el total en 0
        total = 0

        # Primero creamos la orden, pero aún no guardamos el total
        orden = Orden.objects.create(**validated_data)

        for detalle in detalles_data:
            cantidad = detalle['cantidad']
            precio_unitario = detalle['precio_unitario']
            total += cantidad * precio_unitario
            OrdenDetalle.objects.create(orden=orden, **detalle)
        
        # Ahora actualizamos el total
        orden.total = total
        orden.save()

        return orden
    
    def update(self, instance, validated_data):
        detalle_data = validated_data.pop('detalles', None)
        instance = super().update(instance,validated_data)

        if detalle_data is not None:
            instance.detalles.all().delete()
            for detalle in detalle_data:
                OrdenDetalle.objects.create(orden=instance,**detalle)
        return instance

