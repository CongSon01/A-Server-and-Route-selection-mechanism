import pika
import json
import os, sys, threading
import time
import tomli

# tensorflow
# import tensorflow as tf
# from keras.models import load_model

import tomli
try:
    with open('config.toml', "rb") as f:
        toml_dict = tomli.load(f)
except tomli.TOMLDecodeError:
    print("Yep, definitely not valid.")

config = toml_dict['tensor-worker']

RABBIT_URL = 'localhost'
ROUTING_KEY = 'hello2'
QUEUE_NAME = ROUTING_KEY
EXCHANGE = 'events'
THREADS = 5
PREFETCH_COUNT = 2 * THREADS

class ThreadedConsumer(threading.Thread):
    def __init__(self, thread_id=-1):
        threading.Thread.__init__(self)
        self.thread_id = thread_id

        # parameters = pika.URLParameters(RABBIT_URL)
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = connection.channel()
        # self.channel.queue_declare(queue=QUEUE_NAME, auto_delete=False)
        # self.channel.queue_bind(queue=QUEUE_NAME, exchange=EXCHANGE, routing_key=ROUTING_KEY)
        self.channel.basic_qos(prefetch_count=PREFETCH_COUNT)
        self.channel.basic_consume(QUEUE_NAME, on_message_callback=self.callback, auto_ack=True)
        threading.Thread(target=self.channel.basic_consume(QUEUE_NAME, on_message_callback=self.callback))

    def callback(self, channel, method, properties, body):
        message = json.loads(body)
        # time.sleep(5)
        # print(message)
        self.predict(message)
        channel.basic_ack(delivery_tag=method.delivery_tag)

    def predict(self, message):
        print(message)
        with open(f"{self.thread_id}.json", "w") as outfile:
            outfile.write(message)

    def run(self):
        print ('starting thread to consume from rabbit...')
        self.channel.start_consuming()

def main():
    for thread_id in range(THREADS):
        print ('launch thread', thread_id)
        td = ThreadedConsumer(thread_id=thread_id)
        td.start()


if __name__ == '__main__':
    main()
    # ctrl + c to exit

