from django.shortcuts import redirect, render

from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from ecomapp1.forms import CheckoutForm
from ecomapp1.models import Category, Order, Product, Cart, CartProduct
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

def index(request):
    product_list = Product.objects.all()
    return render(request, 'index.html', {'product_list': product_list})


def search(request):
    if request.method == 'GET':
        keyword = request.GET.get('keyword')
        results = Product.objects.filter(title__icontains=keyword)
        return render(request, 'search.html', {'results': results})
    

def categories(request):
    allcategories = Category.objects.all()
    products = Product.objects.all()  # Fetch all products
    return render(request, 'categories.html', {'allcategories': allcategories, 'products': products})

def product_details(request, slug):
    product = Product.objects.get(slug=slug)
    product.view_count += 1
    product.save()
    return render(request, 'product_details.html', {'product': product})


@login_required(login_url='loginPage')
def addtocart(request, pro_id):
    # get product by id from url
    product = Product.objects.get(id=pro_id)

    # check if user is authenticated
    if not request.user.is_authenticated:
        return render(request, 'login.html', {'message': 'Please login to add products to cart.'})

    # check if cart exists
    cart_id = request.session.get('cart_id', None)
    if cart_id:
        cart_obj = Cart.objects.get(id=cart_id)
        this_product_in_cart = cart_obj.cartproduct_set.filter(product=product)

        # items already exists in the cart
        if this_product_in_cart.exists():
            cartproduct = this_product_in_cart.last()
            cartproduct.quantity += 1
            cartproduct.subtotal += product.selling_price
            cartproduct.save()
            cart_obj.total += product.selling_price
            cart_obj.save()
        # new items
        else:
            cartproduct = CartProduct.objects.create(cart=cart_obj, product=product, rate=product.selling_price, quantity=1, subtotal=product.selling_price)
            cart_obj.total += product.selling_price
            cart_obj.save()

    else:
        cart_obj = Cart.objects.create(total=0)
        request.session['cart_id'] = cart_obj.id
        cartproduct = CartProduct.objects.create(cart=cart_obj, product=product, rate=product.selling_price, quantity=1, subtotal=product.selling_price)
        cart_obj.total += product.selling_price
        cart_obj.save()

    return render(request, 'addtocart.html', {'product': product})


# @login_required(login_url='loginPage')
def mycart(request):
    if request.user.is_authenticated:
        cart_id = request.session.get('cart_id', None)
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
            return render(request, 'mycart.html', {'cart': cart})
        else:
            return render(request, 'mycart.html')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                cart_id = request.session.get('cart_id', None)
                if cart_id:
                    cart = Cart.objects.get(id=cart_id)
                    return render(request, 'mycart.html', {'cart': cart})
                else:
                    return render(request, 'mycart.html')
            else:
                return render(request, 'login.html', {'message': 'Invalid username or password.'})
        else:
            return render(request, 'login.html', {'message': 'Please login to view products in cart.'})
    


def managecart(request, cp_id):
    action = request.GET.get('action')
    cp_obj = CartProduct.objects.get(id=cp_id)

    cart_obj = cp_obj.cart
    if action == "inc":
        cp_obj.quantity += 1
        cp_obj.subtotal += cp_obj.rate
        cp_obj.save()
        cart_obj.total += cp_obj.rate
        cart_obj.save() 
    elif action == "dcr":
        cp_obj.quantity -= 1
        cp_obj.subtotal -= cp_obj.rate
        cp_obj.save()
        cart_obj.total -= cp_obj.rate
        cart_obj.save()
        if cp_obj.quantity == 0:
            cp_obj.delete()
    elif action == "rmv":
        cart_obj.total -= cp_obj.subtotal
        cart_obj.save()
        cp_obj.delete()
    else:
        pass
    return render(request, 'mycart.html', {'cart': cart_obj})


def emptycart(request):
    cart_id = request.session.get('cart_id', None)
    if cart_id:
        cart = Cart.objects.get(id=cart_id)
        cart.cartproduct_set.all().delete()
        cart.total = 0
        cart.save()
    return render(request, 'mycart.html')





@login_required
def checkout(request):
    user = request.user
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            cart_id = request.session.get('cart_id')
            if cart_id:
                cart_obj = Cart.objects.get(id=cart_id)
                form.instance.cart = cart_obj
                form.instance.ordered_by = user
                form.instance.subTotal = cart_obj.total
                form.instance.discount = 0
                form.instance.total = cart_obj.total
                form.instance.order_status = "Order Pending"
                del request.session['cart_id']
                form.save()
                message = "Your order has been placed."
                product_list = Product.objects.all()
                return render(request, 'index.html', {'product_list': product_list, 'message': message})
            else:
                return redirect('home')
    else:
        form = CheckoutForm()

    cart_id = request.session.get('cart_id', None)
    if cart_id:
        cart_obj = Cart.objects.get(id=cart_id)
    else:
        cart_obj = None

    if not request.user.is_authenticated:
        return redirect('/login/?next=/checkout/')

    context = {'form': form}
    if cart_obj:
        context['cart'] = cart_obj

    return render(request, 'checkout.html', context)

        


def profile(request):
    if request.user.is_authenticated:
        user = request.user
        orders = Order.objects.filter(ordered_by=user).order_by('-id')
        return render(request, 'my_profile.html', {'user': user, 'orders': orders})
    else:
        return redirect('/login/?next=/profile/')


def all_orders(request):
    orders = Order.objects.all().order_by('-id')
    return render(request, 'ddmin_pages/orderspage.html', {'orders': orders})
