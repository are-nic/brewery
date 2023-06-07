from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    qty = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ('name',)
        db_table = 'items'

    def __str__(self):
        return self.name
