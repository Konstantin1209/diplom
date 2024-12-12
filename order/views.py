import json
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from customers_suppliers.models import Supplier
from order.models import Category, Parameter, Product, ProductInfo, ProductParameter
from order.serializers import CategorySerializer, ParameterSerializer, ProductInfoSerializer, ProductParameterSerializer, ProductSerializer
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
        # logging.info("Allowed actions: %s", allowed_actions)
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
            supplier = product_info_instance.shop
            if supplier.user == self.request.user:
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
    
    
    
    
        
    
# try:
#     product_info_instance = ProductInfo.objects.get(id=product_id)  # Получаем объект по id
#     supplier = product_info_instance.shop  # Получаем связанный объект Supplier

#     if supplier.user == request.user:  # Проверяем, является ли текущий пользователь владельцем магазина
#         logging.info("Вы являетесь создателем этого объекта ProductInfo через магазин.")
#     else:
#         logging.info("Вы не являетесь создателем этого объекта ProductInfo.")
# except ProductInfo.DoesNotExist:
#     logging.warning(f'ProductInfo с id {product_id} не найден.')             
            
                
    
    
    
    # def check_admin_permission(self, allowed_actions=None):
    #     if allowed_actions is None:
    #         allowed_actions = []
    #     if self.request.user.is_staff:
    #         return [AllowAny()]
    #     if self.action in allowed_actions:
    #         return [AllowAny()]
    #     if self.request.user.is_authenticated:
    #         if self.request.user.user_type == 'customer':
    #             if self.action in allowed_actions:
    #                 return [AllowAny()]
    #             else:
    #                 raise PermissionDenied("У вас нет разрешения на это действие.")
    #         if self.request.user.user_type == 'supplier':
    #             if self.action == 'create':
    #                 return [AllowAny()]
    #             product_info_id = self.kwargs.get('pk')
    #             product_info = ProductInfo.objects.get(id=product_info_id)
    #             if product_info.shop.owner == self.request.user:
    #                 return [AllowAny()]     
    #     return [IsAuthenticated()]
    
    # def check_admin_permission(self):
    #     logging.info(self.request.user)
    #     product_info_instance = ProductInfo.objects.get(id=5)
    #     supplier = product_info_instance.shop 
    #     logging.info(product_info_instance)
    #     logging.info(supplier)
    #     logging.info(supplier.user)
        
        
        
    #     if self.request.user.is_staff:
    #         return [AllowAny()]
    #     if self.action in self.allowed_actions_permission():
    #         return [AllowAny()]
    #     if self.request.user.is_authenticated:
    #         if self.request.user.user_type == 'customer':
    #             if self.action in self.allowed_actions_permission():
    #                 return [AllowAny()]
    #             else:
    #                 raise PermissionDenied("Нет прав.")
    #         if self.request.user.user_type == 'supplier':
    #             if self.action == 'create':
    #                 return [AllowAny()]
    #             if self.shop.user == self.request.user:
    #                 return [AllowAny()]
    #     return [IsAuthenticated()]
                    
    # def allowed_actions_permission(self, allowed_actions=None):
    #     if allowed_actions is None:
    #         allowed_actions = ['list', 'retrieve']
    #     logging.info("Allowed actions: %s", allowed_actions)
    #     return allowed_actions


class CategoryViewSet(PerrmissionMixin, viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filterset_fields = ['id', 'name']
    
    def get_permissions(self):
        logging.info(f' разрешенные методы: {self.allowed_actions_permission()}')
        logging.info(f' Является ли покупателем: {self.check_user_type_mixin('customer')}')
        logging.info(f' Является ли поставщиком: {self.check_user_type_mixin('supplier')}')
        logging.info(f' Является ли админом: {self.check_admin_mixin()}')
        logging.info(f' Кем является: {self.request.user}, метод: {self.action}')
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
    serializer_class = ProductInfoSerializer
    filterset_fields = ['id', 'model', 'external_id', 'product', 'shop', 'quantity', 'price', 'price_rrc']

    def get_permissions(self):
        if self.check_admin_mixin():
            return [AllowAny()]
        if self.check_user_type_mixin('supplier'):
            if self.check_creator_mixin(self, self.product_id):
                return [AllowAny()]
        if self.allowed_actions_permission():
            return [AllowAny()]
        raise PermissionDenied("Нет прав.")
            
        
        


class ParameterViewSet(PerrmissionMixin, viewsets.ModelViewSet):
    queryset = Parameter.objects.all()
    serializer_class = ParameterSerializer
    filterset_fields = ['id', 'name']
    
    

class ProductParameterViewSet(PerrmissionMixin, viewsets.ModelViewSet):
    queryset = ProductParameter.objects.all()
    serializer_class = ProductParameterSerializer
    filterset_fields = ['id', 'product_info', 'parameter', 'value']
    
