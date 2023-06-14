import json
import pika

# establishing a connection with the RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', heartbeat=600, blocked_connection_timeout=300))
channel = connection.channel()


def publish(method, body):
    """
    Обработка отправляемых сообщений в RabbitMQ.
    Используется для сигналов
    Очередь мы выбираем сами - за это отвечает параметр "exchange=''"
    Задаем маршрут к очереди - routing_key='items'
    :param method: информация о сообщении
    :param body: тело сообщения
    :return:
    """
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='', routing_key='items', body=json.dumps(body), properties=properties)