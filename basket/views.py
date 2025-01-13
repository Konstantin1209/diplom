import logging


from basket.models import Cart, CartProduct
from basket.serializers import CartProductSerializer, CartSerializer
from products.models import ProductInfo
from customers_suppliers.models import Customer
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.response import Response




logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S', filename='load_data.log')
logger = logging.getLogger('basket')




class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    filterset_fields = ['id', 'products']
    
    def list(self, request, *args, **kwargs):
        if self.request.user.is_staff:
            logger.info('Администратор')
            carts = Cart.objects.all()
            serializer = self.get_serializer(carts, many=True)  
            return Response(serializer.data)
        if not self.request.user.is_authenticated:
            logger.info('Аноним')
            raise PermissionDenied("Нет прав.")
        serializer = self.get_serializer(request.user)
        logger.info(request.user)
        return Response(serializer.data)
        
                
            
        
    
    
class CartProductViewSet(viewsets.ModelViewSet):
    queryset = CartProduct.objects.all()
    serializer_class = CartProductSerializer
    filterset_fields = ['id', 'cart', 'product_info']
    



 
