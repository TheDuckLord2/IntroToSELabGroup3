from django.urls import path
from .views import StaticDataView

urlpatterns = [
    path('data/', StaticDataView.as_view(), name='html_data'),
]