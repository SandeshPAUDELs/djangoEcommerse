from typing import Any
from django import views
from django.contrib.auth import authenticate, login, logout
from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, FormView

from ecomapp.forms import CheckoutForm, CustomerLoginForm, CustomerRegistrationForm
from .models import *
from django.views.generic import DetailView
# Create your views here.


class EcomMixin(object):
    def dispatch(self, request, *args, **kwargs):
        cart_id = request.session.get('cart_id', None)
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            if request.user.is_authenticated and hasattr(request.user, 'customer'):
                cart_obj.customer = request.user.customer
                cart_obj.save()
        return super().dispatch(request, *args, **kwargs)
    
class HomeView(EcomMixin, TemplateView):
    template_name = 'home.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['myname'] = "Sandesh Paudel"
        context['product_list'] = Product.objects.all().order_by("-id")
        # context['allcategories'] = Category.objects.all()
        return context 

class AboutView(EcomMixin, TemplateView):
    template_name = 'about.html'


class ProdutDetails(EcomMixin, TemplateView):
    template_name = 'product_details.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        url_slug = self.kwargs['slug']
        product = Product.objects.get(slug=url_slug)
        product.view_count += 1
        product.save()
        context['product'] = product
        return context 
   

class AllProducts(EcomMixin, TemplateView):
    template_name = 'allProducts.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['allcategories'] = Category.objects.all()
        return context


class AddToCart(EcomMixin, TemplateView):
    template_name = 'addtocart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #  get product id from requested url
        product_id = self.kwargs['pro_id']
        # get product
        product_obj = Product.objects.get(id=product_id)

        # check if cart exists
        cart_id = self.request.session.get('cart_id', None)
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            this_product_in_cart = cart_obj.cartproduct_set.filter(product=product_obj)

            # items already exists in the cart
            if this_product_in_cart.exists():
                cartproduct = this_product_in_cart.last()
                cartproduct.quantity += 1
                cartproduct.subtotal += product_obj.selling_price
                cartproduct.save()
                cart_obj.total += product_obj.selling_price
                cart_obj.save()
            # new items
            else:
                cartproduct = CartProduct.objects.create(cart=cart_obj, product=product_obj, rate=product_obj.selling_price, quantity=1, subtotal=product_obj.selling_price)
                cart_obj.total += product_obj.selling_price
                cart_obj.save()

        else:
            cart_obj = Cart.objects.create(total=0)
            self.request.session['cart_id'] = cart_obj.id
            cartproduct = CartProduct.objects.create(cart=cart_obj, product=product_obj, rate=product_obj.selling_price, quantity=1, subtotal=product_obj.selling_price)
            cart_obj.total += product_obj.selling_price
            cart_obj.save()

        return context


class MyCart(EcomMixin, TemplateView):
    template_name = 'my_cart.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_id = self.request.session.get('cart_id', None)
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
            context['cart'] = cart
        return context
    

