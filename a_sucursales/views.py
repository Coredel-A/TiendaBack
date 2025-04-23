from django.shortcuts import render
from .models import Sucursal
from .serializers import SucursalSerializer
from rest_framework import viewsets
# Create your views here.

class SucursalViewSet(viewsets.ModelViewSet):
    queryset = Sucursal.objects.all()
    serializer_class = SucursalSerializer