from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import Inventario
from .serializzers import InventarioSerializer
# Create your views here.

class InventarioViewSet(viewsets.ModelViewSet):
    queryset = Inventario.objects.all()
    serializer_class = InventarioSerializer
    permission_classes = [permissions.AllowAny]
