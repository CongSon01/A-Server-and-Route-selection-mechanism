#!/usr/bin/python3
import requests
import os.path
from topozoo_mininet import TopologyZooXML
from zipfile import ZipFile
import time
import pandas as pd
import os
import numpy as np
import random, json
import set_up_mininet

os.system('sudo mn -c')
os.system('sudo mn -c')
set_up_topo = json.load(open('/home/onos/Downloads/flaskSDN/flaskAPI/set_up/set_up_topo.json'))

class Mininet:
    def __init__(self,topology_graph, list_ip , controller_port, controller_type):
        self.topology_graph = topology_graph
        self.controller_ip_s = list_ip
        self.controller_port = controller_port
        self.controller_type = controller_type
        self.run_topo()

    def run_topo(self):
        from mininet.net import Mininet
        from mininet.node import Controller, RemoteController, OVSController
        from mininet.node import Host
        from mininet.node import OVSKernelSwitch
        from mininet.cli import CLI
        from mininet.log import setLogLevel, info
        import ipaddress

        def myNetwork():
            net = Mininet( topo=None, build=False )

            info( '*** Adding controller\n' )
            controller = None

            number_controllers = len(set_up_topo['switch_in_controllers'])
            list_controllers = [None for i in range(number_controllers)]
            list_name_controllers = ['c'+str(i) for i in range(number_controllers) ]

            print(self.controller_ip_s)
            print(list_name_controllers)
            if self.controller_type == "controller":
                controller = Controller
                self.controller_port = 6653
                for c in range(len(list_name_controllers)):
                    list_controllers[c]=net.addController(name=list_name_controllers[c],
                        controller=controller,
                        protocol='tcp',
                        port=self.controller_port)
                
                
            elif self.controller_type =="remote":
                controller = RemoteController
                for c in range(len(list_name_controllers)):
                    list_controllers[c]=net.addController(name=list_name_controllers[c],
                    controller=controller,
                    protocol='tcp',
                    ip=self.controller_ip_s[c],
                    port=self.controller_port)
                
                
            elif self.controller_type == "ovscontroller":
                controller = OVSController
                self.controller_port = 6633
                for c in range(len(list_name_controllers)):
                    list_controllers[c]=net.addController(name=list_name_controllers[c],
                        controller=controller,
                        protocol='tcp',
                        port=self.controller_port)
            else:
                for c in range(len(list_name_controllers)):
                    list_controllers[c]=net.addController(name=list_name_controllers[c],
                        controller=RemoteController,
                        protocol='tcp',
                        ip=self.controller_ip_s[c],
                        port=self.controller_port)
                
            info( '*** Add switches\n')
            switches = {}
            added_switches={}
            hosts_remove = set_up_topo['host_remove']
            MAX_CAPACITY_BW = set_up_mininet.MAX_CAPACITY_BW
            LOSS_PER = set_up_mininet.LOSS_PER
            LINK_DELAY = set_up_mininet.LINK_DELAY

            for (first,second,node_type) in self.topology_graph:
                if node_type == "s":
                    # if first[1] in hosts_remove or second[1] in hosts_remove:
                    #     continue
                    if first[1] not in added_switches:
                        switches[first[1]] = net.addSwitch('s'+str(first[1]+1), cls=OVSKernelSwitch)
                        added_switches[first[1]] = True
                    if second[1] not in added_switches:
                        switches[second[1]] = net.addSwitch('s'+str(second[1]+1), cls=OVSKernelSwitch)
                        added_switches[second[1]] = True
                    

            info( '*** Add hosts\n')
            hosts= []
            
            first_ip = '10.0.0.0'

            for (first,second,node_type) in sorted(self.topology_graph):
                if node_type == "h":
                    # if first[1] in hosts_remove:
                    #     continue
                    # else:
                    hosts.append(net.addHost('h'+str(first[1]+1), cls=Host, ip=str(ipaddress.IPv4Address(int(ipaddress.IPv4Address(first_ip))+first[1]+1)), defaultRoute=None))   
                
            info( '*** Add links\n' )
            # luu lai topo dang matrix

            n = len(hosts)
            print(n)
            Matrix_graph = [[0 for x in range(n)] for y in range(n)] 

            filename = '/home/onos/Downloads/flaskSDN/flaskAPI/run/bridge.txt'
            bridges = set_up_topo['bridge']

            # flatten_bridge = sum(bridge, [])
            
            for (first,second,node_type) in self.topology_graph:
                try:
                    if node_type=="h":
                        # print(hosts[first[1]].ipBase,switches[second[1]].dpid)
                        net.addLink(hosts[first[1]],switches[second[1]], delay=LINK_DELAY, loss=LOSS_PER, bw=MAX_CAPACITY_BW, use_htb=True)
                        if ( str(switches[second[1]]) in bridges ):
                            print("HOST Bien ", hosts[first[1]], " - ", first[1])

                    elif node_type=="s":
                        # Tao matrix de cat canh
                        # print(int(first[1]), int(second[1]))
                        Matrix_graph[int(first[1])][int(second[1])] = 1

                        # print("CANH: " , int(str(switches[first[1]]).replace('s', ''))," --> ", int(str(switches[second[1]]).replace('s', '')))

                        # Luu cac canh noi vao file
                        if [int(str(switches[first[1]]).replace('s', '')), int(str(switches[second[1]]).replace('s', ''))] in bridges:
                            print("BIEN", str(switches[first[1]].dpid), str(switches[second[1]].dpid))
                            net.addLink(switches[first[1]],switches[second[1]], port1= 10, port2=10, delay=LINK_DELAY, loss=LOSS_PER, bw=MAX_CAPACITY_BW, use_htb=True)

                            with open(filename, 'a') as outfile:
                                entry = {"src": {
                                            "port": 10,
                                            "id": "of:" + str(switches[first[1]].dpid)
                                        },
                                        "dst": {
                                            "port": 10,
                                            "id": "of:" + str(switches[second[1]].dpid)
                                        }}
                                outfile.write(json.dumps(entry))
                                outfile.write("\n")
                                entry = {"src": {
                                            "port": 10,
                                            "id": "of:" + str(switches[second[1]].dpid)
                                        },
                                        "dst": {
                                            "port": 10,
                                            "id": "of:" + str(switches[first[1]].dpid)
                                        }}
                                outfile.write(json.dumps(entry))
                                outfile.write("\n")
                                outfile.close()
                        else:
                            net.addLink(switches[first[1]],switches[second[1]], delay=LINK_DELAY, loss=LOSS_PER, bw=MAX_CAPACITY_BW, use_htb=True)

                except KeyError as e:
                    print("switch or host is unavailable: {}".format(e))

            info ('*** Get Matrix_graph\n')
            # https://graphonline.ru/en/ vẽ rồi cắt
            np.savetxt('graph_matrix.txt',Matrix_graph, fmt='%s')
            
            info( '*** Starting network\n' )
            net.build()   # sinh ip cho cac host

            info( '*** Starting controllers\n' )
            for controller in net.controllers:
                controller.start()

            info( '*** Starting switches\n')

            # add switch vao controller
            switch_in_controllers = set_up_topo['switch_in_controllers']
            for controller in switch_in_controllers:
                for i_sw in switch_in_controllers[controller]:
                    self.add_sw_to_controller(list_controllers[int(controller.split('_')[1])], switches.get(i_sw), hosts[i_sw])
            

            ######## ping all cac host voi nhau
            # self.ping_one_to_all(net, hosts, hosts_remove)
            self.ping_host_in_sdn(net,hosts, switch_in_controllers)
            # net.pingAll()

            kq = input("Nhap index host and serer:")

            if kq == 'ok':
                generate_topo(net)
                CLI(net)
            
            net.stop()

        setLogLevel( 'info' )
        myNetwork()
    
    def add_sw_to_controller(self, controller, switch, host):
        print('add controller ', controller, ' : ' , switch , ' ' ,  switch.dpid, host)
        switch.start( [controller] )

    
    def ping_host_in_sdn(self, net,hosts, switch_in_controllers):
        for key in switch_in_controllers:
            for i in switch_in_controllers[key]:
                net.ping( [hosts[switch_in_controllers[key][0]], hosts[i]] )
        return 

