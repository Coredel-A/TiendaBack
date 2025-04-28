from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/usuarios/', include('a_usuarios.urls')),
    path('api/productos/', include('a_productos.urls')),
    path('api/inventario/', include('a_inventario.urls')),
    path('api/ordenes/', include('a_ordenes.urls')),
    path('api/sucursales/', include('a_sucursales.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
