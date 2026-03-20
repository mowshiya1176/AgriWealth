from django.shortcuts import render
from marketplace.models import WasteItem, WasteCategory


def home_view(request):
    featured_items = WasteItem.objects.filter(
        status='available', is_featured=True
    ).select_related('farmer', 'category')[:6]
    recent_items = WasteItem.objects.filter(
        status='available'
    ).select_related('farmer', 'category')[:8]
    categories = WasteCategory.objects.all()
    stats = {
        'total_listings': WasteItem.objects.count(),
        'available': WasteItem.objects.filter(status='available').count(),
        'categories': categories.count(),
    }
    return render(request, 'core/home.html', {
        'featured_items': featured_items,
        'recent_items': recent_items,
        'categories': categories,
        'stats': stats,
    })


def about_view(request):
    return render(request, 'core/about.html')
