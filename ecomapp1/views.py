from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from ecomapp1.models import Category, Product, Cart, CartProduct
from django.shortcuts import render

@login_required(login_url='loginPage')
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
    return render(request, 'categories.html', {'allcategories': allcategories})

def product_details(request, slug):
    product = Product.objects.get(slug=slug)
    product.view_count += 1
    product.save()
    return render(request, 'product_details.html', {'product': product})



def addtocart(request, pro_id):
    # get product by id from url
    product = Product.objects.get(id=pro_id)

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


def mycart(request):
    cart_id = request.session.get('cart_id', None)
    if cart_id:
        cart = Cart.objects.get(id=cart_id)
        return render(request, 'mycart.html', {'cart': cart})
    else:
        return render(request, 'mycart.html')

