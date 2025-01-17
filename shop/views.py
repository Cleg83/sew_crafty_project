from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Product, Category

def shop_items(request):
    """ Shop view to show all items in the shop """

    shop_items = Product.objects.all()
    query = None
    category_filter = None
    sort_by = None

    # Search functionality
    if 'q' in request.GET:
        query = request.GET['q']
        if query:
            queries = Q(name__icontains=query) | Q(description__icontains=query)
            shop_items = shop_items.filter(queries)
        else:
            messages.error(request, 'Please enter some search criteria!')

    # Category filtering
    if 'category' in request.GET:
        category_filter = request.GET['category']
        if category_filter:
            shop_items = shop_items.filter(category__id=category_filter)

    # Sorting functionality
    if 'sort' in request.GET:
        sort_by = request.GET['sort']
        if sort_by == 'price_low_to_high':
            shop_items = shop_items.order_by('price')
        elif sort_by == 'price_high_to_low':
            shop_items = shop_items.order_by('-price')
        elif sort_by == 'name_a_to_z':
            shop_items = shop_items.order_by('name')
        elif sort_by == 'name_z_to_a':
            shop_items = shop_items.order_by('-name')

    categories = Category.objects.all()

    context = {
        'shop_items': shop_items,
        'search_criteria': query,
        'category_filter': category_filter,
        'categories': categories,
        'sort_by': sort_by,
        'on_shop_page': True,
    }

    return render(request, 'shop/shop.html', context)


def shop_item_info(request, shop_item_id):
    """ Shop item info view """

    shop_item = get_object_or_404(Product, pk=shop_item_id)

    context = {
        'shop_item': shop_item, 
    }

    return render(request, 'shop/shop_item_info.html', context)


def manage_shop(request):
    
    shop_items = Product.objects.all()
    categories = Category.objects.all()

    template = 'shop/manage_shop.html'

    context = {
        'shop_items': shop_items,
        'categories': categories,
    }

    return render(request, template, context)

