from django.urls import path
from authentication import views

urlpatterns = [
    path('login/', views.loginPage, name='loginPage'),  
    path('logout/', views.logoutUser, name='logout'),  
    path('register/', views.register, name='register'),
    path('forget_password/', views.forget_password, name='forget_password'),
    path('send_otp/', views.send_otp, name='send_otp'),
    path('verify_otp/', views.verify_otp, name='verify_otp'),

]