from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import Usuario, DireccionEnvio

class DireccionEnvioSerializer(serializers.ModelSerializer):
    class Meta:
        model = DireccionEnvio
        fields = ['id', 'usuario', 'direccion', 'ciudad', 'departamento', 'pais', 'codigo_postal', 'telefono_contacto']

class UsuarioSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    direcciones_envio = DireccionEnvioSerializer(many=True, read_only=True)

    class Meta:
        model = Usuario
        fields = ['id', 'nombre', 'email', 'telefono', 'rol', 'puesto', 'sucursal', 'estado', 'fecha_registro', 'password', 'direcciones_envio']

    def create(self, validated_data):
        password = validated_data.pop('password')
        usuario = Usuario(**validated_data)
        usuario.set_password(password)
        usuario.save()
        return usuario
    
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'), email=email, password=password)
            if not user:
                raise serializers.ValidationError('Credenciales incorrectas.')
        else:
            raise serializers.ValidationError('Debes proporcionar email y contraseña.')

        data['user'] = user
        return data
