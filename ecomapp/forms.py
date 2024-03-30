from django import forms
from .models import Customer, Order


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['ordered_by', 'shipping_address', 'mobile', 'email']

class CustomerRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    username = forms.CharField(widget=forms.TextInput())
    class Meta:
        model = Customer
        fields = ['full_name', 'address', 'password', 'username']