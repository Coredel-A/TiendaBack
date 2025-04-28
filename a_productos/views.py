from rest_framework import viewsets, permissions, parsers
from django_filters import rest_framework as filters
from rest_framework.filters import SearchFilter  # Importa SearchFilter correctamente
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
    filter_backends = (filters.DjangoFilterBackend, SearchFilter)  # Utiliza SearchFilter correctamente
    filterset_class = ProductoFilter
    search_fields = ['nombre', 'descripcion', 'marca', 'modelo']

    def get_queryset(self):
        # Filtro por categoría
        categoria_id = self.request.query_params.get('categoria', None)
        queryset = Producto.objects.all()

        if categoria_id:
            print(f"Filtrando por categoría ID: {categoria_id}")  # Debugging
            queryset = queryset.filter(categoria_id=categoria_id)

        # Si se incluye un parámetro de búsqueda, se aplica
        search_param = self.request.query_params.get('search', None)
        if search_param:
            print(f"Filtrando por búsqueda: {search_param}")  # Debugging
            queryset = queryset.filter(nombre__icontains=search_param)  # Filtrar por nombre, puedes incluir otros campos

        return queryset

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [permissions.AllowAny]
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]

