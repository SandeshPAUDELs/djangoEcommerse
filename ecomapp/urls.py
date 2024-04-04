
from django.urls import path
from .views import *


app_name = "ecomapp"
urlpatterns = [

    # Client side pages
    path("", HomeView.as_view(), name="home"),
    path("about/", AboutView.as_view(), name="about"),
    path("contact-us/", ContactUs.as_view(), name="contact"),
    path("all-products/", AllProducts.as_view(), name="allproducts"),
    path("product/<slug:slug>/", ProdutDetails.as_view(), name="productdetail"),
#     here the slug works as the primary key  and with this key the product details according to product will be displayed

    path("add-to-cart-<int:pro_id>/", AddToCart.as_view(), name="addtocart"),
    path("my-cart/", MyCart.as_view(), name="mycart"),
    path("manage-cart/<int:cp_id>/", ManageCartView.as_view(), name="managecart"),
    path("empty-cart/", EmptyCart.as_view(), name="emptycart"),

    path("checkout/", CheckOut.as_view(), name="checkout"),

    path("register/",
         CustomerRegistration.as_view(), name="customerregistration"),
     path("logout/", CustomerLogout.as_view(), name="customerlogout"),

     
    path("login/", CustomerLogin.as_view(), name="customerlogin"),

    path("profile/", CustomerProfile.as_view(), name="customerprofile"),
    path("profile/order-<int:pk>/", CustomerOrder.as_view(),
         name="customerorderdetail"),

    path("search/", Search.as_view(), name="search"),

    path("forgot-password/", ForgetPassword.as_view(), name="passworforgot"),
    path("password-reset/<email>/<token>/",
         PasswordReset.as_view(), name="passwordreset"),

    
]
