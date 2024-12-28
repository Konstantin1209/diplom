from rest_framework import serializers

from basket.models import Cart, CartProduct





class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['id', 'customer', 'products', 'update_total_amount']
        
        
class CartProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartProduct
        fields = ['cart', 'product', 'quantity', 'supplier']
        