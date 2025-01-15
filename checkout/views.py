from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.conf import settings

from .forms import OrderForm
from basket.contexts import basket_contents

from .models import Order, LineItem
from shop.models import Product
from user_profile.models import UserProfile

import stripe
import json

@require_POST
def cache_checkout_data(request):
    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET
        stripe.PaymentIntent.modify(pid, metadata={
            'basket': json.dumps(request.session.get('basket', {})),
            'username': request.user,
        })
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, 'Payment cannot be processed. Please try again later.')
        return HttpResponse(content=e, status=400)


def checkout(request):
    stripe_public = settings.STRIPE_PUBLIC
    stripe_secret = settings.STRIPE_SECRET

    # Check if user is logged in and has a saved address
    if request.user.is_authenticated:
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            has_saved_address = bool(user_profile.default_address_1) 
        except UserProfile.DoesNotExist:
            has_saved_address = False
    else:
        has_saved_address = False  

    if request.method == 'POST':
        basket = request.session.get('basket', {})

        form_data = {
            'first_name': request.POST['first_name'],
            'last_name': request.POST['last_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'address_1': request.POST['address_1'],
            'address_2': request.POST['address_2'],
            'town': request.POST['town'],
            'postcode': request.POST['postcode'],
            'county': request.POST['county'],
            'country': request.POST['country'],
        }

        order_form = OrderForm(form_data)

        if order_form.is_valid():
            order = order_form.save(commit=False)
            pid = request.POST.get('client_secret').split('_secret')[0]
            order.stripe_pid = pid
            order.original_basket = json.dumps(basket)

            # Save the grand total to the order
            basket_to_checkout = basket_contents(request)
            order.grand_total = basket_to_checkout['grand_total']
            order.save()

            # Loop through basket and create LineItems
            for item_id, item_data in basket.items():
                try:
                    shop_item = Product.objects.get(id=item_id)
                    if isinstance(item_data, int):  # Single quantity for each item
                        line_item = LineItem(
                            order=order,
                            shop_item=shop_item,
                            product_name=shop_item.name,  
                            product_price=shop_item.price,  
                            quantity=item_data,
                        )
                        line_item.save()
                except Product.DoesNotExist:
                    messages.error(
                        request,
                        "One item in your basket doesn't exist. "
                        "Please contact us for assistance."
                    )
                    order.delete()
                    return redirect(reverse('view_basket'))

            return redirect(reverse('success', args=[order.order_number]))
        else:
            messages.error(request, 'Error with form. Please check the information you entered.')

    else:
        basket = request.session.get('basket', {})
        if not basket:
            messages.error(request, "There's nothing in your basket")
            return redirect(reverse('shop'))

        basket_to_checkout = basket_contents(request)
        checkout_total = basket_to_checkout['grand_total']
        stripe_total = round(checkout_total * 100)
        stripe.api_key = stripe_secret
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )

    order_form = OrderForm()

    if not stripe_public:
        messages.warning(request, 'Missing stripe public key. Please check environment variables are set correctly.')

    # Pass `has_saved_address` to the template to conditionally render checkboxes
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public': stripe_public,
        'client_secret': intent.client_secret,
        'has_saved_address': has_saved_address, 
    }

    return render(request, template, context)


def success(request, order_number):
    """
    Handle successful checkouts
    """
    order = get_object_or_404(Order, order_number=order_number)

    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user=request.user)
        order.user_profile = profile
        order.save()

    messages.success(request, f'Order successful! Order number: {order_number}. Confirmation will be sent to {order.email}.')

    if 'basket' in request.session:
        del request.session['basket']

    template = 'checkout/success.html'
    context = {
        'order': order
    }

    return render(request, template, context)
