from rest_framework import serializers
from .models import Empleado

class EmpleadoRegistroSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = Empleado
        fields = ['id','email','nombre','puesto','fecha_contratacion','estado','sucursal']
        extra_kwargs = {
            'password': {'write_only': True}
        }
        
    def create(self, validated_data):
        password = validated_data.pop('password')
        empleado = Empleado.objects.create_user(**validated_data, password=password)
        return empleado

class EmpleadoPerfilSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empleado
        fields = ['id','email','nombre','puesto','estado','sucursal']

class EmpleadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empleado
        fields = ['id','email','nombre','puesto','fecha_contratacion','estado','sucursal']