class ManageCartView(EcomMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        cp_id = self.kwargs['cp_id']
        action = request.GET.get('action')
        cp_obj = CartProduct.objects.get(id=cp_id)

        cart_obj = cp_obj.cart
        # cart1 = cp_obj.cart
        # card_id = request.session.get('cart_id', None)
        # if card_id:
        #     cart2 = Cart.objects.get(id=card_id)
        #     if cart1 == cart2:
        #         return redirect('ecomapp:mycart')
        # else:
        #     return redirect('ecomapp:mycart')
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
        return redirect('ecomapp:mycart')

class EmptyCart(EcomMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        cart_id = request.session.get('cart_id', None)
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
            cart.cartproduct_set.all().delete()
            cart.total = 0
            cart.save()
        return redirect('ecomapp:mycart')
    

class CheckOut(EcomMixin, CreateView):
        template_name = 'checkout.html'
        form_class = CheckoutForm
        success_url = reverse_lazy('ecomapp:home')
        
        def dispatch(self, request, *args, **kwargs):
            if request.user.is_authenticated and hasattr(request.user, 'customer'):
                return super().dispatch(request, *args, **kwargs)
            else:
                return redirect('/login/?next=/checkout/')

        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            cart_id = self.request.session.get('cart_id', None)
            if cart_id:
                cart_obj = Cart.objects.get(id=cart_id)
                context['cart'] = cart_obj
            return context
        
        def form_valid(self, form):
            cart_id = self.request.session.get('cart_id')
            if cart_id:
                cart_obj = Cart.objects.get(id=cart_id)
                form.instance.cart = cart_obj
                form.instance.subTotal = cart_obj.total
                form.instance.discount = 0
                form.instance.total = cart_obj.total
                form.instance.order_status = "Order Received"
                del self.request.session['cart_id']
            else:
                return redirect('ecomapp:home')
            return super().form_valid(form)
    

class ContactUs(EcomMixin, TemplateView):
    template_name = 'contactus.html'

class CustomerOrder(DetailView):
    template_name = 'customer_order.html'
    model = Order
    context_object_name = 'ord_obj'
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if request.user.is_authenticated and request.user.customer:
            order_id = self.kwargs['pk']
            order = Order.objects.get(id=order_id)
            if request.user.customer != order.cart.customer:
                return redirect('/profile/')
        else:
            return redirect('/login/?next=/profile/')
        return super().dispatch(request, *args, **kwargs)




class CustomerLogin(FormView):
    template_name = 'customer_login.html'
    form_class = CustomerLoginForm
    success_url = reverse_lazy('ecomapp:home')
    def form_valid(self, form):
        uname = form.cleaned_data.get('username')
        pword = form.cleaned_data.get('password')
        usr = authenticate(username=uname, password=pword)
        # if usr is not None and usr.customer:
        if usr is not None and hasattr(usr, 'customer'):

            login(self.request, usr)
        else:
            return render(self.request, self.template_name, {'form': self.form_class, 'error': 'Username or Password is incorrect'})
        return super().form_valid(form)
    def get_success_url(self):
        if 'next' in self.request.GET:
            next_url = self.request.GET.get('next')
            return next_url
        else:
            return self.success_url


class CustomerProfile(TemplateView):
    template_name = 'customer_profile.html'
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if request.user.is_authenticated and request.user.customer:
            pass
        else:
            return redirect('/login/?next=/profile/')
        return super().dispatch(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customer = self.request.user.customer
        context['customer'] = customer
        orders = Order.objects.filter(cart__customer=customer).order_by('-id')
        context['orders'] = orders
        return context

# from django.contrib.auth.models import User

class CustomerRegistration(CreateView):
    template_name = 'customerRegistration.html'
    form_class = CustomerRegistrationForm
    success_url = reverse_lazy('ecomapp:home')

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        email = form.cleaned_data.get('email')
        
        if not username:
            # If username is not provided, handle it accordingly
            form.add_error('username', 'Username must be set')
            return self.form_invalid(form)
        
        # Check if the username already exists
        if User.objects.filter(username=username).exists():
            # Handle the case when the username already exists
            form.add_error('username', 'Username already exists')
            return self.form_invalid(form)
        
        user = User.objects.create_user(username, email, password)
        form.instance.user = user
        return super().form_valid(form)
class CustomerLogout(views.View):
    def get(self, request):
        logout(request)
        return redirect('ecomapp:home')
    


class Home(EcomMixin, TemplateView):
    template_name = 'home.html'


 
class Search(EcomMixin, TemplateView):
    template_name = 'search.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        kw = self.request.GET.get('keyword')
        results = Product.objects.filter(title__icontains=kw)
        context['results'] = results
        
        return context
    

class PasswordReset(TemplateView):
    template_name = 'password_reset.html'



class ForgetPassword(TemplateView):
    template_name = 'forget_password.html'

