import pika
import json

"""
Publisher: Day la file muc dich day du lieu raw vao rabbit MQ
"""


def connectRabbitMQ(data):
    # chuyen data thanh json
    msg = json.dumps(data)

    # creadentials = pika.PlainCredentials('onos', 'rocks')
    creadentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(
        pika.ConnectionParameters('localhost', 5672, '/', credentials=creadentials))
    channel = connection.channel()

    # thiet lap queue
    channel.queue_declare(queue='onos')
    channel.basic_publish(
        exchange='',
        routing_key='onos',
        body=msg,
        properties=pika.BasicProperties(
            delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
        ))
    # connection.close()