from django.urls import include, path
from authentication import views
# from rest_framework import routers
# router = routers.DefaultRouter()
# from authentication.views import RegisterUserViewSet, ObtainAuthTokenViewSet
# router.register(r'login',  ObtainAuthTokenViewSet)
# router.register(r'register', RegisterUserViewSet)

urlpatterns = [
    path('login/', views.loginPage, name='loginPage'),  
    path('logout/', views.logoutUser, name='logout'),  
    path('register/', views.register, name='register'),
    path('forget_password/', views.forget_password, name='forget_password'),
    path('send_otp/', views.send_otp, name='send_otp'),
    # path('api/', include(router.urls)),
    # # path('verify_otp/', views.verify_otp, name='verify_otp'),
    # path('register1/', views.RegisterUserViewSet.as_view({'post': 'create'}), name='register'),
    # path('login1/', views.ObtainAuthTokenViewSet.as_view({'post': 'create'}), name='login'),
]