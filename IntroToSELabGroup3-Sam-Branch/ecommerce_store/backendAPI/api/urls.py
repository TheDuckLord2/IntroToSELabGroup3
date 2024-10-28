from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .models import Inventory
from .views import UserCreationView
from .views import InventoryView
from .views import StaticDataView

router = DefaultRouter()
router.register(r'users', UserCreationView)
router.register(r'inventories', InventoryView)

urlpatterns = [
    path('', include(router.urls)),
    path('data/', StaticDataView.as_view(), name='html_data'),
]