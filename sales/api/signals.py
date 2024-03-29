from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import *
from .producer import publish_to_warehouse, publish_to_accounting
from .serializers import *


@receiver(post_save, sender=Item)
def create_or_update_item(sender, instance, created, **kwargs):
    """
    Signal triggered when the Item object is created or updated
    """
    serializer = ItemSerializer(instance)

    if not created:
        publish_to_warehouse('item_updated', serializer.data)
        publish_to_accounting('item_updated', serializer.data)

    elif created:
        publish_to_accounting('item_created', serializer.data)


@receiver(post_delete, sender=Item)
def delete_item(sender, instance, **kwargs):
    """
    Signal triggered when the Item object is deleted
    """
    item_pk = instance.id
    publish_to_accounting('item_deleted', item_pk)


@receiver(post_save, sender=OrderItem)
def create_or_update_order_item(sender, instance, created, **kwargs):
    """
    Signal triggered when the OrderItem object is created or updated
    """
    serializer = OrderItemSerializer(instance)

    if created:
        publish_to_accounting('order_item_created', serializer.data)

    if not created:
        publish_to_accounting('order_item_updated', serializer.data)


@receiver(post_delete, sender=OrderItem)
def delete_order_item(sender, instance, **kwargs):
    """
    Signal triggered when the OrderItem object is deleted
    """
    item_pk = instance.id
    publish_to_accounting('order_item_deleted', item_pk)