from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.chat_list_view, name='chat_list'),
    path('room/<int:room_id>/', views.chat_room_view, name='chat_room'),
    path('start/<int:item_id>/', views.start_chat_view, name='start_chat'),
]
