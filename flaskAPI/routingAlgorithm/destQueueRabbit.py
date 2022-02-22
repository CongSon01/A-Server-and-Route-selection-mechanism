import pika

class destQueueRabbit(object):
    """
    destQueueRabbit: class nay dung de tao Queue quay vong cho dest Ip tren rabbit MQ
    """

    def __init__(self):
        self.dest_ip = ""
      
    def get_dest_ip(self):
        return self.dest_ip

    def connectRabbitMQ(self, ip_dest):
    
            msg = str(ip_dest)
            #print("msg =", msg)
            #print("type msg", type(msg))
            # print("DAY VAO QUEUE", msg)
            connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
            channel = connection.channel()

            channel.queue_declare(queue='dest')
            channel.basic_publish(
                    exchange='',
                    routing_key='dest',
                    body=msg,
                    properties=pika.BasicProperties(
                        delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
                    ))

    def receive_queue(self):
                connection = pika.BlockingConnection(
                pika.ConnectionParameters(host='localhost'))
                channel = connection.channel()
                channel.queue_declare(queue='dest')
                #print('Waitting for data send')

                channel.basic_qos(prefetch_count=1)
                channel.basic_consume(queue='dest', on_message_callback= self.callback )
                
                #channel.open()
                channel.start_consuming()

    def callback(self, ch, method, properties, body):
                    self.dest_ip = body
                    ch.basic_ack(delivery_tag=method.delivery_tag)

                    # do call back duoc goi lien tuc nen sau 1 lan goi ta stop lai
                    ch.close()



