import json
import stripe
from django.conf import settings
from django.http import HttpResponse
from django.core.mail import send_mail, EmailMultiAlternatives
from django.core.mail.backends.console import EmailBackend  
from checkout.models import Order, LineItem
from django.template.loader import render_to_string
from django.db.models import Prefetch

import logging
import time

stripe.api_key = settings.STRIPE_SECRET

logger = logging.getLogger(__name__)


def handle_payment_intent_succeeded(event):
    """
    Handle the payment_intent.succeeded webhook from Stripe.
    """
    payment_intent = event['data']['object']
    stripe_pid = payment_intent['id']

    attempt = 1
    order_exists = False

    # Retry logic to find the order
    while attempt <= 5:
        try:
            # order = Order.objects.get(stripe_pid=stripe_pid)
            order = Order.objects.prefetch_related(
                Prefetch('lineitems', queryset=LineItem.objects.select_related('shop_item'))
            ).get(stripe_pid=stripe_pid)
            order_exists = True
            break
        except Order.DoesNotExist:
            attempt += 1
            time.sleep(2)

    if order_exists:
        if order.stripe_pid == stripe_pid:

            # Retrieve the charge object with retry logic
            charge_retrieved = False
            attempt = 1
            while attempt <= 5 and not charge_retrieved:
                try:
                    stripe_charge = stripe.Charge.retrieve(payment_intent['latest_charge'])
                    charge_retrieved = True
                except Exception as e:
                    attempt += 1
                    time.sleep(2) 

            if not charge_retrieved:
                return HttpResponse(content="Failed to retrieve charge details.", status=500)

            # Validate the charge status
            if stripe_charge.status == 'succeeded':
                order.stripe_pid = stripe_pid
                order.stripe_charge_id = stripe_charge.id  # Save charge ID for reference
                order.save()

                # Send confirmation email
                send_confirmation_email(order.email, order)
                return HttpResponse(content=f"Payment intent succeeded for Order {order.order_number}.", status=200)
            else:
                send_failure_email(order.email)  # Send a failure email if needed
                return HttpResponse(content=f"Charge failed for Order {order.order_number}.", status=400)

        return HttpResponse(content="Payment intent already processed.", status=200)
    
    send_error_notification(f"Order with stripe_pid {stripe_pid} not found after 5 attempts.")
    return HttpResponse(content=f"Order not found for stripe_pid {stripe_pid}", status=404)


def send_confirmation_email(order_email, order):
    subject = f"Order Confirmation - {order.order_number}"

    # HTML content
    html_content = render_to_string("emails/order_confirmation.html", {'order': order})
    
    # Plain text content
    text_content = render_to_string("emails/order_confirmation.txt", {'order': order})

    # Send both HTML and plain-text email
    email = EmailMultiAlternatives(
        subject,
        text_content,
        settings.DEFAULT_FROM_EMAIL,  
        [order_email],  
    )
    email.attach_alternative(html_content, "text/html")
    email.send()
    

def handle_payment_intent_failed(event):
    """
    Handle payment_intent.failed event from Stripe.
    Notifies the user via email about the failed payment.
    """
    payment_intent = event['data']['object']  
    user_email = payment_intent.get('receipt_email')
    
    if user_email:
        send_failure_email(user_email)


def send_failure_email(user_email):
    """
    Send a failure notification email to the user using the console email backend for testing.
    """
    subject = "Payment Failed"
    message = "We're sorry, but your payment could not be processed. Please try again later."
    
    try:
        send_mail(
            subject, 
            message, 
            settings.DEFAULT_FROM_EMAIL,
            [user_email]  
        )
    except Exception as e:
        logger.error(f"Failed to send failure email to {user_email}: {str(e)}")


def handle_generic_error(event):
    """
    Handle error events and log them accordingly.
    If the event isn't an error event, it will not trigger this handler.
    """
    # Check if the event type corresponds to a real error event
    if 'error' in event:
        error_message = event['data']['object'].get('message', 'No error message available.')
        send_error_notification(f"Error received: {error_message}")
    else:
        # Log the event if it isn't an error
        logger.info(f"Received non-error event: {event['type']}, skipping error handling.")


def send_error_notification(error_message):
    """
    Send an error notification to the admin using the console email backend for testing.
    """
    try:
        send_mail(
            'Stripe Webhook Error', 
            error_message, 
            settings.DEFAULT_FROM_EMAIL, 
            settings.EMAIL_HOT_USER,
        )
    except Exception as e:
        logger.error(f"Failed to send error notification: {str(e)}")
