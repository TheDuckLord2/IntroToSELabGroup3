from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserCreation

class CustomUserAdmin(UserAdmin):
    model = UserCreation
    list_display = ('id', 'email', 'username', 'is_active', 'is_staff', 'is_superuser', 'account_type')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('email', 'username')
    ordering = ('-date_joined',)

    # Add the fieldsets to include additional fields
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('account_type',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('account_type',)}),
    )

admin.site.register(UserCreation, CustomUserAdmin)

