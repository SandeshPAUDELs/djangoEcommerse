from django.contrib import admin
from .models import Cart, CartProduct, Category, Order, Product

# Register your models here.

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CartProduct)
admin.site.register(Order)