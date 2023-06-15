import json
import pika

# establishing a connection with the RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', heartbeat=600, blocked_connection_timeout=300))
channel = connection.channel()

channel.exchange_declare(exchange='sales', exchange_type='fanout')


def publish(method, body):
    """
    Обработка отправляемых сообщений в RabbitMQ.
    Используется для сигналов
    :param method: информация о сообщении
    :param body: тело сообщения
    :return:
    """
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='sales', routing_key='', body=json.dumps(body), properties=properties)