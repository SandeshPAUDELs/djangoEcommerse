import json
from django.http import HttpResponse
from django.shortcuts import redirect, render
import requests

from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy
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
    

# def categories(request):
#     allcategories = Category.objects.all()
#     products = Product.objects.all()  # Fetch all products
#     return render(request, 'categories.html', {'allcategories': allcategories, 'products': products})
def categories(request):
    allcategories = Category.objects.all()
    products = Product.objects.all()

    selected_category = None
    category_slug = request.GET.get('category')  # Retrieve category from query string
    if category_slug:
        try:
            selected_category = Category.objects.get(slug=category_slug)
            products = products.filter(category=selected_category)  # Filter products based on category
        except Category.DoesNotExist:
            pass  # Handle case where category doesn't exist (optional)

    context = {'allcategories': allcategories, 'products': products, 'selected_category': selected_category}
    return render(request, 'categories.html', context)

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

    return render(request, 'addtocart.html', {'product': product, 'message': 'Item added to cart'}) 


# @login_required(login_url='loginPage')
def mycart(request):
    if request.user.is_authenticated:
        cart_id = request.session.get('cart_id', None)
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
            if cart.cartproduct_set.exists():
                return render(request, 'mycart.html', {'cart': cart})
            else:
                message = 'Please add items to your cart to see your cart.'
                return render(request, 'mycart.html', {'message': message})
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
                    if cart.cartproduct_set.exists():
                        return render(request, 'mycart.html', {'cart': cart})
                    else:
                        message = 'Please add items to your cart to see your cart.'
                        return render(request, 'mycart.html', {'message': message})
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
                # return render(request, 'index.html', {'product_list': product_list, 'message': message})
                return render(request, 'khalti_integration.html')
                # return redirect(reverse('initiate') + "? o_id=" + str(form.instance.id))
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


# below code is for khalti integration

def initkhalti(request):
    url = "https://a.khalti.com/api/v2/epayment/initiate/"

    payload = json.dumps({
        "return_url": "http://example.com/",
        "website_url": "https://example.com/",
        "amount": "1000",
        "purchase_order_id": "Order01",
        "purchase_order_name": "test",
        "customer_info": {
            "name": "Ram Bahadur",
            "email": "none@gmail.com",
            "phone": 98000001
        }
    })
    headers = {
        'Authorization': 'key live_secret_key_68791341fdd94846a146f0457ff7b455',
        'Content-Type': 'application/json',
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)
    new_res = json.loads(response.text)
    print(new_res)
    return redirect(new_res['payment_url'])
    # return HttpResponse(response.text)
    

def verifyKhalti(request):
    url = "https://a.khalti.com/api/v2/epayment/lookup/"
    if request.method == 'GET':
        headers = {
            'Authorization': 'key 054dc89c105e49ed9b707155a2cce080',
            'Content-Type': 'application/json',
        }
        pidx = request.GET.get('pidx')
        data = json.dumps({
            'pidx':pidx
        })
        res = requests.request('POST',url,headers=headers,data=data)
        print(res)
        print(res.text)

        new_res = json.loads(res.text)
        print(new_res)
        

        if new_res['status'] == 'Completed':
            # user = request.user
            # user.has_verified_dairy = True
            # user.save()
            # perform your db interaction logic
            pass
        
        # else:
        #     # give user a proper error message
        #     raise BadRequest("sorry ")

        return redirect('home')
    

    