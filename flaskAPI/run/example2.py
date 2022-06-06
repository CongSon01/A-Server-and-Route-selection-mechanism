#!/usr/bin/env python

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
from numpy import random
import json
import time
import pandas as pd

import requests
from requests.auth import HTTPBasicAuth
import random

def myNetwork():

    net = Mininet( topo=None,
                   build=False,
                   ipBase='10.0.0.0/8')

    info( '*** Adding controller\n' )
    # c0=net.addController(name='c0',
    #                   controller=RemoteController,
    #                   ip='10.20.0.209',
    #                   protocol='tcp',
    #                   port=6633)

    c0=net.addController(name='c0',
                      controller=RemoteController,
                      ip='10.20.0.209',
                      protocol='tcp',
                      port=6633)
    # c1=net.addController(name='c1',
    #                   controller=RemoteController,
    #                   ip='10.20.0.210',
    #                   protocol='tcp',
    #                   port=6653)


    info( '*** Add switches\n')

    s1 = net.addSwitch('s1', cls=OVSKernelSwitch)
    s2 = net.addSwitch('s2', cls=OVSKernelSwitch)
    s3 = net.addSwitch('s3', cls=OVSKernelSwitch)
    s4 = net.addSwitch('s4', cls=OVSKernelSwitch)
    # s5 = net.addSwitch('s5', cls=OVSKernelSwitch)
    # s6 = net.addSwitch('s6', cls=OVSKernelSwitch)
    # s7 = net.addSwitch('s7', cls=OVSKernelSwitch)
    # s8 = net.addSwitch('s8', cls=OVSKernelSwitch)



    info( '*** Add hosts\n')
    h1 = net.addHost('h1', cls=Host, ip='10.0.0.1', defaultRoute=None)
    h2 = net.addHost('h2', cls=Host, ip='10.0.0.2', defaultRoute=None)
    # h4 = net.addHost('h4', cls=Host, ip='10.0.0.4', defaultRoute=None)
    # h6 = net.addHost('h6', cls=Host, ip='10.0.0.6', defaultRoute=None)  
    # h7 = net.addHost('h7', cls=Host, ip='10.0.0.7', defaultRoute=None)

    info( '*** Add links\n')
    # add link between si vs hi

    # # bw-10Gb/s
    net.addLink(s1, h1, bw=10, delay='5ms', loss=4, use_htb=True)
    net.addLink(s2, h2, bw=10, delay='5ms', loss=4, use_htb=True)
    # net.addLink(s4, h4, bw=10, delay='5ms', loss=4, use_htb=True)
    # net.addLink(s6, h6, bw=10, delay='5ms', loss=4, use_htb=True)
    # net.addLink(s7, h7, bw=10, delay='5ms', loss=4, use_htb=True)

    # # add links
    net.addLink(s1, s2, bw=10, delay='5ms', loss=4, use_htb=True)
    net.addLink(s2, s3, bw=10, delay='5ms', loss=4, use_htb=True)
    net.addLink(s3, s4, bw=10, delay='5ms', loss=4, use_htb=True)
    net.addLink(s4, s1, bw=10, delay='5ms', loss=4, use_htb=True)

    # net.addLink(s5, s6, bw=10, delay='5ms', loss=4, use_htb=True)
    # net.addLink(s6, s7, bw=10, delay='5ms', loss=4, use_htb=True)
    # net.addLink(s7, s8, bw=10, delay='5ms', loss=4, use_htb=True)
    # net.addLink(s8, s5, bw=10, delay='5ms', loss=4, use_htb=True)

    # add link between si and si+1
    # net.addLink(s2, s5 , port1= 10, port2=10, bw=10, delay='5ms', loss=4, use_htb=True)
    # filename = '/home/onos/Downloads/flaskSDN/flaskAPI/run/bridge.txt'
    # with open(filename, 'a') as outfile:
    #                             entry = {"src": {
    #                                         "port": 10,
    #                                         "id": "of:" + str(s2.dpid)
    #                                     },
    #                                     "dst": {
    #                                         "port": 10,
    #                                         "id": "of:" + str(s5.dpid)
    #                                     }}
    #                             outfile.write(json.dumps(entry))
    #                             outfile.write("\n")
    #                             entry = {"src": {
    #                                         "port": 10,
    #                                         "id": "of:" + str(s5.dpid)
    #                                     },
    #                                     "dst": {
    #                                         "port": 10,
    #                                         "id": "of:" + str(s2.dpid)
    #                                     }}
    #                             outfile.write(json.dumps(entry))
    #                             outfile.write("\n")
    #                             outfile.close()
    # net.addLink(s3, s8, port1= 10, port2=10, bw=10, delay='5ms', loss=4, use_htb=True)
    # with open(filename, 'a') as outfile:
    #                             entry = {"src": {
    #                                         "port": 10,
    #                                         "id": "of:" + str(s3.dpid)
    #                                     },
    #                                     "dst": {
    #                                         "port": 10,
    #                                         "id": "of:" + str(s8.dpid)
    #                                     }}
    #                             outfile.write(json.dumps(entry))
    #                             outfile.write("\n")
    #                             entry = {"src": {
    #                                         "port": 10,
    #                                         "id": "of:" + str(s8.dpid)
    #                                     },
    #                                     "dst": {
    #                                         "port": 10,
    #                                         "id": "of:" + str(s3.dpid)
    #                                     }}
    #                             outfile.write(json.dumps(entry))
    #                             outfile.write("\n")
    #                             outfile.close()

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

    # net.get('s5').start([c1])
    # net.get('s6').start([c1])
    # net.get('s7').start([c1])
    # net.get('s8').start([c1])
    # net.get('s4').start([c1])
    # print(h1.MAC())
    # print(h2.MAC())
    # print(h4.MAC())


    info( '*** Post configure switches and hosts\n')

    net.pingAll()

    #time.sleep(15)
    # ham chinh de sinh thoi gian cho cac switch
    # generate_topo(net)

    CLI(net)
    # net.stop()

