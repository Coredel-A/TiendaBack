from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Usuario, DireccionEnvio
from .serializers import UsuarioSerializer, LoginSerializer, DireccionEnvioSerializer
from rest_framework_simplejwt.tokens import RefreshToken

class DireccionesEnvioView(generics.ListCreateAPIView):
    serializer_class = DireccionEnvioSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return DireccionEnvio.objects.filter(usuario=self.request.user)

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)

class DireccionEnvioDetalleView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DireccionEnvioSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return DireccionEnvio.objects.filter(usuario=self.request.user)

class RegistroUsuarioView(generics.CreateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [AllowAny]

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        usuario = serializer.validated_data['user']

        refresh = RefreshToken.for_user(usuario)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': UsuarioSerializer(usuario).data
        }, status=status.HTTP_200_OK)

class UsuarioDetalleView(generics.RetrieveAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

