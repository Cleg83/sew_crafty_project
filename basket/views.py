from django.shortcuts import render, redirect, reverse, HttpResponse, get_object_or_404
from django.contrib import messages
from shop.models import Product


def view_basket(request):
    """ A view for the shopping basket """
    template = 'basket/basket.html'
    context = {
        'on_basket_page': True,
    }
    return render(request, template, context)


def get_basket(request):
    """ Helper function to retrieve the current basket from the session """
    return request.session.get('basket', {})


def save_basket(request, basket):
    """ Helper function to save the updated basket back to the session """
    request.session['basket'] = basket
    request.session.modified = True


def add_to_basket(request, item_id):
    """ Add a specific item and quantity to the basket """
    shop_item = get_object_or_404(Product, pk=item_id)

    try:
        quantity = int(request.POST.get('quantity', 1))
    except ValueError:
        messages.error(request, "Invalid quantity specified.")
        return redirect(reverse('shop_item_info', args=[item_id]))  # redirect to the shop item page

    # If redirect_url is not passed, default to the basket page
    redirect_url = request.POST.get('redirect_url', reverse('view_basket'))

    basket = get_basket(request)

    # Update the basket with the new item and quantity
    if str(item_id) in basket:
        basket[str(item_id)] += quantity
    else:
        basket[str(item_id)] = quantity

    save_basket(request, basket)

    # Add success message
    messages.success(request, f'{shop_item.name} added to your basket!')

    # To avoid recursion, ensure we only redirect to the page we want
    return redirect(redirect_url)  # Redirect either to basket or the original page


def adjust_basket(request, item_id):
    """ Adjust the quantity of an item in the basket """
    shop_item = get_object_or_404(Product, pk=item_id)

    try:
        quantity = int(request.POST.get('quantity', 0))
        if quantity < 1:
            raise ValueError
    except ValueError:
        messages.error(request, "Invalid quantity specified.")
        return redirect(reverse('view_basket'))  # redirect to the basket page

    basket = get_basket(request)
    if str(item_id) in basket:
        basket[str(item_id)] = quantity  # Adjust the quantity
    else:
        messages.warning(request, f"{shop_item.name} is not in your basket.")

    save_basket(request, basket)
    messages.success(request, f'Updated {shop_item.name} quantity to {quantity}.')

    # Avoid recursion by redirecting cleanly
    return redirect(reverse('view_basket'))  # Redirect to the basket page


def delete_from_basket(request, item_id):
    """ Remove a specific item from the basket """
    shop_item = get_object_or_404(Product, pk=item_id)
    basket = get_basket(request)

    if str(item_id) in basket:
        del basket[str(item_id)]  # Remove item from basket
        save_basket(request, basket)
        messages.success(request, f'{shop_item.name} removed from your basket.')
    else:
        messages.warning(request, f'{shop_item.name} was not found in your basket.')

    # To avoid recursion and infinite redirects, redirect only to the basket page
    return redirect(reverse('view_basket'))  # Redirect to the basket page
