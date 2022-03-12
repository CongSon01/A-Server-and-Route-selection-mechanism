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
                        switches[second[1]] = net.addSwitch('s'+str(second[1]+1), cls=OVSKernelSwitch)
                        added_switches[second[1]] = True
                    

            info( '*** Add hosts\n')
            hosts= []
            
            first_ip = '10.0.0.0'
            not_host = ['h8', 'h9', 'h10', 'h11']
            for (first,second,node_type) in sorted(self.topology_graph):
                if node_type == "h":
                    #hosts.append(net.addHost('h'+str(i), cls=Host, defaultRoute=None))
                    name_host = 'h'+str(first[1]+1)
                    if name_host not in not_host:
                        hosts.append(net.addHost(name_host, cls=Host, ip=str(ipaddress.IPv4Address(int(ipaddress.IPv4Address(first_ip))+first[1]+1)), defaultRoute=None))
                    # else:
                        # hosts.append(net.addHost('h'+str(first[1]+1), cls=Host, defaultRoute=None))
                    

            info( '*** Add links\n' )
            switch_not_host = ['s10','s11', 's9', 's8']
            two_switch_connect = ['s9_s10','s8_s11']
            for (first,second,node_type) in self.topology_graph:
                try:
                    if node_type=="s":
                        name_connect = str(str(switches[first[1]]) +'_'+str(switches[second[1]]))
                        if  name_connect in two_switch_connect :
                            print(name_connect)
                            net.addLink(switches[first[1]],switches[second[1]], port1= 10, port2=10, bw=10, delay='5ms', loss=2, use_htb=True)
                        else:
                            net.addLink(switches[first[1]],switches[second[1]], bw=10, delay='5ms', loss=0, use_htb=True)
                    elif node_type=="h":
                        if ( str(switches[second[1]]) not in switch_not_host):
                            net.addLink(hosts[first[1]],switches[second[1]], bw=10, delay='5ms', loss=0, use_htb=True)
                except KeyError as e:
                    print("switch or host is unavailable: {}".format(e))


            info( '*** Starting network\n')
            net.build()
            info( '*** Starting controllers\n')
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
            #         sw.start([c0])
            #     else:
            #         print('add controller 2', sw)
            #         sw.start([c1])
            #     i_sw += 1

            sw_0 = [0, 1, 2, 9, 10] # 's1', 's2', 's3', 's10', 's11'
            sw_1 = [3 ,4, 5, 6, 7, 8] # 's4', 's5', 's6', 's7', 's8', 's9'
            for i_sw in sw_0:
                switches.get(i_sw).start([c0])
            for i_sw in sw_1:
                switches.get(i_sw).start([c1])

            info( '*** Post configure switches and hosts\n')
            net.pingAll()

            generate_topo(net)
            CLI(net)
            net.stop()

        setLogLevel( 'info' )
        myNetwork()

def generate_topo(net):
    
    host_list, server_list = create_host_server(net)
    num_host = len(host_list)   

    period   =  30 # random data from 0 to period 
    interval = 5 # each host generates data 5 times randomly

    # khoi tao bang thoi gian cho tung host
    print("bang khoi tao")
    starting_table = create_starting_table(num_host, period, interval)
    print("\n")
    print("Bang ket thuc")
    processing_table = create_processing_table(num_host, period, starting_table, interval)

    write_table_to_file(starting_table, 'starting_table.csv')
    write_table_to_file(processing_table, 'processing_table.csv')

    # kich hoat server chuan bi lang nghe su dung iperf

    # chay topo mininet
    # bat reactive
    # khi nao print bat flask thi bat
    # sau do doi tin hieu reponse
    start_server(host_list, server_list, net)
    print("Sleep 2phut after start flask")
    # delay de chay flask da roi lap lich goi flask api
    time.sleep(120)


    # lap lich cho host
    run_shedule(starting_table, processing_table, period, interval,net)

    #call_routing_api(host_list, server_list)

    
def create_starting_table(num_host, period, interval):

    starting_table =  np.zeros( (num_host, interval) )
    s = 0 # random starting time

    for h in range( len(starting_table) ):
        for t in range( len(starting_table[h]) ):
            s = random.uniform(0, period) # do t = 0 to 100

            starting_table[h][t] = s
        starting_table[h].sort()

    print(starting_table)
    return starting_table

def create_processing_table(num_host, period, starting_table, interval):

   processing_table = np.zeros( (num_host, interval) )
   s = 0 # processing time
     
   for h in range( len(processing_table) ):
        for t in range( len(processing_table[h]) ):
          if t == len(processing_table[h]) - 1:
                      upper_bound = period   
          else:
                      upper_bound = starting_table[h][t+1]

          # thoi gian chay moi host thuoc khoang denta thoi gian 
          # bat dau t va t+1 cua host do  
          low_bound   = starting_table[h][t]
          s = random.uniform(low_bound, upper_bound)  
          #print("L = ", low_bound, "Upper = ", upper_bound, "value = ", s)  
          processing_table[h][t] = s

   print(processing_table)
   return processing_table   

