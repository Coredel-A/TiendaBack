from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrdenViewSet, create_payment_intent

router = DefaultRouter()
router.register(r'', OrdenViewSet)

urlpatterns = [
    path('create-payment-intent/', create_payment_intent, name='create-payment-intent'),
]

urlpatterns += router.urls