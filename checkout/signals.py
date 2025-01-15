from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import LineItem


@receiver(post_save, sender=LineItem)
def update_order_on_save(sender, instance, created, **kwargs):
    """
    Update order totals when a LineItem is created or updated.
    """
    instance.order.update_total()


@receiver(post_delete, sender=LineItem)
def update_order_on_delete(sender, instance, **kwargs):
    """
    Update order totals when a LineItem is deleted.
    """
    instance.order.update_total()