import sys, os
from scapy.all import *
import time
import threading
import subprocess

service_name = sys.argv[1]
src_ip = sys.argv[2]
dst_ip = sys.argv[3]

def ls_subfolders(rootdir):
    sub_folders_n_files = []
    for path, _, files in os.walk(rootdir):
        for name in files:
            sub_folders_n_files.append(os.path.join(path, name))
    return sorted(sub_folders_n_files)

def ls_file_in_current_folder(path):
    return [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

def ls_folder_in_current_folder(path):
    return [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]

def packet_count(packets):
    count = 0
    for packet in packets:
        with open(f"packet_count-{service_name}.txt", "w") as f:
            if IP in packet and packet[IP].src == src_ip:
                count = count + 1
            f.write(f"{count}")
    print(count)

def packet_callback(packet):
    # print(f"client handle response packet {random.randint(1,1000)}")
    with open(f"end_time-{service_name}.txt", "w") as f:
        f.write(f"{time.time()}")

def client_sniff():
    print("client start sniff")
    sniff(filter=f"src {dst_ip} and icmp", prn=packet_callback)

def tcpreplay():
    start_time = ""
    end_time = ""

    store_path = '/home/onos/Desktop/output_rewrite/'   
    service_path = f'{store_path}{service_name}/'
    for i in range (100):
        print(f"===== {i} =====")
        for folder in ls_folder_in_current_folder(service_path):
            print("===============================")
            print(f"folder: {folder}")
            src = "h" + src_ip.split(".")[-1]
            dst = "h" + dst_ip.split(".")[-1]
            for file_path in ls_subfolders(os.path.join(service_path, folder, f"{src}-{dst}")):
                print(f"filepath: {file_path}")
                file_path = os.path.join(service_path, folder, file_path)
                packets = rdpcap(file_path)
                packet_count(packets)
                start_time = time.time()
                print("start replay")
                # subprocess.Popen(f'echo "rocks@123" | sudo -S -k tcpreplay -i {interface} -K {file_path}', shell=True, stdout=subprocess.PIPE, 
                #                           stderr=subprocess.PIPE).communicate()
                srp(packets, timeout=1, verbose=False)
                time.sleep(120)
                print("replay done")
                with open(f"end_time-{service_name}.txt", "r") as f1:
                    end_time = f1.read()
                print(f"timer {start_time} {end_time}")

                with open(f"packet_count-{service_name}.txt", "r") as f2:
                    count = int(f2.read())

                response_time = (float(end_time) - float(start_time)) / count
                    
                with open(f"response_time-{service_name}.txt", mode="a") as f3:
                    f3.write(f"'service_type': {service_name}, 'src_ip': {src_ip}, 'dst_ip': {dst_ip}, 'response_time': {response_time}\n")
                
                print(f"response_time: {response_time}")
                time.sleep(30)

if __name__ == '__main__':
    # threading.Thread(target=packet_count).start()
    threading.Thread(target=client_sniff).start()
    threading.Thread(target=tcpreplay).start()