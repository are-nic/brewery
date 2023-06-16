"""
To receive messages from the Sales.
"""
import json
import pika
from api.models import Item
from django.core.management.base import BaseCommand

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', heartbeat=600, blocked_connection_timeout=300))
channel = connection.channel()

channel.exchange_declare(exchange='sales', exchange_type='direct')

result = channel.queue_declare(queue='', exclusive=True, durable=True)
queue_name = result.method.queue

channel.queue_bind(exchange='sales', queue=queue_name, routing_key='to_warehouse')


def callback(ch, method, properties, body):
    """
    It handles the updating of Item instances
    :param ch: the channel where communication occurs
    :param method: the information concerning message delivery
    :param properties: user-defined properties on the message.
    :param body: the message received
    """
    print("Warehouse -> Receive message from Sales")
    data = json.loads(body)
    print(data)

    item = Item.objects.get(id=data['id'])
    # Сравниваем кол-во полученного товара с кол-вом в таблице данного проекта. Если оно совпадает, то не обновляем продукт
    if properties.content_type == 'item_updated' and item.qty != data['qty']:
        item.name = data['name']
        item.price = data['price']
        item.qty = data['qty']
        item.save()
        print("item updated")

    ch.basic_ack(delivery_tag=method.delivery_tag)


class Command(BaseCommand):
    def handle(self, *args, **options):
        # to allow our callback function to receive messages from the queue.
        channel.basic_consume(queue=queue_name, on_message_callback=callback)
        print("Warehouse's Consumer started...")
        channel.start_consuming()

