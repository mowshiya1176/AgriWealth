from django.contrib import admin
from .models import WasteItem, WasteCategory


@admin.register(WasteCategory)
class WasteCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'icon']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(WasteItem)
class WasteItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'farmer', 'category', 'quantity', 'unit', 'status', 'is_featured', 'created_at']
    list_filter = ['status', 'category', 'is_featured', 'created_at']
    search_fields = ['title', 'description', 'farmer__username', 'location']
    list_editable = ['status', 'is_featured']
    readonly_fields = ['views_count', 'created_at', 'updated_at']
    date_hierarchy = 'created_at'
