from django import forms
from .models import Customer, Order


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['ordered_by', 'shipping_address', 'mobile', 'email']

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Customer

class CustomerRegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=100, help_text='Required. Enter a valid email address.')

    class Meta:
        model = Customer
        fields = ['full_name', 'address', 'password', 'username']

class CustomerLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())