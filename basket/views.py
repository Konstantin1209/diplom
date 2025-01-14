import logging


from basket.models import Cart, CartProduct
from basket.serializers import CartProductSerializer, CartSerializer
from products.models import ProductInfo
from customers_suppliers.models import Customer
from rest_framework import viewsets, status
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser




logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S', filename='load_data.log')
logger = logging.getLogger('basket')




def get_user_carts(user):
    try:
        carts = Cart.objects.filter(customer=user.customer)
        return carts
    except Exception as e:
        logger.error(e)
        return None


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    filterset_fields = ['id', 'products']
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        try:
            if request.user.is_staff:
                carts = Cart.objects.all()
            else:
                carts = get_user_carts(request.user)
            if carts is None:
                return Response({"error": "Корзины не найдены"}, status=status.HTTP_404_NOT_FOUND)
            serializer = self.get_serializer(carts, many=True)
            return Response(serializer.data)
        except Exception as e:
            logger.error(e)
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                
            
        
    
    
class CartProductViewSet(viewsets.ModelViewSet):
    queryset = CartProduct.objects.all()
    serializer_class = CartProductSerializer
    filterset_fields = ['id', 'cart', 'product_info']
    



 
