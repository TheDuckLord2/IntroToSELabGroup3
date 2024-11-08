from django.contrib import admin
from .models import UserCreation, CreatedUser, Cart

# Register your models here.

admin.site.register(UserCreation)
admin.site.register(CreatedUser)
admin.site.register(Cart)
