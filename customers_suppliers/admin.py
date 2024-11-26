from django.contrib import admin

from customers_suppliers.models import CustomUser, Customer, Supplier



@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'is_customer', 'is_supplier']
    list_filter = ['id', 'email']
    
    
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'phone_number']
    list_filter = ['id']

  
@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'contact_person']
    list_filter = ['id'] 