def generate_topo(net):
    host_list, server_list = create_host_server(net)

    print("HOST")
    for host in host_list:
        print(host.IP())
    
    print("SERVER")
    for server in server_list:
        print(server.IP())
    
    name_host = list()
    for ip_host in host_list:
        name_host.append(str(ip_host))

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
        cmd_read_log = 'python readlog.py'+' '+ip_server + ' &'
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
            for h_i in host_list:
                temp[h_i] = random.randint(1, period)
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

def run_shedule(generate_flow, net, life_time):
    print("generate_flow--------")
    print(list(generate_flow.values()))
    
    full_times = sum([ list(start_host.values()) for start_host in list(generate_flow.values()) ], [])
    full_values = [ start_host for start_host in generate_flow.values() ]

    start_time = time.time()
    stop_time = max(full_times)
    while True:
        current_time = int(time.time() - start_time)
        if ( current_time in  full_times):
            p = net.get(get_host_affter_time(full_values, current_time))
            print("HOST: ", p, " Chay luc ", current_time)
            des = call_routing_api_flask( p.IP() )
            # des = "10.0.0.4"
            print("TRUYEN DU LIEU ", p.IP(), "--->", des)
            

                      
            # rate = random.randint(20000000, 60000000) #20^6 - 60*10^6 = 20Mb -> 60Mb
            # phan tram chiem dung bang thong
            rate = np.random.uniform(set_up_mininet.MIN_IPERF, set_up_mininet.MAX_IPERF) #20^6 - 60*10^6 = 20Mb -> 60Mb
            print("------------- gui du lieu-----------", rate)
            plc_cmd =  'iperf -c %s -b %d -u -p 1337 -t %d &' %(des, rate, life_time)
            p.cmd(plc_cmd)   

        if ( current_time == stop_time ):
            print("DONE")
            break
    print("OK")
  
