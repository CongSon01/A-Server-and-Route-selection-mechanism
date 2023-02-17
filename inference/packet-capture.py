import subprocess as sb
import sys, os
import pika
import config

connection = pika.BlockingConnection(pika.ConnectionParameters(config.RABBIT_URL))
channel = connection.channel()
channel.queue_declare(queue=config.CONSUMER_QUEUE)

# cmd = 'tshark -i any -Y "gquic.payload" \
#         -T fields \
#         -e frame.time_epoch -e ip.src -e udp.srcport -e ip.dst -e udp.dstport -e ip.proto \
#         -e _ws.col.Info -e gquic.payload \
#         -E header=n -E separator=, -E quote=d -E occurrence=f \
#         -a duration:20000'

cmd = 'tshark -i s4-eth2 -Y "tcp.payload" \
        -T fields \
        -e frame.time_epoch -e ip.src -e tcp.srcport -e ip.dst -e udp.dstport -e ip.proto \
        -e _ws.col.Info -e tcp.payload \
        -E header=n -E separator=, -E quote=d -E occurrence=f \
        -a duration:20000'

def main():
    with open("packet-capture.log", "wb") as file:
        proc = sb.Popen(cmd, shell=True, stdout=sb.PIPE, stdin=sb.PIPE)
        line = ''
        for char in iter(lambda: proc.stdout.read(1), b''):
            file.write(char)
            if char == b'\n':
                channel.basic_publish(exchange='', routing_key=config.CONSUMER_ROUTING_KEY, body=line)
                line = ''
                continue
            line += char.decode('latin-1')
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