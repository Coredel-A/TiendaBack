from django.urls import path
from .views import ( 
    RegistroUsuarioView, LoginView, UsuarioDetalleView,
    DireccionesEnvioView, DireccionEnvioDetalleView)

urlpatterns = [
    path('registro/', RegistroUsuarioView.as_view(), name='registro'),
    path('login/', LoginView.as_view(), name='login'),
    path('perfil/', UsuarioDetalleView.as_view(), name='perfil'),
    path('direcciones-envio/', DireccionesEnvioView.as_view(), name='lista-direcciones'),
    path('direcciones-envio/<int:pk>/', DireccionEnvioDetalleView.as_view(), name='detalle-direccion'),
]
