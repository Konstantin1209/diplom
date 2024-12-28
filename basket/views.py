import logging


from basket.models import Cart, CartProduct
from basket.serializers import CartProductSerializer, CartSerializer
from products.models import ProductInfo
from customers_suppliers.models import Customer
from rest_framework import viewsets




logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S', filename='load_data.log')
logger = logging.getLogger('basket')




class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    filterset_fields = ['id', 'products']
    
    
class CartProductViewSet(viewsets.ModelViewSet):
    queryset = CartProduct.objects.all()
    serializer_class = CartProductSerializer
    filterset_fields = ['id', 'cart', 'product_info']
    



 
