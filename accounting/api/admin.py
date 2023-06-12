from django.contrib import admin
from .models import *


@admin.register(Salary)
class SalaryAdmin(admin.ModelAdmin):
    list_display = ['employee_name', 'salary_per_month', 'taxes']


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'price']


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['item', 'qty', 'ordered_at', 'total_sum']