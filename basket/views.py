import logging
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse

from basket.serializers import CartItemSerializer, CartSerializer
from .models import Cart, CartItem
from customers_suppliers.models import Customer
from rest_framework import viewsets




logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S', filename='load_data.log')
logger = logging.getLogger('basket')



class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    filterset_fields = ['id', 'customer', 'created_at', 'total_amount', 'items']
    
    
class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    filterset_fields = fields = ['id', 'product_info']