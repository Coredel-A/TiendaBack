from rest_framework import viewsets, permissions, parsers
from django_filters import rest_framework as filters
from rest_framework.filters import SearchFilter
from .models import Producto, Categoria
from .serializers import ProductoSerializer, CategoriaSerializer

class ProductoFilter(filters.FilterSet):
    categoria = filters.NumberFilter(field_name='categoria_id')

    class Meta:
        model = Producto
        fields = ['categoria']

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    permission_classes = [permissions.AllowAny]
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]
    filter_backends = (filters.DjangoFilterBackend, SearchFilter)
    filterset_class = ProductoFilter
    search_fields = ['nombre', 'descripcion', 'marca', 'modelo']

    # Simplificamos get_queryset para evitar conflictos con SearchFilter
    def get_queryset(self):
        queryset = Producto.objects.all()
        
        # Filtro por categoría - dejamos esto porque es importante para filtrar por categoría
        categoria_id = self.request.query_params.get('categoria', None)
        if categoria_id:
            queryset = queryset.filter(categoria_id=categoria_id)
            
        # Eliminamos el filtro manual por search para que lo maneje SearchFilter
        return queryset

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [permissions.AllowAny]
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]
