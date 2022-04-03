from os import link
from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from subprocess import call
import numpy as np
from numpy import random, rate
import json
import time
import pandas as pd
import sys
sys.path.append('/home/onos/Downloads/flask_SDN/Flask-SDN/flaskAPI/model')
import BW_server
import time
import os
import requests
from requests.auth import HTTPBasicAuth
import random

def myNetwork():
    net = Mininet( topo=None,
                   build=False,
                   ipBase='10.0.0.0/8', link=TCLink)

    info( '*** Adding controller\n' )
    c0=net.addController(name='c0',
                      controller=RemoteController,
                      ip='10.20.0.248',
                      protocol='tcp',
                      port=6653)
    c1=net.addController(name='c1',
                      controller=RemoteController,
                      ip='10.20.0.250',
                      protocol='tcp',
                      port=6653)

    info( '*** Add switches\n')
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch)
    s2 = net.addSwitch('s2', cls=OVSKernelSwitch)
    s3 = net.addSwitch('s3', cls=OVSKernelSwitch)
    s4 = net.addSwitch('s4', cls=OVSKernelSwitch)
    s5 = net.addSwitch('s5', cls=OVSKernelSwitch)
    s6 = net.addSwitch('s6', cls=OVSKernelSwitch)
    s7 = net.addSwitch('s7', cls=OVSKernelSwitch)
    s8 = net.addSwitch('s8', cls=OVSKernelSwitch)

    info( '*** Add hosts\n')
    h1 = net.addHost('h1', cls=Host, ip='10.0.0.1', defaultRoute=None)
    h2 = net.addHost('h2', cls=Host, ip='10.0.0.2', defaultRoute=None)  
    # h3 = net.addHost('h3', cls=Host, ip='10.0.0.3', defaultRoute=None)
    # h4 = net.addHost('h4', cls=Host, ip='10.0.0.4', defaultRoute=None)
    # h5 = net.addHost('h5', cls=Host, ip='10.0.0.5', defaultRoute=None)
    h3 = net.addHost('h3', cls=Host, ip='10.0.0.3', defaultRoute=None)
    h4 = net.addHost('h4', cls=Host, ip='10.0.0.4', defaultRoute=None)
    #h8 = net.addHost('h8', cls=Host, ip='10.0.0.8', defaultRoute=None)

    info( '*** Add links\n')
    # bw-10Gb/s
    # add links vs hosts
    net.addLink(h1, s1, bw=10, delay='1ms', loss=1, use_htb=True, cls= TCLink)
    net.addLink(h2, s2, bw=10, delay='1ms', loss=1, use_htb=True, cls= TCLink )

    # add links vs servers
    net.addLink(h3, s6, bw=10, delay='1ms', loss=1, use_htb=True, cls= TCLink )
    net.addLink(h4, s8, bw=10, delay='1ms', loss=1, use_htb=True, cls= TCLink )

    # add link between si and si+1
    net.addLink(s1, s2, bw=10, delay='1ms', loss=1, use_htb=True, cls= TCLink  )
    net.addLink(s2, s3, bw=10, delay='1ms', loss=1, use_htb=True, cls= TCLink  )
    net.addLink(s3, s4, bw=10, delay='1ms', loss=1, use_htb=True, cls= TCLink )
    net.addLink(s4, s1, bw=10, delay='1ms', loss=1, use_htb=True, cls= TCLink  )
    
    net.addLink(s5, s6, bw=10, delay='1ms', loss=1, use_htb=True, cls= TCLink  )
    net.addLink(s6, s7, bw=10, delay='1ms', loss=1, use_htb=True, cls= TCLink )
    net.addLink(s7, s8, bw=10, delay='1ms', loss=1, use_htb=True, cls= TCLink  )
    net.addLink(s8, s5, bw=10, delay='1ms', loss=1, use_htb=True, cls= TCLink )
    
    # noi giua 2 SDN
    net.addLink(s4, s5, port1= 10, port2=10, bw=10, delay='1ms', loss=1, use_htb=True, cls= TCLink)
    #net.addLink(s3, s6, port1= 11, port2=11, bw=10, delay='1ms', loss=1, use_htb=True)

    info( '*** Starting network\n')
    net.build()
    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info( '*** Starting switches\n')
    net.get('s1').start([c0])
    net.get('s2').start([c0])
    net.get('s3').start([c0]) 
    net.get('s4').start([c0])

    net.get('s5').start([c1])
    net.get('s6').start([c1])
    net.get('s7').start([c1])
    net.get('s8').start([c1])

    info( '*** Post configure switches and hosts\n')
    net.pingAll()
    time.sleep(15)
    # lap lich sinh mang
    generate_topo(net)
    CLI(net)

def generate_topo(net):
    host_list, server_list = create_host_server(net)

    print("------------------   server  -----------------------")
    print(server_list)
    num_host = len(host_list) 
    num_server = len(server_list) 
    print("So host =", num_host, " So server=", num_server) 

    period = 100 # random data from 0 to period 
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
        
    print(list_ip_server)
    
    # read file server and write to mongo
    for ip_server in list_ip_server:
        os.system('python readlog.py'+' '+ip_server+' &')
        time.sleep(1)
    time.sleep(60)

    # lap lich cho host
    #run_shedule(starting_table, period, interval,net)

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

def run_shedule(starting_table, period, interval, net):
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
    # ban dau tap net.hosts co 1,2 ... 8 con
    host_list = list()
    server_list = list()

    for h in range( len(net.hosts) ):
        if h <=1:   # host 1 2 
            host_list.append( net.hosts[h])
        else: # server 3 4
            server_list.append( net.hosts[h])

    return (host_list, server_list)

def call_routing_api_flask(host):
    print("call flask")
    response = requests.post("http://10.20.0.250:5000/getIpServer", data= host)  
    dest_ip = response.text
    return str(dest_ip)

                
def start_server(num_server, net):
    """
    Kjch hoat server de truyen iperd
    """
    #p1, p2, p3,p4,p5,p6,p7,p8 = net.get('h1', 'h2', 'h3','h4', 'h5', 'h6','h7', 'h8')
    p1, p2, p3, p4 = net.get('h1', 'h2', 'h3', 'h4')

    plc1_cmd=''
    strGet=''
    plc2_cmd=''
    i=3

    # duyet qua kich hoat cac server 3 4
    while i <= 4:    
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
        # path = '/home/onos/Downloads/flask_SDN/Flask-SDN/flaskAPI/run/'
        # name_server = path + 'server' + strGet + ".txt"
        # old_list_BW = get_BW_from_server(name_server, strGet)
        plc2_cmd = 'iperf -s -u -p 1337 -i 1 > 10.0.0.%s.txt &' %i
        # get BW from file server
        
        # if len(list_BW) != len(old_list_BW):
            # BW_server.insert_data(list_BW[len(old_list_BW):])
        p.cmd(plc2_cmd)
        # time.sleep(10)
        # list_BW = get_BW_from_server(name_server, strGet)
        # BW_server.insert_data(list_BW)

        i=i+1 

def write_table_to_file(table, name_file):
    df = pd.DataFrame(table)
    df.to_csv(name_file)
    
if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()
    # sudo mn -c
    # sudo python3 -E example2.py

   