from django.urls import path
from . import views
from .webhooks import stripe_webhook

urlpatterns = [
    path('', views.checkout, name='checkout'),
    path('cache_checkout_data/', views.cache_checkout_data, name='cache_checkout_data'),
    path('success/<order_number>', views.success, name='success'),
    path('webhook/', stripe_webhook, name='stripe_webhook'),
]