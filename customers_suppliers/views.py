from django.http import HttpResponse
from django.shortcuts import render
from .models import CustomUser
from .serializers import CustomUserSerializer, CustomerSerializers, SupplierSerializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from .models import Customer, Supplier
from rest_framework.permissions import IsAuthenticated


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    filterset_fields = ['id', 'username', 'email', 'user_type']
    permission_classes = [IsAuthenticated]

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializers
    

class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializers





    
    
    
        




