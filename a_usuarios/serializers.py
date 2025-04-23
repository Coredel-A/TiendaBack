from rest_framework import serializers
from .models import Usuario

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id','nombre','email','telefono','password','estado','fecha_registro']  # o puedes poner los campos específicos: ['id', 'nombre', 'correo', 'telefono', 'password']
        extra_kwargs = {
            'password': {'write_only': True},  # para que no se muestre al obtener los datos
            'fecha_registro': {'read_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        usuario = Usuario(**validated_data)
        usuario.set_password(password)
        usuario.save()
        return usuario
