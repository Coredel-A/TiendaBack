from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import Orden
from .serializers import OrdenSerializer
# Create your views here.

class OrdenViewSet(viewsets.ModelViewSet):
    queryset = Orden.objects.all()
    serializer_class = OrdenSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(usuario=self.request.user)
        else:
            serializer.save()
