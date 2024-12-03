from django.urls import include, path
from . import views
from rest_framework.routers import DefaultRouter
from .views import register

router = DefaultRouter()
router.register('custom_user', views.CustomUserViewSet)
router.register('customer', views.CustomerViewSet)
router.register('supplier', views.SupplierViewSet)


urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('register', register, name='register') 
]

