from .models import Cart, CartProduct, Order, Product, Category
from rest_framework import serializers

class ProductSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Product
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    category_id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Category
        fields = '__all__'

class CartSerializer(serializers.ModelSerializer):
    cart_id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Cart
        fields = '__all__'

class CardProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    cart = CartSerializer()
    class Meta:
        model = CartProduct
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    cart = CartSerializer()
    class Meta:
        model = Order
        fields = '__all__'





        







