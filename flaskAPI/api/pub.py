import pika
import json

"""
Publisher: Day la file muc dich day du lieu raw vao rabbit MQ
"""
def connectRabbitMQ(data):
    # chuyen data thanh json
    msg = json.dumps(data)
    
    creadentials = pika.PlainCredentials('onos', 'rocks')
    connection = pika.BlockingConnection(
    pika.ConnectionParameters('10.20.0.250', 5672, '/', credentials=creadentials))
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
    #connection.close()

# while(True):
#     # quan trong
#     Links_details = {'src': 1234,'des':3456}
#     # goi ham connect
#     connectRabbitMQ(Links_details)


