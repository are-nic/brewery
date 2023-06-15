"""
To receive messages from the Warehouse. Подписка на очередь 'warehouse', в которую передаются сообщения для Sales
"""
import json
import pika
from api.models import Item
from django.core.management.base import BaseCommand

# connect to RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', heartbeat=600, blocked_connection_timeout=300))
channel = connection.channel()

'''channel.exchange_declare(exchange='warehouse', exchange_type='fanout')

result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

channel.queue_bind(exchange='warehouse', queue=queue_name)'''
channel.queue_declare(queue='warehouse')


def callback(ch, method, properties, body):
    """
    It handles the creation, updating, and deletion of Item's instances
    :param ch: the channel where communication occurs
    :param method: the information concerning message delivery
    :param properties: user-defined properties on the message.
    :param body: the message received
    """
    print("Receive items from warehouse")
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


class Command(BaseCommand):
    def handle(self, *args, **options):
        # to allow our callback function to receive messages from the queue.
        channel.basic_consume(queue='warehouse', on_message_callback=callback, auto_ack=True)
        print("Consuming started...")
        channel.start_consuming()       # tell our channel to start receiving messages