def create_host_server(net):

    index_hosts = set_up_topo['hosts']
    index_servers = set_up_topo['servers']

    host_list = [ net.hosts[h] for h in index_hosts ]
    
    server_list = [ net.hosts[h] for h in index_servers ]

    return (host_list, server_list)

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

        # chay background nhan iperf
        background_get_iperf_cmd = 'iperf -s -u -p 1337 -i 1 > ./BW_server/%s.txt &' %server.IP()
        p.cmd(background_get_iperf_cmd)


def write_table_to_file(table, name_file):
    with open(name_file, "w") as outfile:
        json.dump(table, outfile)
    

def download_file(filename, url):
    """
    Download an URL to a file
    """
    with open(str(filename), 'wb') as fout:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        # Write response data to file
        for block in response.iter_content(4096):
            fout.write(block)
            
def download_if_not_exists(url,filename):
    """
    Download a URL to a file if the file
    does not exist already.
    Returns
    -------
    True if the file was downloaded,
    False if it already existed
    """
    if not os.path.exists(str(filename)):
        download_file(filename, url)
        return True
    return False

def extract (zip_file_path,destination_path):
    # Create a ZipFile Object and load sample.zip in it
    with ZipFile(zip_file_path, 'r') as zipObj:
        # Extract all the contents of zip file in different directory
        zipObj.extractall(destination_path)


def get_file_names_in_a_directory(dir):
    """
    Get all files in a directory dir
    """
    import os
    files = sorted([f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))])
    return files


def print_all_topos(extracted_dir):
    """
    Print all available topologies
    """
    for file_name in get_file_names_in_a_directory(extracted_dir):      
        if file_name.endswith(".graphml"):
            print(file_name.replace(".graphml",""))


if __name__=="__main__":

    import argparse
    parser = argparse.ArgumentParser(
        description='This script is a fast way to run topology\'s that are available in topologyzoo.com on mininet!')

    parser.add_argument('--availtopo', dest='avail_topo', help="prints list of all available topologies and exit.",required=False,action="store_true")
    args = parser.parse_args()


    import tempfile
    tmp_dir = tempfile.gettempdir()

    archive_path = os.path.join(tmp_dir,"archive.zip")
    download_if_not_exists("http://www.topology-zoo.org/files/archive.zip",archive_path)
    extract (archive_path,os.path.join(tmp_dir,"topologyzoo"))

    if args.avail_topo:
        print_all_topos(os.path.join(tmp_dir,"topologyzoo"))
        exit(0)

    topo_name = set_up_topo['name_topo']
    controller_port = set_up_topo['controller_port']
    controller_type = set_up_topo['controller_type']
        
    list_ip = set_up_topo['ip_sdn']
    tzoo2= TopologyZooXML(os.path.join(tmp_dir,"topologyzoo",topo_name+".graphml"))
    m = Mininet(tzoo2.get_topology(), list_ip ,controller_port,controller_type)   
    # sudo python3 -E run_mininet2.py