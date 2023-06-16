"""
To receive messages from the Sales. Подписка на обменник 'sales', из которого формируется очередь специально для для Accounting
"""
import json
import pika
from api.models import Item, OrderItem
from django.core.management.base import BaseCommand

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', heartbeat=600, blocked_connection_timeout=300))
channel = connection.channel()

channel.exchange_declare(exchange='sales', exchange_type='direct')

result = channel.queue_declare(queue='', exclusive=True, durable=True)
queue_name = result.method.queue

# Привязка очереди к Exchange
channel.queue_bind(exchange='sales', queue=queue_name, routing_key='to_accounting')


def callback(ch, method, properties, body):
    """
    It handles the creation, updating, and deletion of Item's and OrderItem's instances
    :param ch: the channel where communication occurs
    :param method: the information concerning message delivery
    :param properties: user-defined properties on the message.
    :param body: the message received
    """
    print("Accounting -> Receive Item from Sales")
    data = json.loads(body)
    print(data)
    # ---------------------------------- item ---------------------------------------
    if properties.content_type == 'item_created':
        Item.objects.create(id=data['id'], name=data['name'], price=data['price'], qty=data['qty'])
        print("item created")

    elif properties.content_type == 'item_updated':
        item = Item.objects.get(id=data['id'])
        item.name = data['name']
        item.price = data['price']
        item.qty = data['qty']
        item.save()
        print("item updated")

    elif properties.content_type == 'item_deleted':
        item = Item.objects.get(id=data)
        item.delete()
        print("item deleted")

    # ---------------------------------- Order's Item ----------------------------------
    elif properties.content_type == 'order_item_created':
        item = Item.objects.get(id=data['item'])
        OrderItem.objects.create(id=data['id'], item=item, qty=data['qty'])
        print("Order's item created")

    elif properties.content_type == 'order_item_updated':
        item = Item.objects.get(id=data['item'])
        order_item = OrderItem.objects.get(id=data['id'])
        order_item.item = item
        order_item.qty = data['qty']
        order_item.save()
        print("Order's item updated")

    elif properties.content_type == 'order_item_deleted':
        order_item = OrderItem.objects.get(id=data)
        order_item.delete()
        print("Order's item deleted")

    ch.basic_ack(delivery_tag=method.delivery_tag)


class Command(BaseCommand):
    def handle(self, *args, **options):
        # to allow our callback function to receive messages from the "items" queue.
        channel.basic_consume(queue=queue_name, on_message_callback=callback)
        print("Accounting Consumer started...")
        channel.start_consuming()       # tell our channel to start receiving messages
