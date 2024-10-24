from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserCreationView
from .views import StaticDataView

router = DefaultRouter()
router.register(r'users', UserCreationView)

urlpatterns = [
    path('', include(router.urls)),
    path('data/', StaticDataView.as_view(), name='html_data'),
]