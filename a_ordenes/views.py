import stripe
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import Orden
from .serializers import OrdenSerializer

stripe.api_key = settings.STRIPE_SECRET_KEY

# Viewset de las órdenes
class OrdenViewSet(viewsets.ModelViewSet):
    queryset = Orden.objects.all()
    serializer_class = OrdenSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(usuario=self.request.user)
        else:
            serializer.save()

# Endpoint aparte para Stripe (FUERA de la clase)
@api_view(['POST'])
def create_payment_intent(request):
    try:
        # Recibimos el monto a pagar desde el frontend
        amount = request.data.get('amount')  # Debe venir en centavos
        if not amount:
            return Response({'error': 'Amount is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Crear el PaymentIntent
        intent = stripe.PaymentIntent.create(
            amount=int(amount),
            currency='usd',  # Cambia si quieres otra moneda
            payment_method_types=['card'],
        )

        return Response({
            'client_secret': intent['client_secret']
        })

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
