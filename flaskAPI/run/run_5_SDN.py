#!/usr/bin/python3
import requests
import os.path
from topozoo_mininet import TopologyZooXML
from zipfile import ZipFile
import time
import pandas as pd
from requests.auth import HTTPBasicAuth
import random
import os
import numpy as np
import random, json
from os import path

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
        from mininet.node import CPULimitedHost, Host, Node
        from mininet.node import OVSKernelSwitch, UserSwitch
        from mininet.node import IVSSwitch
        from mininet.cli import CLI
        from mininet.log import setLogLevel, info
        from mininet.link import TCLink, Intf
        from subprocess import call
        import ipaddress

        def myNetwork():
            net = Mininet( topo=None,
                        build=False,
                        ipBase='10.0.0.0/8')

            info( '*** Adding controller\n' )
            controller = None
            list_c = [None, None, None, None]
            c_controllers = ['c0', 'c1', 'c2', 'c3']
            # c_controllers = ['c0']
            print(self.controller_ip_s)
            print(c_controllers)
            if self.controller_type == "controller":
                controller = Controller
                self.controller_port = 6653
                for c in range(len(c_controllers)):
                    list_c[c]=net.addController(name=c_controllers[c],
                        controller=controller,
                        protocol='tcp',
                        port=self.controller_port)
                
                
            elif self.controller_type =="remote":
                controller = RemoteController
                for c in range(len(c_controllers)):
                    list_c[c]=net.addController(name=c_controllers[c],
                    controller=controller,
                    protocol='tcp',
                    ip=self.controller_ip_s[c],
                    port=self.controller_port)
                
                
            elif self.controller_type == "ovscontroller":
                controller = OVSController
                self.controller_port = 6633
                for c in range(len(c_controllers)):
                    list_c[c]=net.addController(name=c_controllers[c],
                        controller=controller,
                        protocol='tcp',
                        port=self.controller_port)
            else:
                for c in range(len(c_controllers)):
                    list_c[c]=net.addController(name=c_controllers[c],
                        controller=RemoteController,
                        protocol='tcp',
                        ip=self.controller_ip_s[c],
                        port=self.controller_port)
                
            info( '*** Add switches\n')
            switches = {}
            added_switches={}
            for (first,second,node_type) in self.topology_graph:
                if node_type == "s":
                    if first[1] not in added_switches:
                        switches[first[1]] = net.addSwitch('s'+str(first[1]+1), cls=OVSKernelSwitch)
                        added_switches[first[1]] = True
                    if second[1] not in added_switches:
                        switches[second[1]] = net.addSwitch('s'+str(second[1]+1), 
                        cls=OVSKernelSwitch)
                        added_switches[second[1]] = True
                    

            info( '*** Add hosts\n')
            hosts= []
            
            first_ip = '10.0.0.0'
            ##########################################################################################################
            sw_0 = [10,11,12,15,16,17,13]
            sw_1 = [4,5,7,8,9]
            sw_2 = [0,1,2,3,6,14,19,25,26]
            sw_3 = [18,20,21,22,23,24,27]
            # sw_0 = []
            # total_sw = np.arange(0,int(len(switches)))
            
            # sw_1 = list(set(total_sw) - set(sw_0))
            # sw_0 = np.arange(0,int(len(switches)))
            # sw_1 = np.arange(100, 101)

            sw_in_c0 = ['s'+str(i+1) for i in sw_0]
            sw_in_c1 = ['s'+str(i+1) for i in sw_1]
            sw_in_c2 = ['s'+str(i+1) for i in sw_2]
            sw_in_c3 = ['s'+str(i+1) for i in sw_3]
            # sw_in_c1 = ['s'+str(i+1) for i in sw_1]
            # print(sw_in_c1)
            # not_host = ['h8', 'h9', 'h10', 'h11']
            # not_host = ['h1', 'h3']
            # switch_not_host = [1,7,6,13]  # day la index khong phai ten switch
            switch_not_host = []
            for (first,second,node_type) in sorted(self.topology_graph):
                if node_type == "h":
                    # if first[1] not in switch_not_host:
                    hosts.append(net.addHost('h'+str(first[1]+1), cls=Host, ip=str(ipaddress.IPv4Address(int(ipaddress.IPv4Address(first_ip))+first[1]+1)), defaultRoute=None))   
                    # else:
                        # print("remove host " + str(first[1] + 1))
            info( '*** Add links\n' )
            # switch_not_host = ['s0', 's1', 's23', 's24']
            # switch_not_host = ['s0', 's52']

            # switch_not_host = [1,2,6,13]
            n = len(switches)
            Matrix_graph = [[0 for x in range(n)] for y in range(n)] 

            filename = '/home/onos/Downloads/flaskSDN/flaskAPI/run/bridge.txt'
            bridge = [['s11', 's18'], ['s2','s14'], ['s7', 's8'], ['s25', 's26'], ['s20', 's28']]

            switch_bridge = ['s11', 's18', 's2','s14', 's7', 's8', 's25', 's26','s20', 's28']
            
            for (first,second,node_type) in self.topology_graph:
                try:
                    if node_type=="h":
                        net.addLink(hosts[first[1]],switches[second[1]], bw=10, delay='0ms', loss=1, use_htb=True)
                        if ( str(switches[second[1]]) in switch_bridge ):
                            print("HOST Bien ", hosts[first[1]], " - ", first[1])

                    elif node_type=="s":
                        # Tao matrix de cat canh
                        Matrix_graph[int(first[1])][int(second[1])] = 1
                        Matrix_graph[int(second[1])][int(first[1])] = 1

                        # Luu cac canh noi vao file
                        if [str(switches[first[1]]), str(switches[second[1]])] in bridge:
                            print("BIEN", str(switches[first[1]].dpid), str(switches[second[1]].dpid))
                            net.addLink(switches[first[1]],switches[second[1]], port1= 10, port2=10, bw=10, delay='0ms', loss=1, use_htb=True)

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
                            net.addLink(switches[first[1]],switches[second[1]], bw=10, delay='0ms', loss=1, use_htb=True)



                    # elif node_type=="h":
                    #     if ( str(switches[second[1]]) not in switch_not_host ):
                    #         net.addLink(hosts[first[1]],switches[second[1]], bw=10, delay='0ms', loss=1, use_htb=True)
                except KeyError as e:
                    print("switch or host is unavailable: {}".format(e))
            info ('*** Get Matrix_graph\n')
            # https://graphonline.ru/en/ vẽ rồi cắt
            np.savetxt('graph_matrix.txt',Matrix_graph, fmt='%s')
            
            info( '*** Starting network\n' )
            net.build()

            info( '*** Starting controllers\n' )
            for controller in net.controllers:
                controller.start()

            info( '*** Starting switches\n')
            
            for i_sw in sw_0:
                if i_sw < len(switches):
                    print('add controller 0 ' , switches[i_sw] , ' ', switches.get(i_sw).dpid)
                    switches.get(i_sw).start([list_c[0]])
            
            for i_sw in sw_1:
                if i_sw < len(switches):
                    print('add controller 1 ' , switches[i_sw] , ' ' ,  switches.get(i_sw).dpid)
                    switches.get(i_sw).start([list_c[1]])
            
            for i_sw in sw_2:
                if i_sw < len(switches):
                    print('add controller 2 ' , switches[i_sw] , ' ' ,  switches.get(i_sw).dpid)
                    switches.get(i_sw).start([list_c[2]])
            
            for i_sw in sw_3:
                if i_sw < len(switches):
                    print('add controller 3 ' , switches[i_sw] , ' ' ,  switches.get(i_sw).dpid)
                    switches.get(i_sw).start([list_c[3]])

            info( '*** Post configure switches and hosts\n')
            # time.sleep(15)
            # net.pingAll()

            # net.getNodeByName('h1')

            ######## ping all cac host voi nhau
            # print(hosts)
            p=net.get('h1')
            print(type(p.IP()))
            print((p.IP()))

            host_1 = hosts[0]
            for h in range( len(hosts) ):
                host_i = hosts[h]
                net.ping( [host_1, host_i] )
            
            # time.sleep(15)


            generate_topo(net)
            CLI(net)
            
            # net.stop()

        setLogLevel( 'info' )
        myNetwork()

