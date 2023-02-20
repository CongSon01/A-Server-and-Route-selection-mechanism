import pika
import json
from multiprocessing import Process
from datetime import datetime
import multiprocessing
import concurrent.futures
import sqlite3 as sqll

import sys, os


def do_job(body):
    body = json.loads(body)
    type = body[-1]['Type']
    print('Object type in work currently ' + type)
    cnums = [x['cadnum'] for x in body[:-1]]
    print('Got {} cnums to work with'.format(len(cnums)))

    date_start = datetime.now()
    download_xmls(type,cnums)
    date_end = datetime.now()
    ch.basic_ack(delivery_tag=method.delivery_tag)
    print('Download complete in {} seconds'.format((date_end-date_start).total_seconds()))

def callback(ch, method, properties, body):
    print('Got something')
    p = Process(target=do_job,args=(body))
    p.start()
    p.join()

def consume(queue_name='test', hostname='localhost', worker_id=-1):
    parameters = pika.URLParameters(hostname)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue=queue_name, durable=True)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(callback, queue='bot-test')
    channel.start_consuming()


def get_workers():
    try:
        return multiprocessing.cpu_count()
    except NotImplementedError:
        return 4

def main():
    workers = get_workers()
    with concurrent.futures.ProcessPoolExecutor() as executor:
        for i in range(workers):
            executor.submit(consume)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')

        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)