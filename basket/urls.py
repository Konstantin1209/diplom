from django.urls import path, include
from rest_framework.routers import DefaultRouter

from basket.views import CartProductViewSet, CartViewSet



router = DefaultRouter()
router.register(r'cart', CartViewSet)
router.register(r'cart-product', CartProductViewSet)

urlpatterns = [
    path(r'api/v1/', include(router.urls)),
]