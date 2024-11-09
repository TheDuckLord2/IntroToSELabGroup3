from django.contrib import admin
from .models import CustomModel
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

# Admin class for CustomModel
class CustomModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'description')
    search_fields = ('name', 'description')
    list_filter = ('user',)

    # You can add custom functionality here, e.g., actions, or specific filtering.

# Admin class for User (if you want to extend User admin)
class CustomUserAdmin(UserAdmin):
    # Customize the User Admin page to include more fields (if necessary)
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('is_admin',)}),  # Example custom field
    )
    list_display = ('username', 'email', 'is_staff', 'is_superuser', 'is_admin')
    list_filter = ('is_admin',)

    # Optional: Override permissions based on user role
    def has_change_permission(self, request, obj=None):
        # Allow superuser and users with 'is_admin' to change, others don't
        if request.user.is_superuser or getattr(request.user, 'is_admin', False):
            return True
        return False

# Register models with the admin interface
admin.site.register(CustomModel, CustomModelAdmin)
admin.site.unregister(User)  # Unregister default User Admin
admin.site.register(User, CustomUserAdmin)  # Register custom User Admin
