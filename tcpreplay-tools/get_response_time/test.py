from scapy.all import *
import time

pcap_file = "/home/onos/Desktop/output_rewrite/FileTransfer/FileTransfer_00001_20180328094056/h1-h11/0.pcap"

packets = rdpcap(pcap_file)

start_time = time.time()
response_packets = srp(packets, timeout=10, verbose=False)[0]
end_time = time.time()

response_times = [(pkt[1].time - pkt[0].sent_time) for pkt in response_packets]
print("sent")
for i in range(len(response_times)):
    print(f"{response_times[i]:.2f}")