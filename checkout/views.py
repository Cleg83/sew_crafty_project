from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.http import Http404
from .models import Order
from .forms import OrderForm
from basket.contexts import basket_contents  # Import the basket_contents function to get the basket data

def checkout(request):
    """ Display the checkout page with the order form. """
    # Get basket contents using the basket_contents context function
    basket_context = basket_contents(request)
    
    # If basket is empty, redirect to the basket page
    if basket_context['item_count'] == 0:
        messages.error(request, "Your basket is empty. Please add some items to your basket first.")
        return redirect(reverse('view_basket'))
    
    # Get the total cost (grand total) from the basket context
    total_cost = basket_context['grand_total']
    
    # Initialize the order form (using POST or GET)
    order_form = OrderForm(request.POST or None)

    if request.method == 'POST' and order_form.is_valid():
        # Create and save the order
        order = order_form.save(commit=False)
        order.total_cost = total_cost
        order.save()

        # Optionally clear the basket after the order is placed
        request.session['basket'] = {}  # Clear the basket session
        messages.success(request, "Your order has been placed successfully!")

        # Redirect to the order confirmation page
        return redirect(reverse('order_confirmation', args=[order.id]))
    
    # Render the checkout page with the basket context and the order form
    context = {
        'basket_items': basket_context['basket_items'],
        'total': basket_context['total'],
        'item_count': basket_context['item_count'],
        'delivery': basket_context['delivery'],
        'free_delivery_prompt': basket_context['free_delivery_prompt'],
        'free_delivery_item_threshold': basket_context['free_delivery_item_threshold'],
        'grand_total': basket_context['grand_total'],
        'order_form': order_form,
    }

    return render(request, 'checkout/checkout.html', context)
