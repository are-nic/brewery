from django.contrib import admin
from .models import *


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['item']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'created_at', 'updated_at']
    inlines = [OrderItemInline]


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'qty', 'price']