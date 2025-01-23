from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Product, Category
from .forms import AddProductForm, AddCategoryForm


def shop_items(request):
    """ Shop view to show all items in the shop """

    shop_items = Product.objects.filter(permanently_unavailable=False)
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
    """A view for the manage shop page"""
    if not request.user.is_superuser:
        messages.error(
            request, 
            "You do not have the necessary permissions to access this page."
        )
        return redirect('shop')
    
    shop_items = Product.objects.all()
    categories = Category.objects.all()

    template = 'shop/manage_shop.html'

    context = {
        'shop_items': shop_items,
        'categories': categories,
    }

    return render(request, template, context)


def add_shop_item(request):
    """ View to add a new product """
    if not request.user.is_superuser:
        messages.error(
            request, 
            "You do not have the necessary permissions to perform this action."
        )
        return redirect('shop')
    
    if request.method == 'POST':
        form = AddProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product added successfully!')
            return redirect('manage_shop')
        else:
            messages.error(request, 'Failed to add product. Please ensure the form is valid.')
    else:
        form = AddProductForm()

    template = 'shop/add_shop_item.html'
    context = {
        'form': form,
    }
    return render(request, template, context)


def edit_shop_item(request, shop_item_id):
    """ View to edit an existing product """
    if not request.user.is_superuser:
        messages.error(
            request, 
            "You do not have the necessary permissions to perform this action."
        )
        return redirect('shop')

    shop_item = get_object_or_404(Product, pk=shop_item_id)
    if request.method == 'POST':
        form = AddProductForm(request.POST, request.FILES, instance=shop_item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully!')
            return redirect('manage_shop')
        else:
            messages.error(request, 'Failed to update product. Please ensure the form is valid.')
    else:
        form = AddProductForm(instance=shop_item)

    template = 'shop/edit_shop_item.html'
    context = {
        'form': form,
        'shop_item': shop_item,
    }
    return render(request, template, context)


def delete_from_store(request, item_id):
    """
    Marks a shop item as permanently unavailable instead of deleting it.
    """
    if not request.user.is_superuser:
        messages.error(
            request, 
            "You do not have the necessary permissions to perform this action."
        )
        return redirect('shop')

    shop_item = get_object_or_404(Product, id=item_id)
    shop_item.permanently_unavailable = True
    shop_item.save()
    messages.success(request, f"{shop_item.name} has been marked as permanently unavailable.")
    return redirect('manage_shop')


def add_category(request):
    """View to add a new category."""
    if not request.user.is_superuser:
        messages.error(
            request, 
            "You do not have the necessary permissions to perform this action."
        )
        return redirect('shop')
    
    if request.method == "POST":
        form = AddCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Category added successfully!")
            return redirect('manage_shop')  
        else:
            messages.error(request, "Failed to add category. Please check the form.")
    else:
        form = AddCategoryForm()

    template = 'shop/add_category.html'
    context = {
        'form': form,
    }
    return render(request, template, context)


def edit_category(request, category_id):
    """View to edit an existing category."""
    if not request.user.is_superuser:
        messages.error(
            request, 
            "You do not have the necessary permissions to perform this action."
        )
        return redirect('shop')
    
    category = get_object_or_404(Category, pk=category_id)

    if request.method == "POST":
        form = AddCategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, "Category updated successfully!")
            return redirect('manage_shop')  
        else:
            messages.error(request, "Failed to update category. Please check the form.")
    else:
        form = AddCategoryForm(instance=category)

    template = 'shop/edit_category.html'
    context = {
        'form': form,
        'category': category,
    }
    return render(request, template, context)

