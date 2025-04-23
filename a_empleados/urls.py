from django.urls import path
from .views import EmpleadoLoginView, EmpleadoPerfilView, EmpleadoRegistroView


urlpatterns = [
    path('empleado/login/', EmpleadoLoginView.as_view(), name='empleado-login'),
    path('empleado/perfil/', EmpleadoPerfilView.as_view(), name='empleado-perfil'),
    path('empleados/', EmpleadoRegistroView.as_view(), name='empleado-registro'),
]