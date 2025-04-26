from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/token/', obtain_auth_token, name='api_token_auth'),
    path('api/usuarios/', include('a_usuarios.urls')),
    path('api/empleados/', include('a_empleados.urls')),
    path('api/productos/', include('a_productos.urls')),
    path('api/inventario/', include('a_inventario.urls')),
    path('api/ordenes/', include('a_ordenes.urls')),
    path('api/sucursales/', include('a_sucursales.urls')),
]
