from scapy.all import *

# Set the IP address and port to listen on
src_ip = sys.argv[1]

def filter_gquic(pkt):
    try:
        return UDP in pkt
        #return (UDP in pkt and pkt[UDP].dport == 443 and pkt[IP].src == src_ip) or (UDP in pkt)
    except Exception as e:
        print(e)
        return UDP in pkt

# Define a callback function to handle incoming packets
def handle_packet(packet):
    print("server start sniff")
    if IP in packet:
        print(f"hit")
        # Create a new IP packet with the source and destination IP addresses reversed
        print(f"{packet[IP].src}-{packet.src}, {packet[IP].dst}-{packet.dst}")

        eth = Ether(src=packet.dst, dst=packet.src)
        ip = IP(src=packet[IP].dst, dst=packet[IP].src)
        icmp = ICMP()

        # Combine the IP and ICMP packets and send them back to the client
        reply = eth/ip/icmp
        sendp(reply)
        print(f"sent icmp response: {packet.id}")

# Start a scapy sniffing session to listen for incoming packets
sniff(lfilter=filter_gquic, prn=handle_packet)