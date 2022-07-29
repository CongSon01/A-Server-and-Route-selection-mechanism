import set_up_mininet
import json, os, time, random
import numpy as np
import requests
import sys, json
PATH_ABSOLUTE = "/home/onos/Downloads/A-Server-and-Route-selection-mechanism/flaskAPI/"

sys.path.append(PATH_ABSOLUTE+'handledata/models')
sys.path.append(PATH_ABSOLUTE+'core')
sys.path.append(PATH_ABSOLUTE+'run')
sys.path.append(PATH_ABSOLUTE+'api')

import CusTopo

# import from core
import connectGraph, Graph
import apiSDN
# import Server_Info, Server_Info_Full

class generate_topo_info:
    def __init__(self):
        self.list_ip = json.load(open('/home/onos/Downloads/A-Server-and-Route-selection-mechanism/flaskAPI/set_up/set_up_topo.json'))["controllers"]
        self.topo_network  = ''
        self.hosts  = ''
        self.servers  = ''
        self.graph = ''
        
        
    def get_api(self):
        # get full ip of SDN
        
        apiSDN.call_topo_api_sdn(self.list_ip)
        print("DOC XONG TOPO")
        apiSDN.call_host_api_sdn(self.list_ip)
        print("DOC XONG HOST")
        number_ip = len(self.list_ip) + 1

        topo_files = [PATH_ABSOLUTE + 'topos/topo_' + str(index_path) + '.json' for index_path in range(1, number_ip)]
        host_files = [PATH_ABSOLUTE + 'hosts/host_' + str(index_path) + '.json' for index_path in range(1, number_ip)]

        # sinh ra file hop nhat giua cac mang: topo.json va host.json 
        connectGraph.connectGraph(topo_files, host_files)

        # khoi tao topo rong
        self.topo_network = CusTopo.Topo()
        # add do thi topo.json va host.json vao topo
        self.graph = Graph.Graph(self.topo_network, 'topo.json', 'host.json')

        # get tap host va server tronng topo
        self.hosts  = self.topo_network.get_hosts()
        self.servers = self.topo_network.get_servers()

        name_hosts = [ip_host.replace('10.0.0.', 'h') for ip_host in self.hosts.keys()]
        name_servers = [ip_server.replace('10.0.0.', 'h') for ip_server in self.servers.keys()]
        # print("HOST: ",name_hosts)
        # print("SO HOST: " , len(name_hosts))
        # host_can = json.load(open('/home/onos/Downloads/flaskSDN/flaskAPI/set_up/set_up_topo.json'))["hosts"]
        # print("CAN: ", len(host_can))

        # print("SERVERS: ", name_servers)
        # print("SO SERVERS: " , len(name_servers))
        # server_can = json.load(open('/home/onos/Downloads/flaskSDN/flaskAPI/set_up/set_up_topo.json'))["servers"]
        # print("CAN: ", len(server_can))
        return name_hosts, name_servers

    def get_topo_from_api(self):
        return self.topo_network

    def get_graph_from_api(self):
        return self.graph

    def get_host_from_api(self):
        return self.hosts

    def get_server_from_api(self):
        return self.servers

def generate_topo(net, hosts_save):
    gtopo = generate_topo_info()
    name_hosts, name_servers = gtopo.get_api()
    print(name_hosts, name_servers)
    print(hosts_save)
    server_list = [ hosts_save[h] for h in  name_servers ]
    print(server_list)
    name_host = name_hosts

    period = set_up_mininet.PERIOD # random data from 0 to period 
    interval = set_up_mininet.INTERVAL # each host generates data 5 times randomly
    life_time = set_up_mininet.LIFE_TIME

    # khoi tao bang thoi gian cho tung host
    starting_table = create_starting_table( name_host, period, interval, life_time )
    write_table_to_file(starting_table, 'starting_table.json')
    
    # kich hoat server chuan bi lang nghe su dung iperf
    start_server(server_list, net)
    
    list_ip_server = list()
    for ip_server in server_list:
        list_ip_server.append(str(ip_server.IP()))

    # read file server and write to mongo
    for ip_server in list_ip_server:
        print("Ip server =", ip_server)
        # cmd_read_log = 'python readlog.py'+' '+ip_server + ' &'
        cmd_read_log = 'python readServerLog.py'+' '+ip_server + ' &'
        os.system(cmd_read_log)
        time.sleep(2)

    # print("Cho 10 phut")
    # time.sleep(60*10)
    next = input("Enter continues: ")
    if next == 'ok':
        run_shedule(starting_table,net,life_time)

