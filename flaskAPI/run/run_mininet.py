#!/usr/bin/python3
import requests
import os.path
from topozoo_mininet import TopologyZooXML
from zipfile import ZipFile
import time
import pandas as pd
from requests.auth import HTTPBasicAuth
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
            for (first,second,node_type) in sorted(self.topology_graph):
                if node_type == "h":
                    #hosts.append(net.addHost('h'+str(i), cls=Host, defaultRoute=None))
                    if sys.version_info >= (3, 0):
                        hosts.append(net.addHost('h'+str(first[1]+1), cls=Host, ip=str(ipaddress.IPv4Address(int(ipaddress.IPv4Address(first_ip))+first[1]+1)), defaultRoute=None))
                    else:
                        hosts.append(net.addHost('h'+str(first[1]+1), cls=Host, defaultRoute=None))
                    

            info( '*** Add links\n' )
            for (first,second,node_type) in self.topology_graph:
                try:
                    if node_type=="s":
                        net.addLink(switches[first[1]],switches[second[1]], bw=10, delay='5ms', loss=4, use_htb=True)
                    elif node_type=="h":
                        net.addLink(hosts[first[1]],switches[second[1]], bw=10, delay='5ms', loss=4, use_htb=True)
                except KeyError as e:
                    print("switch or host is unavailable: {}".format(e))


            info( '*** Starting network\n')
            net.build()
            info( '*** Starting controllers\n')
            for controller in net.controllers:
                controller.start()

            info( '*** Starting switches\n')
            len_switches = len(switches)
            index_split = int(len_switches/2)
            i_sw = 0
            for _,sw in switches.items():
                if (i_sw < index_split):
                    sw.start([c0])
                else:
                    sw.start([c1])
                i_sw += 1

            info( '*** Post configure switches and hosts\n')

            CLI(net)
            net.stop()

        setLogLevel( 'info' )
        myNetwork()


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
    