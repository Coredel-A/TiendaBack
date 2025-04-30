from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrdenViewSet, create_payment_intent, obtener_sugerencias

router = DefaultRouter()
router.register(r'', OrdenViewSet, basename='orden')

urlpatterns = [
    path('create-payment-intent/', create_payment_intent, name='create-payment-intent'),
    path('sugerencias/', obtener_sugerencias, name='sugerencias'),
]

urlpatterns += router.urls