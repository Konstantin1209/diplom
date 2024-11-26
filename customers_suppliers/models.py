from django.contrib.auth.models import AbstractUser, User
from django.db import models


class CustomUser (AbstractUser ):
    email = models.EmailField(unique=True)
    is_customer = models.BooleanField(default=False)
    is_supplier = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f"{self.username} ({self.email})"


class Customer(models.Model):
    user = models.OneToOneField(CustomUser , related_name='customer', on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} (Клиент)"


class Supplier(models.Model):
    user = models.OneToOneField(CustomUser , related_name='supplier', on_delete=models.CASCADE)
    contact_person = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} (Поставщик)"
    
    
