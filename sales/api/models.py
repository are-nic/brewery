from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

User = settings.AUTH_USER_MODEL


class Item(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    qty = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ('name',)
        db_table = 'items'

    def __str__(self):
        return self.name


class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_placed = models.BooleanField(default=False, help_text='The Order has been placed')

    class Meta:
        ordering = ('updated_at',)
        db_table = 'order'

    def __str__(self):
        return f'Order from {self.customer.username}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True)
    qty = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ('order',)
        db_table = 'order_items'

    def __str__(self):
        return self.item.name


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    """ create a token when user was created """
    if created:
        Token.objects.create(user=instance)
