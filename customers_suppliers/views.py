from django.http import HttpResponse
from django.shortcuts import render
from .models import CustomUser
from .serializers import CustomUserSerializer, CustomerSerializers, SupplierSerializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from .models import Customer, Supplier
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import PermissionDenied



class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    filterset_fields = ['id', 'username', 'email', 'user_type']
    
    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
    def retrieve(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        if str(request.user.id) != str(user_id):
            raise PermissionDenied ('Вы не можете просматривать данные других пользователей.')
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
            

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializers
    

class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializers





    
    
    
        




