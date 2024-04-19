from django.contrib import admin
from django.urls import include, path

from ecomapp1 import views

urlpatterns = [
    path('', views.index, name='home'),
]