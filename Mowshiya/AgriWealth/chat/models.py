from django.db import models
from django.conf import settings


class ChatRoom(models.Model):
    farmer = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='farmer_rooms'
    )
    buyer = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='buyer_rooms'
    )
    waste_item = models.ForeignKey(
        'marketplace.WasteItem', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='chat_rooms'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['farmer', 'buyer', 'waste_item']
        ordering = ['-updated_at']

    def __str__(self):
        return f"Chat: {self.farmer.username} and {self.buyer.username}"

    def get_other_user(self, user):
        return self.buyer if user == self.farmer else self.farmer


class Message(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.sender.username}: {self.content[:50]}"
