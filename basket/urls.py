from django.urls import path, include
from rest_framework.routers import DefaultRouter



router = DefaultRouter()


urlpatterns = [
    path(r'api/v1/', include(router.urls)),
]