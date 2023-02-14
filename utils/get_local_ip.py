import netifaces

def get_local_ip(nic):
    addrs = netifaces.ifaddresses(nic)
    ipv4_addrs = [addr["addr"] for addr in addrs.get(netifaces.AF_INET, [])]
    return ipv4_addrs[0]
