import subprocess as sb
import sys
import pika
import os

# config
import tomli

try:
    with open('config.toml', "rb") as f:
        toml_dict = tomli.load(f)
except tomli.TOMLDecodeError:
    print("Yep, definitely not valid.")

config = toml_dict['packet-capture']

QUEUE_NAME = config['QUEUE_NAME']
ROUTING_KEY = config['ROUTING_KEY']

CMD = config['CMD'] 

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue=QUEUE_NAME)


def hex_to_dec(string: str):
    pass

def main():
    with open("packet-capture.log", "wb") as file:
        proc = sb.Popen(CMD, shell=True, stdout=sb.PIPE, stdin=sb.PIPE)
        line = ''
        # lines = []
        for char in iter(lambda: proc.stdout.read(1), b''):
            file.write(char)
            if char == b'\n':
                channel.basic_publish(
                            exchange='',
                            routing_key=ROUTING_KEY,
                            body=line)
                # lines.append(line)
                # print(line)
                line = ''
                continue
            # print(char)
            line += char.decode('latin-1')
    # print(lines[20])
    connection.close()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)