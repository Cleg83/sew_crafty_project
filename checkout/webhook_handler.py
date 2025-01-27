import json
import stripe
from django.conf import settings
from django.http import HttpResponse
from django.core.mail import send_mail, EmailMessage
from django.core.mail.backends.console import EmailBackend  
from checkout.models import Order
import logging


stripe.api_key = settings.STRIPE_SECRET

logger = logging.getLogger(__name__)

import time

logger = logging.getLogger(__name__)



def handle_payment_intent_succeeded(event):
    """
    Handle the payment_intent.succeeded webhook from Stripe.
    """
    payment_intent = event['data']['object']
    stripe_pid = payment_intent['id']
    logger.info(f"Received payment_intent.succeeded for {stripe_pid}")

    attempt = 1
    order_exists = False

    # Retry logic to find the order
    while attempt <= 5:
        try:
            order = Order.objects.get(stripe_pid=stripe_pid)
            logger.info(f"Order found with stripe_pid: {stripe_pid}")
            order_exists = True
            break
        except Order.DoesNotExist:
            attempt += 1
            logger.info(f"Attempt {attempt} to find order with stripe_pid: {stripe_pid}")
            time.sleep(1)

    if order_exists:
        # If a stripe_pid is found, consider the order already paid
        if order.stripe_pid == stripe_pid:
            logger.info(f"Order {order.order_number} already has stripe_pid {stripe_pid}.")
            
            # Retrieve the charge object with retry logic
            charge_retrieved = False
            attempt = 1
            while attempt <= 5 and not charge_retrieved:
                try:
                    # Retrieve the Charge object using the payment intent's latest charge
                    stripe_charge = stripe.Charge.retrieve(payment_intent['latest_charge'])
                    charge_retrieved = True
                    logger.info(f"Charge retrieved successfully: {stripe_charge.id}")
                except Exception as e:
                    attempt += 1
                    logger.warning(f"Attempt {attempt} to retrieve charge failed: {str(e)}")
                    time.sleep(1)  # Retry after 1 second

            if not charge_retrieved:
                logger.error(f"Failed to retrieve charge after {attempt} attempts")
                return HttpResponse(content="Failed to retrieve charge details.", status=500)

            # Validate the charge status
            if stripe_charge.status == 'succeeded':
                # If the charge was successful, proceed with marking the order as paid
                order.stripe_pid = stripe_pid
                order.stripe_charge_id = stripe_charge.id  # Save charge ID for reference
                order.save()

                # Send confirmation email
                logger.info(f"Attempting to send confirmation email to {order.email} for order {order.order_number}")
                send_confirmation_email(order.email, order)
                logger.info(f"Order {order.order_number} marked as Paid.")

                return HttpResponse(content=f"Payment intent succeeded for Order {order.order_number}.", status=200)
            else:
                logger.error(f"Charge for order {order.order_number} failed with status: {stripe_charge.status}")
                send_failure_email(order.email)  # Send a failure email if needed
                return HttpResponse(content=f"Charge failed for Order {order.order_number}.", status=400)

        return HttpResponse(content="Payment intent already processed.", status=200)
    
    # If the order still isn't found, log an error and send a notification
    logger.error(f"Order with stripe_pid {stripe_pid} not found after 5 attempts.")
    send_error_notification(f"Order with stripe_pid {stripe_pid} not found after 5 attempts.")
    return HttpResponse(content=f"Order not found for stripe_pid {stripe_pid}", status=404)




def handle_payment_intent_failed(event):
    """
    Handle payment_intent.failed event from Stripe.
    Notifies the user via email about the failed payment.
    """
    payment_intent = event['data']['object']  
    user_email = payment_intent.get('receipt_email')
    
    if user_email:
        send_failure_email(user_email)


# def send_confirmation_email(user_email, order):
#     """
#     Send a confirmation email to the user using the console email backend for testing.
#     """
#     subject = "Order Confirmation"
#     message = f"Thank you for your order #{order.order_number}. Your payment has been successfully processed."

#     try:

#         email_backend = EmailBackend()
#         send_mail(
#             subject,
#             message,
#             'from@example.com',  
#             [user_email],
#             connection=email_backend  
#         )
#         logger.info(f"Confirmation email successfully sent to {user_email}.")
#     except Exception as e:
#         logger.error(f"Failed to send confirmation email to {user_email}: {str(e)}")

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

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
        'yourstore@example.com',  # From email
        [order_email],  # To email
    )
    email.attach_alternative(html_content, "text/html")
    email.send()



def send_failure_email(user_email):
    """
    Send a failure notification email to the user using the console email backend for testing.
    """
    subject = "Payment Failed"
    message = "We're sorry, but your payment could not be processed. Please try again later."
    
    try:
        email_backend = EmailBackend() 
        send_mail(subject, message, 'from@example.com', [user_email], connection=email_backend)  
        logger.info(f"Failure email sent to {user_email}.")
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
        logger.error(f"Error received: {error_message}")
        send_error_notification(f"Error received: {error_message}")
    else:
        # Log the event if it isn't an error
        logger.info(f"Received non-error event: {event['type']}, skipping error handling.")


def send_error_notification(error_message):
    """
    Send an error notification to the admin using the console email backend for testing.
    """
    try:
        email_backend = EmailBackend() 
        send_mail('Stripe Webhook Error', error_message, 'from@example.com', ['admin@example.com'], connection=email_backend)
        logger.info("Error notification sent to admin.")
    except Exception as e:
        logger.error(f"Failed to send error notification: {str(e)}")
