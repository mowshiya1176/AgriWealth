from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import ChatRoom, Message
from marketplace.models import WasteItem
from accounts.models import User


@login_required
def chat_list_view(request):
    user = request.user
    if user.is_farmer():
        rooms = ChatRoom.objects.filter(farmer=user).select_related('buyer', 'waste_item')
    else:
        rooms = ChatRoom.objects.filter(buyer=user).select_related('farmer', 'waste_item')
    return render(request, 'chat/chat_list.html', {'rooms': rooms})


@login_required
def chat_room_view(request, room_id):
    room = get_object_or_404(ChatRoom, id=room_id)
    user = request.user
    if user != room.farmer and user != room.buyer:
        messages.error(request, 'You do not have access to this chat.')
        return redirect('chat:chat_list')
    chat_messages = room.messages.select_related('sender').all()
    # Mark messages as read
    chat_messages.filter(is_read=False).exclude(sender=user).update(is_read=True)
    return render(request, 'chat/chat_room.html', {
        'room': room,
        'chat_messages': chat_messages,
        'other_user': room.get_other_user(user),
    })


@login_required
def start_chat_view(request, item_id):
    item = get_object_or_404(WasteItem, id=item_id)
    if request.user == item.farmer:
        messages.error(request, 'You cannot chat with yourself.')
        return redirect('marketplace:waste_detail', pk=item_id)
    if request.user.is_farmer():
        messages.error(request, 'Only buyers can initiate chats.')
        return redirect('marketplace:waste_detail', pk=item_id)

    room, created = ChatRoom.objects.get_or_create(
        farmer=item.farmer,
        buyer=request.user,
        waste_item=item,
    )
    return redirect('chat:chat_room', room_id=room.id)