def generate_topo(net):

    host_list, server_list = create_host_server(net)
    num_host = len(host_list)   

    period = 20 # random data from 0 to period 
    interval = 5 # each host generates data 5 times randomly
    life_time = 20

    name_host = list()
    for ip_host in host_list:
        name_host.append(str(ip_host))
    
    print("HOST: ", name_host)

    # khoi tao bang thoi gian cho tung host
    starting_table = create_starting_table( name_host, period, interval, life_time )

    print(starting_table)

    write_table_to_file(starting_table, 'starting_table.json')

    # kich hoat server chuan bi lang nghe su dung iperf

    # chay topo mininet
    # bat reactive
    # khi nao print bat flask thi bat
    # sau do doi tin hieu reponse
    # start_server(host_list, server_list, net)


    # lap lich cho host
    next = input("Enter continues: ")
    if next == 'ok':
        run_shedule(starting_table,net)

    #call_routing_api(host_list, server_list)

    
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

# def create_processing_table(num_host, period, starting_table, interval):

#    processing_table = np.zeros( (num_host, interval) )
#    s = 0 # processing time
     
#    for h in range( len(processing_table) ):
#         for t in range( len(processing_table[h]) ):
#           if t == len(processing_table[h]) - 1:
#                       upper_bound = period   
#           else:
#                       upper_bound = starting_table[h][t+1]

#           # thoi gian chay moi host thuoc khoang denta thoi gian 
#           # bat dau t va t+1 cua host do  
#           low_bound   = starting_table[h][t]
#           s = random.uniform(low_bound, upper_bound)  
#           #print("L = ", low_bound, "Upper = ", upper_bound, "value = ", s)  
#           processing_table[h][t] = s

#    print(processing_table)
#    return processing_table   
def get_host_affter_time(full_values, run_time):
    for cluster_host in full_values:
        for host in cluster_host:
            if cluster_host[host] == run_time:
                return str(host)

