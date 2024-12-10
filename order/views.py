from django.shortcuts import render
from rest_framework import viewsets

from order.models import Category, Product, ProductInfo
from order.serializers import CategorySerializer, ProductInfoSerializer, ProductSerializer



class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filterset_fields = ['id' 'name', 'shops']
    

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filterset_fields = ['id', 'name', 'category']
    

class ProductInfoViewSet(viewsets.ModelViewSet):
    queryset = ProductInfo.objects.all()
    serializer_class = ProductInfoSerializer
    filterset_fields = ['id', 'model', 'external_id', 'product', 'shop', 'quantity', 'price', 'price_rrc']
