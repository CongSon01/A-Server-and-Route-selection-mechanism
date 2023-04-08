#!/usr/bin/python3
import subprocess as sb
import sys, os
print(sys.executable)
import pika
import config
import time 

nic = sys.argv[1]

# cmd = 'sudo tshark -i "any" -Y "udp and gquic.payload" \
#         -d udp.port==443,gquic \
#         -T fields \
#         -e frame.time_epoch -e ip.src -e udp.srcport -e ip.dst -e udp.dstport -e ip.proto \
#         -e _ws.col.Info -e gquic.payload \
#         -E header=n -E separator=, -E quote=d -E occurrence=f'

#s9-eth3
cmd = 'sudo tshark -i ${nic} -Y "udp and gquic.payload" \
        -d udp.port==443,gquic \
        -T fields \
        -e frame.time_epoch -e ip.src -e udp.srcport -e ip.dst -e udp.dstport -e ip.proto \
        -e _ws.col.Info -e gquic.payload \
        -E header=n -E separator=, -E quote=d -E occurrence=f'
        
# cmd = 'sudo tshark -i "any" -Y "tcp" \
#         -T fields \
#         -e frame.time_epoch -e ip.src -e tcp.srcport -e ip.dst -e tcp.dstport -e ip.proto \
#         -e _ws.col.Info -e tcp.payload \
#         -E header=n -E separator=, -E quote=d -E occurrence=f'

def main():
    with open("packet-capture.log", "wb") as file:
        
        proc = sb.Popen(cmd, shell=True, stdout=sb.PIPE, stdin=sb.PIPE)
        line = ''
        for char in iter(lambda: proc.stdout.read(1), b''):
            file.write(char)
            if char == b'\n':
                try:
                    credentials = pika.PlainCredentials('guest', 'guest')
                    connection = pika.BlockingConnection(pika.ConnectionParameters(config.RABBIT_URL,credentials=credentials,heartbeat=60))
                    channel = connection.channel()
                    channel.queue_declare(queue=config.CONSUMER_QUEUE)
                    print("send data to rabbitmq")
                    channel.basic_publish(exchange='', routing_key=config.CONSUMER_ROUTING_KEY, body=line)
                    line = ''
                    continue
                except Exception as e:
                    print(e)
            line += char.decode('latin-1')
    # connection.close()

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print('Interrupted', e)
       