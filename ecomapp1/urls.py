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
]