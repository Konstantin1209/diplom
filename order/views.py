from django.db import IntegrityError
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from customers_suppliers import serializers
from customers_suppliers.models import Supplier
from order.models import Category, Parameter, Product, ProductInfo, ProductParameter
from order.serializers import CategorySerializer, ParameterSerializer, ProductInfoCreateSerializer, ProductInfoSerializer, ProductParameterSerializer, ProductSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser 
import logging


logging.basicConfig(level=logging.INFO)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.basicConfig(filename='log.txt')

from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.exceptions import PermissionDenied


class PerrmissionMixin:
       
    def allowed_actions_permission(self, allowed_actions=None):
        if allowed_actions is None:
            allowed_actions = ['list', 'retrieve']
        return allowed_actions
    
    def check_user_type_mixin(self, user_type):
        if self.request.user.is_authenticated:
            if self.request.user.user_type == user_type:
                    return True
        return False
    
    def check_admin_mixin(self):
        if self.request.user.is_staff:
            return True
        return False
    
    def check_creator_mixin(self, product_id):
        if self.request.user.is_authenticated:
            product_info_instance = ProductInfo.objects.get(id=product_id)
            shop = product_info_instance.shop
            supplier_user = shop.user
            user_id = supplier_user.id
            logging.info(f' Магазин: {shop.id}')
            logging.info(f'Пользователь: {user_id}')
            logging.info(f' id создателя: {supplier_user.id}, id пользователя: {self.request.user.id}')
            if supplier_user.id == self.request.user.id:
                return True
        else:
            return False
    
    def get_permissions_mixin(self):
        if self.check_admin_mixin():
            logging.info(' Он админ')
            return [AllowAny()]
        if self.check_user_type_mixin('supplier'):
            logging.info(' Он продавец')
            return [AllowAny()]
        if self.check_user_type_mixin('customer'):
            if self.action in self.allowed_actions_permission():
                logging.info(' Покупатель Использует разрешенные методы')
                return [AllowAny()]
        if self.action in self.allowed_actions_permission():
            logging.info(' Аноним Использует разрешенные методы')
            return [AllowAny()]
        logging.info(' Нет прав')
        raise PermissionDenied("Нет прав.")


class CategoryViewSet(PerrmissionMixin, viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filterset_fields = ['id', 'name']
    
    def get_permissions(self):
        return self.get_permissions_mixin()
    
    
class ProductViewSet(PerrmissionMixin, viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filterset_fields = ['id', 'name', 'category']
    
    def get_permissions(self):
        logging.info(f' разрешенные методы: {self.allowed_actions_permission()}')
        logging.info(f' Является ли покупателем: {self.check_user_type_mixin('customer')}')
        logging.info(f' Является ли поставщиком: {self.check_user_type_mixin('supplier')}')
        logging.info(f' Является ли админом: {self.check_admin_mixin()}')
        logging.info(f' Кем является: {self.request.user}, метод: {self.action}')
        return self.get_permissions_mixin()
    
    
class ProductInfoViewSet(PerrmissionMixin, viewsets.ModelViewSet):
    queryset = ProductInfo.objects.all()
    filterset_fields = ['id', 'model', 'external_id', 'product', 'shop', 'quantity', 'price', 'price_rrc']
    
    def get_serializer_class(self):
        logging.info(self.action)
        
        if self.request.user.is_staff:
            return ProductInfoSerializer 
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return ProductInfoCreateSerializer
        return ProductInfoSerializer 
        

    def get_permissions(self):
        if self.check_admin_mixin():
            return [AllowAny()]
        if self.action in self.allowed_actions_permission():
            return [AllowAny()]
        if self.check_user_type_mixin('supplier'):
            if self.action in self.allowed_actions_permission():
                return [AllowAny()]
            if self.action == 'create':
                return [AllowAny()]
            product_id = self.kwargs.get('pk')
            if self.check_creator_mixin(product_id):
                return [AllowAny()]

        raise PermissionDenied("Нет прав.")
    
    def create(self, request, *args, **kwargs):
        if self.request.user.is_staff:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer) 
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        try:
            supplier = request.user.supplier
            serializer = ProductInfoCreateSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(shop=supplier) 
            serializer.save(shop=self.request.user.supplier)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except IntegrityError:
            logging.error("IntegrityError: Дублирующая запись для ProductInfo.")
            raise serializers.ValidationError("Эта информация о продукте уже существует для данного продукта и магазина.")
    
    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()  
            serializer = ProductInfoCreateSerializer(instance, data=request.data, partial=True)  
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)  
            return Response(serializer.data, status=status.HTTP_200_OK)
        except IntegrityError:
            logging.error("IntegrityError: Дублирующая запись для ProductInfo при обновлении.")
            raise serializers.ValidationError("Эта информация о продукте уже существует для данного продукта и магазина.")


class ParameterViewSet(PerrmissionMixin, viewsets.ModelViewSet):
    queryset = Parameter.objects.all()
    serializer_class = ParameterSerializer
    filterset_fields = ['id', 'name']
    
    def get_permissions(self):
        return self.get_permissions_mixin()
    

class ProductParameterViewSet(PerrmissionMixin, viewsets.ModelViewSet):
    queryset = ProductParameter.objects.all()
    serializer_class = ProductParameterSerializer
    filterset_fields = ['id', 'product_info', 'parameter', 'value']
    
    def get_permissions(self):
        logging.info(f"Пользователь {self.request.user} пытается получить доступ к действию: {self.action}")

        if self.check_admin_mixin():
            logging.info("Доступ предоставлен: пользователь является администратором.")
            return [AllowAny()]

        if self.action in self.allowed_actions_permission():
            logging.info(f"Доступ предоставлен: действие '{self.action}' разрешено.")
            return [AllowAny()]

        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            if self.check_user_type_mixin('supplier'):
                product_info = self.request.data.get('product_info')
                if self.check_creator_mixin(product_info):
                    logging.info("Доступ предоставлен: пользователь является создателем продукта.")
                    return [AllowAny()]

        logging.warning(f"Доступ отклонен: у пользователя {self.request.user} нет прав для действия '{self.action}'.")
        raise PermissionDenied("Нет прав.")
            

    
