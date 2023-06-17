from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class Item(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    qty = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ('name',)
        db_table = 'items'

    def __str__(self):
        return self.name


class OrderItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True)
    qty = models.PositiveIntegerField(default=0)
    total_sum = models.FloatField(default=0.00)

    class Meta:
        ordering = ('item',)
        db_table = 'order_items'

    def __str__(self):
        return self.item.name

    def save(self, *args, **kwargs):
        self.total_sum = float(self.item.price) * self.qty
        super(OrderItem, self).save(*args, **kwargs)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    """ create a token when user was created """
    if created:
        Token.objects.create(user=instance)