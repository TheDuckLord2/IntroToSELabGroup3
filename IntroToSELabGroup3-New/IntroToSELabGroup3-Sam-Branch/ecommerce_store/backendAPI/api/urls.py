from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .models import Cart, User
from .views import RegisterView
from .views import CartView
from .views import OrderViewSet
from .views import StaticDataView
from .views import LoginView
from .views import gethome
from . import views, admin

from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse
from django.views import View

router = DefaultRouter()
#router.register(r'users', UserCreationView) #this is sign up
#router.register(r'cart', CartView, basename = 'cart') #this is cart
#router.register(r'products', ProductViewSet) #Products view
#router.register(r'register', RegisterView) #this is login


urlpatterns = [
    path('', include(router.urls)),
    path('data/', StaticDataView.as_view(), name='html_data'),
    path('home/', views.gethome, name='home'),
    path('contact/', views.getcontact, name='contact'),
    path('about/', views.getabout, name='about'),
    path('admin/', views.getadmin, name='admin'),
    path('base/', views.getbase, name='base'),
    path('cart/', views.getcart, name='cart_html'),  # Render the cart HTML page
    path('api/cart/', CartView.as_view({'get': 'list'}), name='cart_api'),
    path('register/', RegisterView.as_view(), name='register'),
    path('product/', views.getproduct, name='product'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LoginView.as_view(), name='logout'),
    path('api/', include(router.urls)),
]