def generate_topo(net):
    host_list, server_list = create_host_server(net)
    num_host = len(host_list) 
    num_server = len(server_list) 
    # print("So host =", num_host, " So server=", num_server) 
    print("HOSTS: ", host_list)
    print("SERVERS: ", server_list)

    print("Vd 1 host: ", str(host_list[0]))
    print("Vd 1 host: ", host_list[0].IP())

    period = 60*10 # random data from 0 to period 
    interval = 10 # each host generates data 5 times randomly

    # khoi tao bang thoi gian cho tung host
    starting_table = create_starting_table(num_host, period, interval)
    write_table_to_file(starting_table, 'starting_table.csv')
    
    # kich hoat server chuan bi lang nghe su dung iperf
    start_server(server_list, net)
    
    list_ip_server = list()
    for ip_server in server_list:
        list_ip_server.append(str(ip_server.IP()))
    
    name_host = list()
    for ip_host in host_list:
        name_host.append(str(ip_host))
        

    print("list IP server")
    print(list_ip_server)
    print("list Name host")
    print(name_host)

    # read file server and write to mongo
    for ip_server in list_ip_server:
        print("Ip server =", ip_server)
        cmd_read_log = 'python readlog.py'+' '+ip_server + ' &'
        os.system(cmd_read_log)
        # print("Read log")
        # print(cmd_read_log)
        time.sleep(1)

    print("Cho 3 phut")
    time.sleep(60*3)

    # # lap lich cho host
    run_shedule(starting_table, period, interval,net, name_host)

