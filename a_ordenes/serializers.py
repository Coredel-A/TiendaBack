from rest_framework import serializers
from .models import Orden, OrdenDetalle
from a_productos.models import Producto
from a_usuarios.models import Usuario, DireccionEnvio
from a_sucursales.models import Sucursal

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
    direccion_envio_id = serializers.PrimaryKeyRelatedField(
        queryset=DireccionEnvio.objects.all(), source='direccion_envio', write_only=True, allow_null=True, required=False
    )
    sucursal_retiro_id = serializers.PrimaryKeyRelatedField(
        queryset=Sucursal.objects.all(), source='sucursal_retiro', write_only=True, allow_null=True, required=False
    )
    direccion_envio = serializers.StringRelatedField(read_only=True)
    sucursal_retiro = serializers.StringRelatedField(read_only=True)
    detalles = OrdenDetalleSerializer(many=True)

    class Meta:
        model = Orden
        fields = [
            'id','usuario','usuario_id','fecha_creacion','estado',
            'tipo_envio','forma_pago','total','seguimiento',
            'direccion_envio', 'direccion_envio_id',
            'sucursal_retiro', 'sucursal_retiro_id',
            'detalles'
        ]
    
    def validate(self, data):
        tipo_envio = data.get('tipo_envio')
        tiene_direccion = data.get('direccion_envio') is not None
        tiene_sucursal = data.get('sucursal_retiro') is not None

        if tipo_envio == 'domicilio' and not tiene_direccion:
            raise serializers.ValidationError("Se requiere una dirección de envío para el tipo 'envio'.")
        if tipo_envio == 'sucursal' and not tiene_sucursal:
            raise serializers.ValidationError("Se requiere una sucursal para el tipo 'recoger'.")
        if tipo_envio == 'domicilio' and tiene_sucursal:
            raise serializers.ValidationError("No se debe incluir sucursal en un envío a domicilio.")
        if tipo_envio == 'sucursal' and tiene_direccion:
            raise serializers.ValidationError("No se debe incluir dirección en una orden con retiro en sucursal.")
        return data

    def create(self, validated_data):
        detalles_data = validated_data.pop('detalles')       
        total = 0
        orden = Orden.objects.create(**validated_data)

        for detalle in detalles_data:
            cantidad = detalle['cantidad']
            precio_unitario = detalle['precio_unitario']
            total += cantidad * precio_unitario
            OrdenDetalle.objects.create(orden=orden, **detalle)
        
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

