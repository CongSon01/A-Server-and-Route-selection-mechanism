from scapy.all import *

# Set the IP address and port to listen on
ip = "10.0.0.1"

# Define a callback function to handle incoming packets
def handle_packet(packet):
    if IP in packet:
        print(f"hit")
        # Create a new IP packet with the source and destination IP addresses reversed
        ip_pkt = IP(src=packet[IP].dst, dst=packet[IP].src)

        # Create a new ICMP ping reply packet
        icmp_pkt = ICMP(type=0, code=0)

        # Combine the IP and ICMP packets and send them back to the client
        reply_pkt = ip_pkt / icmp_pkt
        send(reply_pkt)
        print("sent icmp response")

# Start a scapy sniffing session to listen for incoming packets
sniff(filter=f"src {ip}", prn=handle_packet)