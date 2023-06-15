"""
Передача сообщений декларируется через обменник "sales", в которую передаются сообщения из Sales и принимаются в Warehouse и Accounting
Обменник сам создает очереди для каждого из подписчиков (Warehouse и Accounting)
"""
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
    :param method: информация о сообщении (заголовок по которому происходит поиск в consumer)
    :param body: тело сообщения
    :return:
    """
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='sales', routing_key='', body=json.dumps(body), properties=properties)