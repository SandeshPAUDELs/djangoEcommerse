from django.contrib import admin
from django.urls import include, path

from ecomapp1 import views

urlpatterns = [
    path('', views.index, name='home'),
    path('search/', views.search, name='search'),
    path('categories/', views.categories, name='categories'),
    path('product/<slug:slug>/', views.product_details, name='product_details'),
    path('addtocart/<int:pro_id>/', views.addtocart, name='addtocart'),
    path('mycart/', views.mycart, name='mycart'),
    path('managecart/<int:cp_id>/', views.managecart, name='managecart'),
    path('emptycart/', views.emptycart, name='emptycart'),
    path('checkout/', views.checkout, name='checkout'),
    path('profile/', views.profile, name='profile'),
    path('all_orders/', views.all_orders, name='all_orders'),
    # path('khalti_integration/', views.khalti_intergration, name='khalti_integration')
    path('initiate',views.initkhalti,name="initiate"),
    path('verify',views.verifyKhalti,name="verify")




]