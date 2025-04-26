from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView
from .views import UsuarioViewSet
from .views import registro_usuario, PerfilUsuarioView
from .views import LoginView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet)

urlpatterns = [
    path('registro/', registro_usuario, name='registro_usuario'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('perfil/', PerfilUsuarioView.as_view(), name='perfil-usuario'),
    path('', include(router.urls)),  # rutas automáticas de ViewSet
]

