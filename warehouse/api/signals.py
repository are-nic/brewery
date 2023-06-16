from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import *
from .producer import publish
from .serializers import *


@receiver(post_save, sender=Item)
def create_or_update_item(sender, instance, created, **kwargs):
    """
    Signal triggered when the Item object is created or updated
    """
    serializer = ItemSerializer(instance)

    if created:     # если создан Продукт в БД
        publish('item_created', serializer.data)

    if not created:     # если обновлен Продукт в БД
        publish('item_updated', serializer.data)


@receiver(post_delete, sender=Item)
def delete_item(sender, instance, **kwargs):
    """
    Signal triggered when the Item object is deleted
    """
    item_pk = instance.id
    publish('item_deleted', item_pk)