def run_shedule(starting_table, processing_table, period, interval, net):

    visited = np.full( ( len(starting_table), interval), False, dtype=bool )
    visited_stop = np.full( ( len(processing_table), interval), False, dtype=bool )
    dem = 0
    dem_stop = 0
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
                    #print("host = ", host, "time = ", t)
                    #des=call_routing_api_flask(host+1)
                    p=net.get('h%s' %(host+1))
                    #print( p.IP() )
                    des=call_routing_api_flask( p.IP() )
                    #des = '10.0.0.%s' %des
                    # truyen data den ip cua dest voi duration = 60s
                    #print("TRUYEN DU LIEU ", p.IP(), "--->", des)

                    # random phan tram bang thong  
                    utilize = random.randint(0, 10)
                    plc_cmd =  'iperf -c %s -b %d -p 1337 -t 1000 &' %(des, utilize)
                    #plc_cmd = 'iperf -c %s -b %d -p 1337 -t 1000 &' %des, %utilize

                    p.cmd(plc_cmd)   
                    print(plc_cmd)
                    print("host", host, " --> ", des, "tai giay thu", starting_table[host][t])
                    dem += 1
                    visited[host][t] = True
        
        # for host in range( len(processing_table)):
        #     for stop in range (len(processing_table[host])):
        #         if  abs (processing_table[host][stop] - current ) < 0.001 and visited_stop[host][stop] == False:
        #             #print("host = ", host, "stop= ", stop)
        #             print("host", host, " stop", "tai giay thu", processing_table[host][stop])
        #             visited_stop[host][stop] = True
        #             dem_stop += 1

        # if abs (period - current) < 0.01:
        #     print("host", host, "stop tai giay thu", period )

            
    print("ok")
    print("Dem = " , dem)
    # print("dem stop", dem_stop)
      
def write_table_to_file(table, name_file):

    # convert table into dataframe
    df = pd.DataFrame(table)
    
    # save the dataframe as a csv file
    df.to_csv(name_file)
    
def create_host_server(net):

    # ban dau tap net.hosts co 1,2 ... 8 con
    host_list = []
    server_list = []

    for h in range( len(net.hosts) ):
        if h <= 3:   # host 1,2,3
            host_list.append( net.hosts[h])
        else: # server  4, 5, 6 ,7
            server_list.append( net.hosts[h])

    return (host_list, server_list)

def call_routing_api_flask(host):
    print("call flask")
    response = requests.post("http://10.20.0.250:5000/getIpServer", data= host)
    
    dest_ip = response.text
    #print(dest_ip)
    return str(dest_ip)

def call_routing_api(host_list, server_list):
    
    query = {'src':'10.0.0.1', 'dst':'10.0.0.11'}
    response = requests.get('http://localhost:8181/onos/test/localTopology/set-Routing-byIp', 
    params=query,auth=HTTPBasicAuth('onos', 'rocks'))
    print(response)

def start_server(host_list, server_list, net):

    #p1, p2, p3,p4,p5,p6,p7,p8 = net.get('h1', 'h2', 'h3','h4', 'h5', 'h6','h7', 'h8')
    #p1, p2, p3, p6, p7, p8 = net.get('h1', 'h2', 'h3', 'h4', 'h5', 'h6','h7')
    p1, p2, p3, p6, p7, p8 = net.get('h1', 'h2', 'h3', 'h6','h7', 'h8')
    plc1_cmd=''
    strGet=''
    plc2_cmd=''
    i=5
    # duyet qua 8 host
    while i < len(net.hosts):
        # moi lan khoi tao 1 server co khoang nghi giua chung
        #interval = random.uniform(0.01, 0.1)
        #print ("Initialized transfer; waiting %f seconds..." % interval)
        #time.sleep(interval)

        # do host chay tu 1 nen tang bien i len 1 
        #p5.cmd(plc1_cmd)
        i=i+1

        # ping host i
        plc1_cmd='ping -c5 10.0.0.%s' % i
        print(plc1_cmd)

        # get ten host i 
        strGet='h%s' % i
        print(strGet)
        p=net.get(strGet)

        # kich hoat host i la server, monitor moi 1s
        plc2_cmd = 'iperf -s -u -p 1337 -i 1 &'
        p.cmd(plc2_cmd)

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

    parser.add_argument('--toponame', dest='topo_name', help="Topology name e.g. Abilene",required=False,type=str, default='Abilene')
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
    