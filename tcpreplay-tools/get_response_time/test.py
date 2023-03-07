from scapy.all import *
import time
import threading
import pymongo

mongo_uri = "mongodb://localhost:27017/"
connection = MongoClient(mongo_uri)

# CREATE DATABASE
database = connection['SDN_data']
# CREATE COLLECTION
collection = database['CCDN']

pcap_file = "/home/onos/Desktop/output_rewrite/FileTransfer/FileTransfer_00001_20180328095416/h1-h11/0.pcap"
packets = rdpcap(pcap_file)

src_ip = "10.0.0.1"
dst_ip = "10.0.0.11"

count = 0
for packet in packets:
    with open("packet_count.txt", "w") as f:
        if IP in packet and packet[IP].src == src_ip:
            count = count + 1
        f.write(f"{count}")

def packet_callback(packet):
    with open("response_times.txt", "w") as f:
        f.write(f"{time.time()}")

def sniff_test():
    sniff(filter=f"src {dst_ip} and icmp", prn=packet_callback)

def replay():
    with open("response_times.txt", "r") as f1:
        start_time = time.time()
        srp(packets, timeout=1, verbose=False)
        end_time = float(f1.read())
        print(f"timer {start_time} {end_time}")

    with open("packet_count.txt", "r") as f2:
        count = int(f2.read())

    response_time = (end_time - start_time) / count
    print(f"response_time: {response_time}")


if __name__ == '__main__':
    threading.Thread(target=sniff_test).start()
    threading.Thread(target=replay).start()