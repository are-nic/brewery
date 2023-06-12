from django.db import models


class Salary(models.Model):
    employee_name = models.CharField(max_length=100)
    salary_per_month = models.FloatField()
    taxes = models.FloatField(default=0.00)

    class Meta:
        ordering = ('employee_name',)
        db_table = 'salary'

    def __str__(self):
        return self.employee_name

    def save(self, *args, **kwargs):
        self.taxes = self.salary_per_month * 0.1
        super(Salary, self).save(*args, **kwargs)


class Item(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    class Meta:
        ordering = ('name',)
        db_table = 'items'

    def __str__(self):
        return self.name


class OrderItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True)
    qty = models.PositiveIntegerField(default=0)
    ordered_at = models.DateTimeField(verbose_name="Item was ordered")
    total_sum = models.FloatField(default=0.00)

    class Meta:
        ordering = ('ordered_at',)
        db_table = 'order_items'

    def __str__(self):
        return self.item.name

    def save(self, *args, **kwargs):
        self.total_sum = float(self.item.price) * self.qty
        super(OrderItem, self).save(*args, **kwargs)