def create_starting_table(num_host, period, interval):
    starting_table =  np.zeros( (num_host, interval) )
    s = 0 # random starting time

    for h in range( len(starting_table) ):
        for t in range( len(starting_table[h]) ):
            s = random.uniform(0, period) # do t = 0 to 100

            starting_table[h][t] = s
        starting_table[h].sort()

    #print(starting_table)
    return starting_table
   

def run_shedule(starting_table, period, interval, net, name_host):
    visited = np.full( ( len(starting_table), interval), False, dtype=bool )
    dem = 0
    begin= time.time()
    # ban dau current la moc 0
    current= float(time.time() - begin) # giay hien tai - giay goc = giay current tai moc 0
    #counter time
    counter=float(period+3) # theo doi trong n giay period
    print("print ok after "+str(counter)+"s")

    while(counter-float(current)>0.001): #quan sat trong 10s
        current = time.time() - begin
        #print("current = ", current)
        for host in range ( len(starting_table) ):
            for t in range ( len(starting_table[host])):
                # sai so be hon 0.001
                if  abs (starting_table[host][t] - current ) < 0.001 and visited[host][t] == False:
                    
                        # get doi tuong host i
                        # p=net.get('h%s' %(host+1))
                        print("HOST = ", str(name_host[host]))
                        p = net.get(str(name_host[host]))
                    
                    # # neu object hien tai la host thi tien hanh goi iperf
                    # if p in host_list:
                        # get dich den server cua host i
                        # print(type(p.IP()))
                        des = call_routing_api_flask( p.IP() )
                    
                        #plc_cmd = 'iperf -c %s -p 1337 -t 1000 &' %des
                        # truyen data den ip cua dest voi duration = 60s
                        print("TRUYEN DU LIEU ", p.IP(), "--->", des)

                        # phan tram chiem dung bang thong
                        rate = random.randint(1000000, 8000000) #10^6 - 8*10^6
                        print("------------- gui du lieu-----------", rate)
                        plc_cmd =  'iperf -c %s -b %d -u -p 1337 -t 600 &' %(des, rate)
                        p.cmd(plc_cmd)   
                        #print(plc_cmd)
                        #print("host", host + 1, " --> ", des, "tai giay thu", starting_table[host][t])
                        dem += 1
                        visited[host][t] = True
    print("ok, dem = ", dem)
  
def create_host_server(net):
    host_list = list()
    server_list = list()

    index_hosts = json.load(open('/home/onos/Downloads/flaskSDN/flaskAPI/set_up/hosts.json'))['hosts']
    # /home/onos/Downloads/flaskSDN/flaskAPI/set_up/hosts.json
    index_servers = json.load(open('/home/onos/Downloads/flaskSDN/flaskAPI/set_up/servers.json'))['servers']

    for h in index_hosts:
        host_list.append(net.hosts[h])
    
    for h in index_servers:
        server_list.append(net.hosts[h])

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
    df = pd.DataFrame(table)
    df.to_csv(name_file)
    

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

    # parser.add_argument('--toponame', dest='topo_name', help="Topology name e.g. AttMpls",required=False,type=str, default='AttMpls')
    parser.add_argument('--toponame', dest='topo_name', help="Topology name e.g. Darkstrand",required=False,type=str, default='Darkstrand')
    # parser.add_argument('--toponame', dest='topo_name', help="Topology name e.g. Epoch",required=False,type=str, default='Epoch')
    parser.add_argument('--cport', dest='controller_port', help="Controller port in mininet, default value is 6653.",required=False,type=int,default=6653)

    parser.add_argument('--controller', dest='controller_type', help="Default controller is mininet controller, other options: remote,ovscontroller",required=False,type=str,default="remote")

    args = parser.parse_args()


    import tempfile
    tmp_dir = tempfile.gettempdir()

    archive_path = os.path.join(tmp_dir,"archive.zip")
    download_if_not_exists("http://www.topology-zoo.org/files/archive.zip",archive_path)
    extract (archive_path,os.path.join(tmp_dir,"topologyzoo"))

    if args.avail_topo:
        print_all_topos(os.path.join(tmp_dir,"topologyzoo"))
        exit(0)
    import sys
    if  args.topo_name==None:
        print ("you must specify at least one of the switches, use \"{} -h\" for help.".format(sys.argv[0]))
        exit(1)
        
    list_ip = json.load(open('/home/onos/Downloads/flaskSDN/flaskAPI/set_up/ip_SDN.json'))['ip_sdn']
    tzoo2= TopologyZooXML(os.path.join(tmp_dir,"topologyzoo",args.topo_name+".graphml"))
    m = Mininet(tzoo2.get_topology(), list_ip ,args.controller_port,args.controller_type)   
    # sudo python3 -E run_5_SDN.py