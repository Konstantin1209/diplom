from django.db import models
from customers_suppliers.models import Customer, Supplier
from products.models import ProductInfo

class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='carts', verbose_name='Покупатель')
    products = models.ManyToManyField(ProductInfo, related_name='carts', verbose_name='Товар', through='CartProduct')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'
    
    def __str__(self):
        return f'Корзина пользователя: id-{self.id} - {self.customer}'
    
    def update_total_amount(self):
        self.total_amount = sum(item.product.price * item.quantity for item in self.cart_products.all())
        self.save()


class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_products', verbose_name='Корзина')
    product = models.ForeignKey(ProductInfo, on_delete=models.CASCADE, related_name='cart_products', verbose_name='Товар')
    quantity = models.IntegerField(default=1, verbose_name='Количество')
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, verbose_name='Поставщик')

    class Meta:
        unique_together = ('cart', 'product')  
        verbose_name = 'Товар в корзине'
        verbose_name_plural = 'Товары в корзине'

    def save(self, *args, **kwargs):
        """Переопределение метода save для проверки количества."""
        if self.quantity <= 0:
            raise ValueError("Количество должно быть положительным.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.product} (Количество: {self.quantity}) в корзине {self.cart}'