
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers

from ecomapp1 import views

# from authentication import views
from ecomapp1.views import ProductViewSet, CategoryViewSet
# from authentication.views import RegisterUserViewSet, ObtainAuthTokenViewSet
# router = routers.DefaultRouter()
# router.register(r'login1',  ObtainAuthTokenViewSet.as_view({'post': 'create'}))
# router.register(r'register1', RegisterUserViewSet.as_view({'post': 'create'}))

# router.register(r'products', ProductViewSet)
# router.register(r'categories', CategoryViewSet)
# router.register(r'cart', views.CartViewSet)
# router.register(r'cartproduct', views.CartProductViewSet)
# router.register(r'order', views.OrderViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', include('ecomapp.urls')),
    path('', include('authentication.urls')),
    path('', include('ecomapp1.urls')),
    # path('api/', include(router.urls))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)