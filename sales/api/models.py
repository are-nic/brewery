from django.db import models
from django.conf import settings


User = settings.AUTH_USER_MODEL


class Order(models.Model):
    PAY_METHOD = [
        ('UPON_RECEIPT', 'Pay upon receipt'),
        ('ONLINE', 'Pay online'),
    ]
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    pay_method = models.CharField(max_length=50, choices=PAY_METHOD)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_paid = models.BooleanField(default=False)

    class Meta:
        ordering = ('updated_at',)
        db_table = 'order'

    def __str__(self):
        return self.customer.name


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='recipes', on_delete=models.CASCADE)
    item = models.CharField()
    qty = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ('order',)
        db_table = 'order_item'

    def __str__(self):
        return self.item
