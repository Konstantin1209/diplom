from django.http import HttpResponse
from django.shortcuts import render
from .models import CustomUser
from .serializers import CustomUserSerializer, CustomerSerializers, SupplierSerializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from .models import Customer, Supplier
from .forms import CustomUserCreationForm, CustomerRegistrationForm



def register(request):
    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST)
        customer_form = CustomerRegistrationForm(request.POST)
        
        if user_form.is_valid() and customer_form.is_valid():
            user = user_form.save()
            customer = customer_form.save(commit=False)
            customer.user = user
            customer.save()
            return HttpResponse('Покупатель успешно создан')
    else:
        user_form = CustomUserCreationForm()
        customer_form = CustomerRegistrationForm()

    return render(request, 'register.html', {
        'user_form': user_form,
        'customer_form': customer_form   
    })

class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    filterset_fields = ['id', 'username', 'email', 'user_type']
    

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializers
    

class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializers





    
    
    
        




