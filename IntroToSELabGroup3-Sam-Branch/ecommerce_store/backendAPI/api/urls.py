from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .models import Inventory
from .views import UserCreationView
from .views import InventoryView
from .views import StaticDataView
from .views import RegisterView
from .views import gethome
from . import views

router = DefaultRouter()
router.register(r'users', UserCreationView)
router.register(r'inventories', InventoryView)
router.register(r'register', RegisterView)
#router.register(r'home', gethome)

urlpatterns = [
    path('', include(router.urls)),
    path('data/', StaticDataView.as_view(), name='html_data'),
    path('home/', views.gethome, name='home'),
    path('contact/', views.getcontact, name='contact'),
]
