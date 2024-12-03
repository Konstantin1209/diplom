from django import forms
from .models import CustomUser, Customer, Supplier
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm



class CustomerRegistrationForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ('phone_number',)
        

class CustomUserCreationForm(UserCreationForm): 
    class Meta:
        model = CustomUser
        fields = ('username','user_type', 'email', 'password1', 'password2')
    
    
        
        


