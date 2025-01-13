import logging
from rest_framework import serializers

from basket.models import Cart, CartProduct



logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S', filename='load_data.log')
logger = logging.getLogger('basket')



class CartSerializer(serializers.ModelSerializer):
    total_amount = serializers.SerializerMethodField()
    
    class Meta:
        model = Cart
        fields = ['id', 'customer', 'products', 'total_amount', 'cart_type', 'adress', 'created_at', 'updated_at']
        
    def get_total_amount(self, obj):
        try:
            return obj.update_total_amount()
        except Exception as e:
            logger.error(f"Ошибка при обновлении общей суммы: {e}")
            return None
        
        
class CartProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartProduct
        fields = ['cart', 'product', 'quantity', 'supplier']
        