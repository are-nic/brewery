"""
To receive messages from the Sales
"""
import json
import pika
from api.models import Item
from django.core.management.base import BaseCommand

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', heartbeat=600, blocked_connection_timeout=300))
channel = connection.channel()
channel.queue_declare(queue='items from sales')


def callback(ch, method, properties, body):
    """
    It handles the updating of Item instances
    :param ch: the channel where communication occurs
    :param method: the information concerning message delivery
    :param properties: user-defined properties on the message.
    :param body: the message received
    """
    print("Receive items from sales")
    data = json.loads(body)
    print(data)

    if properties.content_type == 'item_updated':
        item = Item.objects.get(id=data['id'])
        item.name = data['name']
        item.price = data['price']
        item.qty = data['qty']
        item.save()
        print("item updated")


class Command(BaseCommand):
    def handle(self, *args, **options):
        # to allow our callback function to receive messages from the "items" queue.
        channel.basic_consume(queue='items from sales', on_message_callback=callback, auto_ack=True)
        print("Consuming started...")
        channel.start_consuming()       # tell our channel to start receiving messages
