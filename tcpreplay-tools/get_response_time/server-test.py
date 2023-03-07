from scapy.all import *
import threading
import queue

src_ip = sys.argv[1]
interface = sys.argv[2]

def filter_gquic(pkt):
    try:
        return (UDP in pkt and pkt[UDP].dport == 443 and pkt[IP].src == src_ip)
    except Exception as e:
        print(e)
        return UDP in pkt

def sniff_thread(interface, queue):
    sniff(lfilter=filter_gquic, iface=interface, prn=lambda pkt: queue.put(pkt))

def process_packets(queue):
    try:
        packet = queue.get()
        print(f"{packet.summary()}")

        eth = Ether(src=packet.dst, dst=packet.src)
        ip = IP(src=packet[IP].dst, dst=packet[IP].src)
        icmp = ICMP()

        # Combine the IP and ICMP packets and send them back to the client
        reply = eth/ip/icmp
        sendp(reply)
        print(f"sent icmp response: {packet.id}")
    except Exception as e:
        print(e)

packet_queue = queue.Queue()

threads = []
for i in range(2):
    thread = threading.Thread(target=sniff_thread, args=(interface, packet_queue))
    thread.start()
    threads.append(thread)

processing_thread = threading.Thread(target=process_packets, args=(packet_queue,))
processing_thread.start()

for thread in threads:
    thread.join()
processing_thread.join()