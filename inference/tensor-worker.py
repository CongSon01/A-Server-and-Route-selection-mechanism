import pika
import json
import os, sys, threading
import tensorflow as tf
import numpy as np
import config
import requests

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
        ip_src = temp["ip_src"]

        # Determine the maximum length of the lists
        max_len = max(len(lst) for lst in list_of_lists)

        # Pad each list with the default value (0 in this case)
        padded_list_of_lists = [lst + [0] * (max_len - len(lst)) for lst in list_of_lists]

        # Convert the list of lists to a 2D NumPy array
        x_test = np.array(padded_list_of_lists)
        x_test = x_test / 255
        x_test = x_test.reshape(-1, 20, 128, 1)
        
        prediction = model.predict(x_test)
        one_flow_pred = int(np.argmax(prediction, axis=-1))

        label_dict = {'FileTransfer': 0, 'Music': 1, 'VoIP': 2, 'Youtube': 3}
        for key, value in label_dict.items():
            if one_flow_pred == value:
                print(f"=== one_flow_pred === {one_flow_pred}")

        url_update_cost = "http://10.20.0.201:5000/update_cost_base_on_service"
        response_update_cost = requests.post(url_update_cost, {"host_ip": ip_src, "service_type": str(one_flow_pred)})
        print("response: ", response_update_cost)

        url_server_selection = "http://10.20.0.201:5000/getIpServerBasedService"
        response_server_selection = requests.post(url_server_selection, {"host_ip": ip_src, "service_type": str(one_flow_pred)})
        print("response: ", response_server_selection)

        return one_flow_pred

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

