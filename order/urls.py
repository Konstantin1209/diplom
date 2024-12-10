from django.urls import include, path
from . import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()


urlpatterns = [
    path(r'api/v1/', include(router.urls)),
]