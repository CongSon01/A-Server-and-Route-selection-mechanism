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
import random

class Mininet:
    def __init__(self,topology_graph,controller_ip_0,controller_ip_1,controller_port,controller_type):
        self.topology_graph = topology_graph
        self.controller_ip_0 = controller_ip_0
        self.controller_ip_1 = controller_ip_1
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
            c0 = None
            c1 = None
            if self.controller_type == "controller":
                controller = Controller
                self.controller_port = 6653
                c0=net.addController(name='c0',
                    controller=controller,
                    protocol='tcp',
                    port=self.controller_port)
                c1=net.addController(name='c1',
                      controller=controller,
                      protocol='tcp',
                      port=self.controller_port)
                
            elif self.controller_type =="remote":
                controller = RemoteController
                c0=net.addController(name='c0',
                    controller=controller,
                    protocol='tcp',
                    ip=self.controller_ip_0,
                    port=self.controller_port)
                c1=net.addController(name='c1',
                    controller=controller,
                    protocol='tcp',
                    ip=self.controller_ip_1,
                    port=self.controller_port)
                
            elif self.controller_type == "ovscontroller":
                controller = OVSController
                self.controller_port = 6633
                c0=net.addController(name='c0',
                    controller=controller,
                    protocol='tcp',
                    port=self.controller_port)
                c1=net.addController(name='c1',
                    controller=controller,
                    protocol='tcp',
                    port=self.controller_port)
            else:
                c0=net.addController(name='c0',
                                controller=controller,
                                protocol='tcp',
                                ip=self.controller_ip_0,
                                port=self.controller_port)
                c1=net.addController(name='c1',
                                controller=controller,
                                protocol='tcp',
                                ip=self.controller_ip_1,
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
            sw_0 = [0, 1, 2, 3, 6, 14, 25, 26, 19, 27, 18, 22, 21, 20, 23, 24]
            # sw_0 = []
            total_sw = np.arange(0,int(len(switches)))
            
            sw_1 = list(set(total_sw) - set(sw_0))
            # sw_0 = np.arange(0,int(len(switches)))
            # sw_1 = np.arange(100, 101)

            sw_in_c0 = ['s'+str(i+1) for i in sw_0]
            sw_in_c1 = ['s'+str(i+1) for i in sw_1]
            print(sw_in_c0)
            print(sw_in_c1)
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
            # switch_not_host = []
            n = len(switches)
            Matrix_graph = [[0 for x in range(n)] for y in range(n)] 
            # print(hosts)
            # print(switches)
            for (first,second,node_type) in self.topology_graph:
                try:
                    if node_type=="h":
                        if ( second[1] not in switch_not_host ):
                            ####################################### Trung doc lenh
                            print('sw_',second[1] + 1, ' connected to ', hosts[first[1]])
                            
                            net.addLink(hosts[first[1]],switches[second[1]], bw=10, delay='0ms', loss=0, use_htb=True)
                            

                    elif node_type=="s":
                        # name_connect = str(node_1 +'_'+node_2)
                        # if node_1 in sw_in_c0 and node_2 in sw_in_c1:
                        #     print('-Not connenct', name_connect)
                        #     continue
                        
                        # if node_1 in sw_in_c1 and node_2 in sw_in_c0 :
                        #     print('-Not connenct', name_connect)
                        #     continue
                            # net.addLink(switches[first[1]],switches[second[1]], port1= 10, port2=10, bw=10, delay='0ms', loss=0, use_htb=True)
                        
                        
                        Matrix_graph[int(first[1])][int(second[1])] = 1
                        if first[1] == 1 and second[1] == 13 :
                            print('--BIEN--', switches[first[1]]  , '_____________', switches[second[1]])
                            net.addLink(switches[first[1]],switches[second[1]], port1= 10, port2=10, bw=10, delay='0ms', loss=0, use_htb=True)
                        elif first[1] == 6 and second[1] == 7 :
                            print('--BIEN--', switches[first[1]] , '_____________', switches[second[1]])
                            net.addLink(switches[first[1]],switches[second[1]], port1= 10, port2=10, bw=10, delay='0ms', loss=0, use_htb=True)
                        else:
                            net.addLink(switches[first[1]],switches[second[1]], bw=10, delay='0ms', loss=0, use_htb=True)
                            print('+Connenct', first[1], second[1])
                    # elif node_type=="h":
                    #     if ( str(switches[second[1]]) not in switch_not_host ):
                    #         net.addLink(hosts[first[1]],switches[second[1]], bw=10, delay='0ms', loss=0, use_htb=True)
                except KeyError as e:
                    print("switch or host is unavailable: {}".format(e))


            # add bien
            # net.addLink(switches[1],switches[52], port1= 10, port2=10, bw=10, delay='0ms', loss=0, use_htb=True)
            # net.addLink(switches[0],switches[24], port1= 10, port2=10, bw=10, delay='0ms', loss=0, use_htb=True)
            # net.addLink(switches[1],switches[5], port1= 10, port2=10, bw=10, delay='0ms', loss=0, use_htb=True)
            info ('*** Get Matrix_graph\n')
            # https://graphonline.ru/en/ vẽ rồi cắt
            np.savetxt('graph_matrix.txt',Matrix_graph, fmt='%s')
            
            info( '*** Starting network\n' )
            net.build()

            info( '*** Starting controllers\n' )
            for controller in net.controllers:
                controller.start()

            info( '*** Starting switches\n')
            # len_switches = len(switches)
            # index_split = int(len_switches/2)
            # i_sw = 0
            # print(index_split)
            # # sw.start([c0])
            # for _,sw in switches.items():
            #     if (i_sw <= index_split):
            #         print('add controller 1', sw)
                # sw.start([c0])
            #     else:
            #         print('add controller 2', sw)
            #         sw.start([c1])
            #     i_sw += 1

            # sw_0 = [0, 1, 2, 9, 10] # 's1', 's2', 's3', 's10', 's11'
            # sw_1 = [3 ,4, 5, 6, 7, 8] # 's4', 's5', 's6', 's7', 's8', 's9'
            
            for i_sw in sw_0:
                if i_sw < len(switches):
                    print('add controller 0', switches.get(i_sw))
                    switches.get(i_sw).start([c0])
            for i_sw in sw_1:
                if i_sw < len(switches) :
                    print('add controller 1', switches.get(i_sw))
                    switches.get(i_sw).start([c1])

            info( '*** Post configure switches and hosts\n')
            # time.sleep(15)
            # CLI(net)
            # net.pingAll()

            # net.getNodeByName('h1')

            ######## ping all cac host voi nhau
            print("hostssssssssssssssssssssssssssssssssssssssssss")
            # print(hosts)

            host_1 = hosts[0]
            for h in range( len(hosts) ):
                host_i = hosts[h]
                net.ping( [host_1, host_i] )


            # host_i = net.getNodeByName( "h1" )
            # switch_i = net.getNodeByName( "s1" )


            # for h in :
            #     host_list.append(net.hosts[h])

            # print("typeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee", host_i)
            # net.ping( [host_i, switch_i] )
            
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


    print("------------------   server  -----------------------")
    print(server_list)

    period = 1000 # random data from 0 to period 
    interval = 10 # each host generates data 5 times randomly

    # khoi tao bang thoi gian cho tung host
    starting_table = create_starting_table(num_host, period, interval)
    write_table_to_file(starting_table, 'starting_table.csv')
    
    # kich hoat server chuan bi lang nghe su dung iperf
    start_server(num_server, net)
    print("Tat reactive va bat flask trong 1 phut")
    
    list_ip_server = list()
    for ip_server in server_list:
        list_ip_server.append(str(ip_server.IP()))
        

    print("list IP server")
    print(list_ip_server)
    
    # read file server and write to mongo
    for ip_server in list_ip_server:
        os.system('python readlog.py'+' '+ip_server+' &')
        time.sleep(1)
    time.sleep(60)

    # lap lich cho host
    #run_shedule(starting_table, period, interval,net, host_list)

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

def run_shedule(starting_table, period, interval, net, host_list):
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
                        p=net.get('h%s' %(host+1))
                    
                    # # neu object hien tai la host thi tien hanh goi iperf
                    # if p in host_list:
                        # get dich den server cua host i
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
    # ban dau tap net.hosts co 1,2 ... 11 con
    host_list = list()
    server_list = list()

    # index_hosts = [0, 2]
    # index_servers = [3, 4]
    index_hosts = [20, 21, 23, 22]
    index_servers = [11,10,17]

    for h in index_hosts:
        host_list.append(net.hosts[h])
    
    for h in index_servers:
        server_list.append(net.hosts[h])

    # for h in range( len(net.hosts) ):
    #     if h <=4:   # host 1 2 3 4 5
    #         host_list.append( net.hosts[h])
    #     else: # server 3 4
    #         server_list.append( net.hosts[h])

    return (host_list, server_list)

def call_routing_api_flask(host):
    print("call flask")
    response = requests.post("http://10.20.0.250:5000/getIpServer", data= host)  
    dest_ip = response.text
    return str(dest_ip)

def start_server(num_host, net):
    """
    Kjch hoat server de truyen iperd
    """
    #p1, p2, p3,p4,p5,p6,p7,p8 = net.get('h1', 'h2', 'h3','h4', 'h5', 'h6','h7', 'h8')
    # p1, p2, p3, p4, p5, p6, p7 = net.get('h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7')

    # net.get all
    # for i in range(num_host):
    # print('------------------   get all  -----------------------')
    # for i in range(1, num_host+1):
    #     print('get host', i)
    #     net.get('h%s' %(i))

    plc1_cmd=''
    strGet=''
    plc2_cmd=''

    # set_server theo ten server h12, h11, h18
    set_server = [11,12,18]
    # set_server = [3,4]
    # i=6

    # duyet qua kich hoat cac server 3 4
    print('------------------   PING SERVER  -----------------------')
    for i in set_server: 
        # ping server i
        plc1_cmd='ping -c5 10.0.0.%s' % i
        print(plc1_cmd)

        # get ten server i 
        strGet='h%s' % i
        print(strGet)
        # get doi tuong server i
        p=net.get(strGet)

        # kich hoat server i, monitor moi 1s
        #plc2_cmd = 'iperf -s -p 1337 -i 1 &'
        plc2_cmd = 'iperf -s -u -p 1337 -i 1 > 10.0.0.%s.txt &' %i
        p.cmd(plc2_cmd)


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
    parser.add_argument('--cip0', dest='controller_ip_0', help="Controller ip in mininet, default value is 10.20.0.248.",required=False,type=str,default="10.20.0.248")
    parser.add_argument('--cip1', dest='controller_ip_1', help="Controller ip in mininet, default value is 10.20.0.250.",required=False,type=str,default="10.20.0.250")

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
        

    tzoo2= TopologyZooXML(os.path.join(tmp_dir,"topologyzoo",args.topo_name+".graphml"))
    m = Mininet(tzoo2.get_topology(),args.controller_ip_0, args.controller_ip_1 ,args.controller_port,args.controller_type)   
    # sudo python3 -E run_mininet.py