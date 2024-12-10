from django.urls import include, path
from . import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'category', views.CategoryViewSet)
router.register(r'product', views.ProductViewSet)
router.register(r'product_info', views.ProductInfoViewSet)

urlpatterns = [
    path(r'api/v1/', include(router.urls)),
]