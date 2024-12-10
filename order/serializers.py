from rest_framework import serializers
from .models import Category, Product, ProductInfo, Parameter, ProductParameter




class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']
        

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'category']
        

class ProductInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductInfo
        fields = ['model', 'external_id', 'product', 'shop', 'quantity', 'price', 'price_rrc']


