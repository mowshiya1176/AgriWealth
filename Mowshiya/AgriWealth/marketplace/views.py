from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import WasteItem, WasteCategory
from .forms import WasteItemForm, SearchForm


def marketplace_view(request):
    form = SearchForm(request.GET)
    items = WasteItem.objects.filter(status='available').select_related('farmer', 'category')

    if form.is_valid():
        q = form.cleaned_data.get('q')
        category = form.cleaned_data.get('category')
        status = form.cleaned_data.get('status')

        if q:
            items = items.filter(
                Q(title__icontains=q) |
                Q(description__icontains=q) |
                Q(possible_products__icontains=q) |
                Q(location__icontains=q)
            )
        if category:
            items = items.filter(category=category)
        if status:
            items = items.filter(status=status)

    categories = WasteCategory.objects.all()
    return render(request, 'marketplace/marketplace.html', {
        'items': items,
        'form': form,
        'categories': categories,
        'total': items.count(),
    })


def waste_detail_view(request, pk):
    item = get_object_or_404(WasteItem, pk=pk)
    item.views_count += 1
    item.save(update_fields=['views_count'])
    related = WasteItem.objects.filter(category=item.category).exclude(pk=pk)[:4]
    return render(request, 'marketplace/waste_detail.html', {'item': item, 'related': related})


@login_required
def add_waste_view(request):
    if not request.user.is_farmer():
        messages.error(request, 'Only farmers can list waste items.')
        return redirect('marketplace:marketplace')
    if request.method == 'POST':
        form = WasteItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.farmer = request.user
            item.save()
            messages.success(request, 'Waste item listed successfully!')
            return redirect('marketplace:waste_detail', pk=item.pk)
    else:
        form = WasteItemForm()
    return render(request, 'marketplace/waste_form.html', {'form': form, 'action': 'Add'})


@login_required
def edit_waste_view(request, pk):
    item = get_object_or_404(WasteItem, pk=pk, farmer=request.user)
    if request.method == 'POST':
        form = WasteItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Listing updated!')
            return redirect('marketplace:waste_detail', pk=item.pk)
    else:
        form = WasteItemForm(instance=item)
    return render(request, 'marketplace/waste_form.html', {'form': form, 'action': 'Edit', 'item': item})


@login_required
def delete_waste_view(request, pk):
    item = get_object_or_404(WasteItem, pk=pk, farmer=request.user)
    if request.method == 'POST':
        item.delete()
        messages.success(request, 'Listing deleted.')
        return redirect('accounts:profile')
    return render(request, 'marketplace/waste_confirm_delete.html', {'item': item})
