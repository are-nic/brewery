"""
To receive messages from the Warehouse.
"""
import json
import pika
from api.models import Item
from django.core.management.base import BaseCommand

# connect to RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq', heartbeat=600, blocked_connection_timeout=300))
channel = connection.channel()

channel.queue_declare(queue='warehouse', durable=True)


def callback(ch, method, properties, body):
    """
    It handles the creation, updating, and deletion of Item's instances
    :param ch: the channel where communication occurs
    :param method: the information concerning message delivery
    :param properties: user-defined properties on the message.
    :param body: the message received
    """
    print("Sales -> Receive items from Warehouse")
    data = json.loads(body)
    print(data)

    if properties.content_type == 'item_created':
        Item.objects.update_or_create(id=data['id'], name=data['name'], price=data['price'], qty=data['qty'])
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

    # ch.basic_ack(delivery_tag=method.delivery_tag)


class Command(BaseCommand):
    def handle(self, *args, **options):
        # to allow our callback function to receive messages from the queue.
        channel.basic_consume(queue='warehouse', on_message_callback=callback, auto_ack=True)
        print("Sales Consumer started...")
        channel.start_consuming()       # tell our channel to start receiving messages
