from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import *
from .producer import publish
from .serializers import *


@receiver(post_save, sender=Item)
def create_or_update_item(sender, instance, created, **kwargs):
    """
    Signal triggered when the Item object is created
    """
    serializer = ItemSerializer(data=instance)
    serializer.is_valid()
    print(serializer)
    if created:
        print('item_created', serializer.data)
        publish('item_created', serializer.data)

    if not created:
        print('item_updated', serializer.data)
        publish('item_updated', serializer.data)


@receiver(post_delete, sender=Item)
def delete_item(sender, instance, **kwargs):
    """
    Signal triggered when the Item object is deleted
    """
    item_pk = instance.id
    print('item_deleted', item_pk)
    publish('item_deleted', item_pk)