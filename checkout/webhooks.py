import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import stripe

from .webhook_handler import handle_payment_intent_succeeded, handle_payment_intent_failed, handle_generic_error


# Define the Stripe secret key
stripe.api_key = settings.STRIPE_SECRET

# Define the endpoint secret
endpoint_secret = settings.STRIPE_ENDPOINT_SECRET

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.headers.get("Stripe-Signature", "")
    print("Headers received:", request.headers)
    print("Stripe-Signature:", sig_header)
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return JsonResponse({'error': 'Invalid payload'}, status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return JsonResponse({'error': 'Invalid signature'}, status=400)

    # Handle the event
    event_type = event['type']
    
    if event_type == 'payment_intent.succeeded':
        handle_payment_intent_succeeded(event)
    elif event_type == 'payment_intent.failed':
        handle_payment_intent_failed(event)
    else:
        handle_generic_error(event)
    
    return JsonResponse({'status': 'success'}, status=200)

