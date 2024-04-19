from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission



class Customer(AbstractUser):
    profile_pic = models.ImageField(upload_to="profile_pics", default="profile_pics/default.png")
    full_name = models.CharField(max_length=200)    
    address = models.TextField()

    # Redefine the relationships with unique related_name arguments
    groups = models.ManyToManyField(Group, related_name='customer_set')
    user_permissions = models.ManyToManyField(Permission, related_name='customer_set')

    def __str__(self):
        return self.full_name



class Category(models.Model):
    title = models.CharField(max_length = 200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title

class Product(models.Model):
    title = models.CharField(max_length = 200)
    slug = models.SlugField(unique = True)
    category = models.ForeignKey(Category, on_delete = models.CASCADE)
    image = models.ImageField(upload_to="products")
    # image = models.ImageField(upload_to="products", default="data:image/jpeg;base64,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")
    marked_price = models.PositiveIntegerField()
    selling_price = models.PositiveIntegerField()
    description = models.TextField()
    warranty = models.CharField(max_length=300, null = True, blank = True)
    return_policy = models.CharField(max_length = 300, null = True, blank = True)
    view_count = models.PositiveIntegerField(default = 0)

    def __str__(self):
        return self.title
    
class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null = True, blank = True)
    total = models.PositiveIntegerField(default = 0)
    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return "Cart: " + str(self.id)
    

class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rate = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    subtotal = models.PositiveIntegerField()

    def __str__(self):
        return "Cart: " + str(self.cart.id) + "CartProduct: " + str(self.id)
    

ORDER_STATUS =  {
    ("Order Received", "Order Received"),
    ("Order pending", "Order Pending"),
    ("On the way", "On the way"),
    ("Order Completed", "Order Completed"),
    ("Order Cancelled", "Order Cancelled")

}

class Order(models.Model):  
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
    ordered_by = models.CharField(max_length=200)
    shipping_address = models.CharField(max_length=200)
    mobile = models.CharField(max_length=10)
    email = models.EmailField(null=True, blank=True)
    subTotal = models.PositiveIntegerField()
    discount = models.PositiveIntegerField()
    total = models.PositiveIntegerField()
    order_status = models.CharField(max_length = 50, choices=ORDER_STATUS)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Order: " + str(self.id)
    

