import subprocess
import time
from scapy.all import *

# Set the path to the PCAP file and the interface to send packets out on
pcap_file = "/home/onos/Desktop/output_rewrite/FileTransfer/FileTransfer_00001_20180328094056/h1-h11/0.pcap"
interface = "h1-eth0"

# Set the target IP and MAC addresses
src_ip = "10.0.0.1"
target_ip = "10.0.0.11"
target_mac = "00:00:00:00:00:11"

packets = rdpcap(pcap_file)

# Open the PCAP file and iterate over the packets
with open("response_times.txt", "w") as f:
    for packet in packets:
        # Check if the packet is an Ethernet packet with the target MAC address
        if Ether in packet and packet[Ether].dst == target_mac:
            # Check if the packet is an IP packet with the target IP address
            if IP in packet and packet[IP].dst == target_ip and packet[IP].src == src_ip:
                print(packet)
                # Rewrite the Ethernet header with the interface's MAC address
                packet[Ether].src = get_if_hwaddr(interface)
                start_time = time.time()
                send(packet, iface=interface)
                time.sleep(0.1)
                print("sent")
                # Use scapy.sniff() to receive the response packet and record the end time
                sniff(count=1, filter=f"icmp")
                print("test")
                end_time = time.time()

                # Calculate the total time and log it
                total_time = end_time - start_time
                f.write(f"Response time: {total_time:.2f} ms\n")