from django.db import models

from customers_suppliers.models import Customer
from order.models import ProductInfo




class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE,related_name='customer', verbose_name='Покупатель')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Общая сумма', default=0)
    is_paid = models.BooleanField(default=False)  
    
    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'
        
    def __str__(self):
        return f'Корзина пользователя:{self.customer}'
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items', verbose_name='Корзина')
    product_info = models.ForeignKey(ProductInfo, on_delete=models.CASCADE, related_name='cart_items', verbose_name='Информация о продукте')
    quantity = models.PositiveIntegerField(verbose_name='Количество')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    
    class Meta:
        verbose_name = 'Элемент корзины'
        verbose_name_plural = 'Элементы корзины'
   
    def __str__(self):
        return f"{self.cart}: {self.product_info.product.name} - {self.quantity} шт."

    
