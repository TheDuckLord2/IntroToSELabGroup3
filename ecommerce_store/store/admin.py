from django.contrib import admin
from .models import StoreStock,User,Order,OrderDetails

admin.site.register(StoreStock)
admin.site.register(User)
admin.site.register(Order)
admin.site.register(OrderDetails)