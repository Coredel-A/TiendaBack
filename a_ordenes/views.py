import stripe
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticated
from .models import Orden, OrdenDetalle
from .serializers import OrdenSerializer
from a_productos.models import Producto
from a_productos.serializers import ProductoSerializer
import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules

stripe.api_key = settings.STRIPE_SECRET_KEY

class OrdenViewSet(viewsets.ModelViewSet):
    queryset = Orden.objects.all()
    serializer_class = OrdenSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)

@api_view(['POST'])
def create_payment_intent(request):
    try:
        amount = request.data.get('amount')  
        if not amount:
            return Response({'error': 'Amount is required'}, status=status.HTTP_400_BAD_REQUEST)

        intent = stripe.PaymentIntent.create(
            amount=int(amount),
            currency='usd',  
            payment_method_types=['card'],
        )

        return Response({
            'client_secret': intent['client_secret']
        })

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def obtener_sugerencias(request):
    try:
        productos = request.data.get('productos', [])
        
        if not productos or not isinstance(productos, list):
            return Response({"error": "Se requiere una lista de productos"}, status=status.HTTP_400_BAD_REQUEST)
        
        datos_transacciones = cargar_datos()      
        df = preparar_dataframe(datos_transacciones)       
        reglas = generar_reglas(df)
        productos_sugeridos = []
        
        for producto in productos:
            reglas_producto = reglas[
                reglas['antecedents'].apply(lambda x: producto in x)
            ]
            
            if not reglas_producto.empty:
                reglas_producto = reglas_producto.sort_values('confidence', ascending=False)
                
                for _, regla in reglas_producto.iterrows():
                    for prod_consecuente in regla['consequents']:
                        if prod_consecuente not in productos and prod_consecuente not in productos_sugeridos:
                            productos_sugeridos.append(prod_consecuente)
                            if len(productos_sugeridos) >= 5: 
                                break
                    
                    if len(productos_sugeridos) >= 5:
                        break
        
        sugerencias_objetos = Producto.objects.filter(nombre__in=productos_sugeridos)
        serializer = ProductoSerializer(sugerencias_objetos, many=True)
        
        return Response({"sugerencias": serializer.data})
    
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def cargar_datos():
    detalles = OrdenDetalle.objects.select_related('orden', 'producto').all()
    data = {}

    for detalle in detalles:
        orden_id = detalle.orden.id
        producto_nombre = detalle.producto.nombre

        if orden_id not in data:
            data[orden_id] = set()

        data[orden_id].add(producto_nombre)

    return list(data.values())

def preparar_dataframe(lista_ordenes):
    all_items = set()
    for productos in lista_ordenes:
        all_items.update(productos)

    all_items = list(all_items)

    encoded_vals = []

    for productos in lista_ordenes:
        row = {}
        for item in all_items:
            row[item] = item in productos
        encoded_vals.append(row)

    return pd.DataFrame(encoded_vals)

def generar_reglas(df):
    frequent_itemsets = apriori(df, min_support=0.2, use_colnames=True)
    rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1)

    return rules
