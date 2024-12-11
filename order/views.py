from django.shortcuts import render
from rest_framework import viewsets

from order.models import Category, Parameter, Product, ProductInfo, ProductParameter
from order.serializers import CategorySerializer, ParameterSerializer, ProductInfoSerializer, ProductParameterSerializer, ProductSerializer



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


class ParameterViewSet(viewsets.ModelViewSet):
    queryset = Parameter.objects.all()
    serializer_class = ParameterSerializer
    filterset_fields = ['id', 'name']
    

class ProductParameterViewSet(viewsets.ModelViewSet):
    queryset = ProductParameter.objects.all()
    serializer_class = ProductParameterSerializer
    filterset_fields = ['id', 'product_info', 'parameter', 'value']