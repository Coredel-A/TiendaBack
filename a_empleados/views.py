from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth import authenticate
from .models import Empleado
from .serializers import EmpleadoRegistroSerializer, EmpleadoPerfilSerializer
from rest_framework_simplejwt.tokens import RefreshToken
# Create your views here.

class EmpleadoLoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        empleado = authenticate(request, email=email, password=password)

        if empleado is not None:
            refresh = RefreshToken.for_user(empleado)
            return Response({
                'token':{
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                },
                'empleado': {
                    'id': empleado.id,
                    'nombre': empleado.nombre,
                    'email': empleado.email,
                    'puesto': empleado.puesto,
                }
            })
        return Response({'error': 'Credenciales invalidas'}, status=status.HTTP_401_UNAUTHORIZED)
    
class EmpleadoPerfilView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = EmpleadoPerfilSerializer(request.user)
        return Response(serializer.data)

class EmpleadoRegistroView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = EmpleadoRegistroSerializer(data=request.data)
        if serializer.is_valid():
            empleado = serializer.save()
            return Response({'mensaje': 'Empleado creado correctamente'}, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    