from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'role', 'location', 'is_active', 'date_joined']
    list_filter = ['role', 'is_active', 'date_joined']
    search_fields = ['username', 'email', 'location']
    fieldsets = UserAdmin.fieldsets + (
        ('AgriWealth Info', {'fields': ('role', 'phone', 'location', 'bio', 'profile_image')}),
    )
