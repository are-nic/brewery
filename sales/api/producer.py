import json
import pika

# establishing a connection with the RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', heartbeat=600, blocked_connection_timeout=300))
channel = connection.channel()

channel.exchange_declare(exchange='sales', exchange_type='direct')
# channel.queue_declare(queue='from_sales_to_ware', durable=True)
# channel.queue_declare(queue='from_sales_to_acc', durable=True)


def publish_to_warehouse(method, body):
    """
    Обработка отправляемых сообщений в Warehouse.
    Используется для сигналов
    :param method: информация о сообщении (заголовок по которому происходит поиск в consumer)
    :param body: тело сообщения
    :return:
    """
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='sales', routing_key='to_warehouse', body=json.dumps(body), properties=properties)


def publish_to_accounting(method, body):
    """
    Обработка отправляемых сообщений в Accounting.
    Используется для сигналов
    :param method: информация о сообщении (заголовок по которому происходит поиск в consumer)
    :param body: тело сообщения
    :return:
    """
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='sales', routing_key='to_accounting', body=json.dumps(body), properties=properties)

