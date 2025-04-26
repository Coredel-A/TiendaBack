from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import AllowAny  # Importa AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import check_password
from .models import Usuario
from .serializers import UsuarioSerializer

@api_view(['POST'])
@permission_classes([AllowAny])  # Permite acceso sin autenticación
def registro_usuario(request):
    if request.method == 'POST':
        serializer = UsuarioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Usuario creado con éxito'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            usuario = Usuario.objects.get(email=email)
            if check_password(password, usuario.password):
                # Generar un token JWT manualmente (o simplemente devolver info básica)
                return Response({
                    'message': 'Login exitoso',
                    'usuario_id': usuario.id,
                    'nombre': usuario.nombre
                }, status=200)
            else:
                return Response({'error': 'Contraseña incorrecta'}, status=400)
        except Usuario.DoesNotExist:
            return Response({'error': 'Usuario no encontrado'}, status=404)
        
class PerfilUsuarioView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UsuarioSerializer(request.user)
        return Response(serializer.data)

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
