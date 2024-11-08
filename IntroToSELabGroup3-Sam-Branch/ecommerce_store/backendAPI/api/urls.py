from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .models import Cart, CreatedUser, UserCreation
from .views import UserCreationView
from .views import CartView
from .views import StaticDataView
from .views import LoginView
from .views import gethome
from . import views, admin

router = DefaultRouter()
#router.register(r'users', UserCreationView) #this is sign up
#router.register(r'cart', CartView) #this is cart
#router.register(r'login', LoginView) #this is login
#router.register(r'register', UserCreationView)

urlpatterns = [
    path('', include(router.urls)),
    path('data/', StaticDataView.as_view(), name='html_data'),
    path('home/', views.gethome, name='home'),
    path('contact/', views.getcontact, name='contact'),
    path('about/', views.getabout, name='about'),
    path('admin/', views.getadmin, name='admin'),
    path('base/', views.getbase, name='base'),
    path('cart/', views.getcart, name='cart'),
    path('register/', views.getregister, name='register'),
    path('product/', views.getproduct, name='product'),
    path('login/', views.getlogin, name='login'),
]