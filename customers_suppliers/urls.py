from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.user_list, name='user_list'),
    path('users/<int:id>/', views.user_id, name='user_list'),
    path('user/create/', views.create_user, name='create_user'),
]