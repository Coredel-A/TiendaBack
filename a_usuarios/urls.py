from django.urls import path
from .views import RegistroUsuarioView, LoginView, UsuarioDetalleView

urlpatterns = [
    path('registro/', RegistroUsuarioView.as_view(), name='registro'),
    path('login/', LoginView.as_view(), name='login'),
    path('perfil/', UsuarioDetalleView.as_view(), name='perfil'),
]
