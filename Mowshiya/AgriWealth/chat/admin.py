from django.contrib import admin
from .models import ChatRoom, Message


@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ['farmer', 'buyer', 'waste_item', 'created_at', 'updated_at']
    list_filter = ['created_at']
    search_fields = ['farmer__username', 'buyer__username']


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'room', 'content_preview', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['sender__username', 'content']

    def content_preview(self, obj):
        return obj.content[:60]
    content_preview.short_description = 'Message'
