from django.contrib import admin

from basket.models import Cart, CartItem

# Register your models here.


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    pass


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    pass