def run_shedule(generate_flow, net):
    print("generate_flow--------")
    print(list(generate_flow.values()))
    
    full_times = sum([ list(start_host.values()) for start_host in list(generate_flow.values()) ], [])
    full_values = [ start_host for start_host in generate_flow.values() ]

    start_time = time.time()
    stop_time = max(full_times)
    while True:
        current_time = time.time() - start_time
        if ( current_time in  full_times):
            p = net.get(get_host_affter_time(full_values, current_time))
            print("HOST: ", p, " Chay luc ", current_time)
            # des = call_routing_api_flask( p.IP() )
            des = "10.0.0.4"
            print("TRUYEN DU LIEU ", p.IP(), "--->", des)
            

                      
            # rate = random.randint(20000000, 60000000) #20^6 - 60*10^6 = 20Mb -> 60Mb
            # phan tram chiem dung bang thong
            rate = np.random.uniform(20000000, 60000000) #20^6 - 60*10^6 = 20Mb -> 60Mb
            print("------------- gui du lieu-----------", rate)
            plc_cmd =  'iperf -c %s -b %d -u -p 1337 -t 600 &' %(des, rate)
            p.cmd(plc_cmd)   

        if ( current_time == stop_time ):
            print("DONE")
            break
    print("OK")
      
def write_table_to_file(table, name_file):
    with open(name_file, "w") as outfile:
        json.dump(table, outfile)
    
def create_host_server(net):

    # ban dau tap net.hosts co 1,2 ... 8 con
    host_list = []
    server_list = []

    for h in range( len(net.hosts) ):
        if h <=2:   # host 1 2 
            host_list.append( net.hosts[h])
        else: # server  5 6 7 8
            server_list.append( net.hosts[h])

    return (host_list, server_list)

def call_routing_api_flask(host):
    print("call flask")
    # des=8
    # url = 'http://127.0.0.1:5000/getIpServer/'
    # response = requests.post(url)

    response = requests.post("http://127.0.0.1:5000/getIpServer", data= host)

    
    dest_ip = response.text
    #print(dest_ip)
    return str(dest_ip)

    # minh phai doc duoc topo mininet
    # sau do moi bat flask
    # sau do file mininet moi chay iperf lap lich


 
    # response = requests.post('http://localhost:8181/onos/v1/flows?appId=onos.onosproject.routing', data = host)
    # print(response)

    # goi url flask
    #return des

def call_routing_api(host_list, server_list):
    
    query = {'src':'10.0.0.1', 'dst':'10.0.0.8'}
    response = requests.get('http://localhost:8181/onos/test/localTopology/set-Routing-byIp', 
    params=query,auth=HTTPBasicAuth('onos', 'rocks'))
    print(response)

def start_server(host_list, server_list, net):

    p1, p2, p3,p4 = net.get('h1', 'h2', 'h3','h4')

    plc1_cmd=''
    strGet=''
    plc2_cmd=''
    i=4
    # duyet qua 8 host
    while i < 8:
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
        plc2_cmd = 'iperf -s -p 1337 -i 1 &'
        p.cmd(plc2_cmd)

    # transfer_data(net)

def transfer_data(net):
    print("tam dung 5s")
    time.sleep(5)
    i=0
    j = 0
  
    while j < 3:
            # h1,.. h4 la client, h5 -> h8 la server
            while i < 4:
                    # moi lan rou tu src -> dst se co 1 khoang nghi
                    i=i+1
                    interval = random.uniform(0.01, 0.1)
                    print("prepare for Routing about", interval, "seconds")
                    # time.sleep(interval)
                    time.sleep(5)

                    # random server 5 -> 8
                    ip_dest = random.randint(5, 8)
                    # call api routing
                    query = {'src':'10.0.0.%s' %i, 'dst':'10.0.0.%s' %ip_dest}
                    response = requests.get('http://localhost:8181/onos/test/localTopology/set-Routing-byIp', params=query,auth=HTTPBasicAuth('onos', 'rocks'))
                    print("Routing from host", i, " to server ", ip_dest)
                    print(response)

                    # sau khi co duong di thi ta goi iperf de truyen data from source -> dest
                    p=net.get('h%s' %i)
                    ip_dest = '10.0.0.%s' %ip_dest
                    # truyen data den ip cua dest voi duration = 60s
                    plc_cmd = 'iperf -c %s -p 1337 -t 60 &' %ip_dest
                    p.cmd(plc_cmd)   
                    print(plc_cmd)
                    print("Tranfering from host thu", i, "to", ip_dest)
                    print("\n")
            j = j+1
       
    print('Kiem tra')
if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()
    # sudo mn -c
    # sudo python3 -E example2.py


 








    
  
