import pika
import json
import os, sys, threading
import time
import tensorflow as tf
import numpy as np
import config

PATH_ABSOLUTE = "/home/onos/Downloads/A-Server-and-Route-selection-mechanism/inference"

class ThreadedConsumer(threading.Thread):
    def __init__(self, thread_id=-1):
        threading.Thread.__init__(self)
        self.thread_id = thread_id

        # parameters = pika.URLParameters(RABBIT_URL)
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=config.RABBIT_URL))
        self.channel = connection.channel()
        # self.channel.queue_declare(queue=QUEUE_NAME, auto_delete=False)
        # self.channel.queue_bind(queue=QUEUE_NAME, exchange=EXCHANGE, routing_key=ROUTING_KEY)
        self.channel.basic_qos(prefetch_count=config.PREFETCH_COUNT)
        self.channel.basic_consume(config.PRODUCER_QUEUE, on_message_callback=self.callback, auto_ack=False)
        threading.Thread(target=self.channel.basic_consume(config.PRODUCER_QUEUE, on_message_callback=self.callback))

    def callback(self, channel, method, properties, body):
        message = json.loads(body)
        # time.sleep(5)
        self.predict(message)
        channel.basic_ack(delivery_tag=method.delivery_tag)

    def predict(self, message):
        model = tf.keras.models.load_model(PATH_ABSOLUTE + "/model/model.h5")
        temp = next(iter(message.values()))
        list_of_lists = temp["data"]
        # Determine the maximum length of the lists
        # max_len = max(len(lst) for lst in list_of_lists)
        max_len = 2560
        # Pad each list with the default value (0 in this case)
        padded_list_of_lists = [lst + [0] * (max_len - len(lst)) for lst in list_of_lists]

        # Convert the list of lists to a 2D NumPy array
        x_test = np.array(padded_list_of_lists)

        x_test = x_test.reshape(-1, 20, 128, 1)
        x_test = x_test / 255
        predictions = model.predict(x_test)
        one_flow_pred = np.argmax(predictions, axis=-1)

        label_dict ={'FileTransfer': 0, 'Music': 1, 'VoIP': 2, 'Youtube': 3}

        print("=== flow_pred ===", one_flow_pred)

        return one_flow_pred
        # with open(f"{self.thread_id}.json", "w") as outfile:
            # outfile.write(message)
        # src (ip-port) - dst(ip=port) - label - protocol (4-7)

    def run(self):
        print ('starting thread to consume from rabbit...')
        self.channel.start_consuming()

def main():
    for thread_id in range(config.THREADS):
        print ('launch thread', thread_id)
        td = ThreadedConsumer(thread_id=thread_id)
        td.start()

if __name__ == '__main__':
    main()
    # ctrl + c to exit

