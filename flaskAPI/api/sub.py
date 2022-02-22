import pika
import json

class Sub(object):
    """
    Subscriber: Day la file muc dich nhan du lieu tu rabbit MQ
    file app.py se lay du leiu tu file nay voi ham sau:
                update.read_params_from_rabbit()
    """

    def __init__(self):
        """
        stack: chua du lieu nhan duoc tu rabbit MQ
        """
        self.stack = []
        self.len_stack = 0

    def receive_queue(self):
        
        connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()
        channel.queue_declare(queue='onos')
        #print('Waitting for data send')

        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(queue='onos', on_message_callback= self.callback )
        
        #channel.open()
        channel.start_consuming()

    def callback(self, ch, method, properties, body):
        
            # body la du lieu nhan duoc tu rabbit MQ
            self.stack.append( json.loads(body) ) 
            self.len_stack +=1 
            ch.basic_ack(delivery_tag=method.delivery_tag)

            # do call back duoc goi lien tuc nen sau 1 lan goi ta stop lai
            ch.close()
           
    def peek_stack(self):
        return self.stack[-1]

    def get_size_stack(self):
        return self.len_stack

    def pop_stack(self):
        return self.stack.pop()      

