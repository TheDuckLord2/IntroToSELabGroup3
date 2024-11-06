from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .models import Cart
from .views import UserCreationView
from .views import CartView
from .views import StaticDataView
from .views import RegisterView
from .views import gethome
from . import views, admin

router = DefaultRouter()
router.register(r'users', UserCreationView) #this is sign up
router.register(r'cart', CartView) #this is cart
router.register(r'register', RegisterView) #this is login

urlpatterns = [
    path('', include(router.urls)),
    path('data/', StaticDataView.as_view(), name='html_data'),
    path('home/', views.gethome, name='home'),
    path('contact/', views.getcontact, name='contact'),
    path('about/', views.getabout, name='about'),
    path('admin/', views.getadmin, name='admin'),
    path('base/', views.getbase, name='base'),
    path('cart/', views.getcart, name='cart'),
    path('login/', views.getlogin, name='login'),
    path('product/', views.getproduct, name='product'),
]