def create_starting_table(host_list, period, interval, life_time):
    generate_flow = {}
    # generate_flow = {0: {'h2': 569, 'h1': 441}, 1: {'h2': 358, 'h1': 366}, 2: {'h2': 302, 'h1': 315}}
    for i in range(interval):
        temp = {}
        if i == 0:
            time_f = random.sample(range(3, period), len(host_list))
            for j in range(len(host_list)):
                temp[host_list[j]] = time_f[j]
        else:
            for h_i in host_list:
                temp[h_i] =  generate_flow[i-1][h_i] + life_time + random.randint(0, 3)
        generate_flow[i] = temp
    return generate_flow


# lay host tuong ung vs thoi gian
def get_host_affter_time(full_values, run_time):
    for cluster_host in full_values:
        for host in cluster_host:
            if cluster_host[host] == run_time:
                return str(host)

def changeLoss(node, lossPara):
    for intf in node.intfList(): # loop on interfaces of node
        if intf.link: # get link that connects to interface(if any)
            try:
                intfs = [ intf.link.intf1, intf.link.intf2 ] #intfs[0] is source of link and intfs[1] is dst of link
                intfs[0].config(loss=lossPara) 
                intfs[1].config(loss=lossPara)
            except:
                print("Link khong duoc su dung")

def run_shedule(generate_flow, net, life_time):
    print("generate_flow--------")
    # print(list(generate_flow.values()))
    
    full_times = sum([ list(start_host.values()) for start_host in list(generate_flow.values()) ], [])
    full_values = [ start_host for start_host in generate_flow.values() ]

    start_time = time.time()
    start_change_loss = time.time()
    stop_time = max(full_times)
    # print(min(full_times))
    nodes = net.switches + net.hosts
    while True:
        current_time = int(time.time() - start_time)
        # thay doi loss toan mang
        # if ( int(time.time() - start_change_loss) > random.randint(8, 15) ):
        #     for node in nodes:
        #         loss_new = random.choice(set_up_mininet.ARR_LOSS)
        #         changeLoss(node, loss_new)
        #     print("CHANGE LOSS")
        #     start_change_loss = time.time()


        # truyen goi tin
        if ( current_time >=  min(full_times) ):
            try:
                try: 
                    p = net.get(get_host_affter_time(full_values, current_time))
                except:
                    p = net.get('h1')

                print("HOST: ", p, " Chay luc ", current_time)
                des = call_routing_api_flask( p.IP() )
                print("TRUYEN DU LIEU ", p.IP(), "--->", des)
                # rate = random.randint(20000000, 60000000) #20^6 - 60*10^6 = 20Mb -> 60Mb
                # phan tram chiem dung bang thong
                # rate = np.random.uniform(set_up_mininet.MIN_IPERF, set_up_mininet.MAX_IPERF) #20^6 - 60*10^6 = 20Mb -> 60Mb
                # print("------------- gui du lieu-----------", rate)
                # plc_cmd =  'iperf -c %s -b %d -u -p 1337 -t %d &' %(des, rate, life_time)
                # p.cmd(plc_cmd)   
                # rate =  set_up_mininet.FILE_SIZE_MAX
                rate = random.randint(set_up_mininet.FILE_SIZE_MIN, set_up_mininet.FILE_SIZE_MAX)   #MG Byte
                print("------------- gui du lieu-----------", rate)
                plc_cmd = 'source /home/onos/Downloads/A-Server-and-Route-selection-mechanism/flaskAPI/get_reponding_time/venv/bin/activate; python /home/onos/Downloads/A-Server-and-Route-selection-mechanism/flaskAPI/get_reponding_time/cli-client.py %s -m b -p -s %d -srt >> ./server_info/%s.txt &' %(des, rate, des)
                p.cmd(plc_cmd)  

                full_times.remove(min(full_times))
            except:
                print("LOI KHI PING")

        if ( current_time > stop_time ):
            print("DONE")
            break
    print("OK")
  

def call_routing_api_flask(host):
    print("call flask")
    response = requests.post("http://10.20.0.201:5000/getIpServer", data= host)  
    dest_ip = response.text
    return str(dest_ip)


def start_server(set_server, net):
    strGet=''
    background_get_iperf_cmd=''

    # duyet qua kich hoat cac server 3 4
    print('------------------   PING SERVER  -----------------------')
    for server in set_server: 
        strGet=str(server)
        print(strGet)
        # get doi tuong server i
        p=net.get(str(server))
        
        # chay background nhan http server
        background_get_http_cmd = 'source /home/onos/Downloads/A-Server-and-Route-selection-mechanism/flaskAPI/get_reponding_time/venv/bin/activate;python /home/onos/Downloads/A-Server-and-Route-selection-mechanism/flaskAPI/get_reponding_time/http-fastapi-server.py &'
        p.cmd(background_get_http_cmd)



def write_table_to_file(table, name_file):
    with open(name_file, "w") as outfile:
        json.dump(table, outfile)


