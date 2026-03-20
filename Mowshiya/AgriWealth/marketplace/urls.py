from django.urls import path
from . import views

app_name = 'marketplace'

urlpatterns = [
    path('', views.marketplace_view, name='marketplace'),
    path('item/<int:pk>/', views.waste_detail_view, name='waste_detail'),
    path('add/', views.add_waste_view, name='add_waste'),
    path('item/<int:pk>/edit/', views.edit_waste_view, name='edit_waste'),
    path('item/<int:pk>/delete/', views.delete_waste_view, name='delete_waste'),
]
