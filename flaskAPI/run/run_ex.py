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
    #                   ip='10.20.0.200',
    #                   protocol='tcp',
    #                   port=6653)
    c0=net.addController(name='c0',
                      controller=RemoteController,
                      ip='10.20.0.211',
                      protocol='tcp',
                      port=6633)
    # c2=net.addController(name='c2',
    #                   controller=RemoteController,
    #                   ip='10.20.0.211',
    #                   protocol='tcp',
    #                   port=6633)


    info( '*** Add switches\n') 
    h1 = net.addHost('h1', cls=Host, ip='10.0.0.1', mac='00:00:00:00:00:01', defaultRoute=None)
    # h2 = net.addHost('h2', cls=Host, ip='10.0.0.2', defaultRoute=None)
    # h3 = net.addHost('h3', cls=Host, ip='10.0.0.3', defaultRoute=None)
    h5 = net.addHost('h5', cls=Host, ip='10.0.0.5', mac='00:00:00:00:00:05', defaultRoute=None)
    h8 = net.addHost('h8', cls=Host, ip='10.0.0.8', mac='00:00:00:00:00:08', defaultRoute=None)

    s1 = net.addSwitch('s1', cls=OVSKernelSwitch)
    s2 = net.addSwitch('s2', cls=OVSKernelSwitch)
    s3 = net.addSwitch('s3', cls=OVSKernelSwitch)
    s4 = net.addSwitch('s4', cls=OVSKernelSwitch)
    s5 = net.addSwitch('s5', cls=OVSKernelSwitch)
    s6 = net.addSwitch('s6', cls=OVSKernelSwitch)
    s7 = net.addSwitch('s7', cls=OVSKernelSwitch)
    s8 = net.addSwitch('s8', cls=OVSKernelSwitch)


    info( '*** Add hosts\n')
    h1 = net.addHost('h1', cls=Host, ip='10.0.0.1', mac='00:00:00:00:00:01', defaultRoute=None)
    # h2 = net.addHost('h2', cls=Host, ip='10.0.0.2', defaultRoute=None)
    # h3 = net.addHost('h3', cls=Host, ip='10.0.0.3', defaultRoute=None)
    h5 = net.addHost('h5', cls=Host, ip='10.0.0.5', mac='00:00:00:00:00:05', defaultRoute=None)
    h8 = net.addHost('h8', cls=Host, ip='10.0.0.8', mac='00:00:00:00:00:08', defaultRoute=None)
    # h6 = net.addHost('h6', cls=Host, ip='10.0.0.6', defaultRoute=None) 

    info( '*** Add links\n')
    # add link between si vs hi

    # bw-10Gb/s
    net.addLink(s1, h1,port1= 1, port2=1, bw=10, delay='5ms', loss=4, use_htb=True)
    # net.addLink(s2, h2, bw=10, delay='5ms', loss=4, use_htb=True)
    # net.addLink(s3, h3, bw=10, delay='5ms', loss=4, use_htb=True)
    net.addLink(s5, h5,port1= 1, port2=1, bw=10, delay='5ms', loss=4, use_htb=True)
    net.addLink(s8, h8,port1= 1, port2=1, bw=10, delay='5ms', loss=4, use_htb=True)

    # add links
    net.addLink(s1, s2, port1= 2, port2=2, bw=10, delay='5ms', loss=4, use_htb=True)
    net.addLink(s2, s3, port1= 3, port2=3, bw=10, delay='5ms', loss=4, use_htb=True)
    net.addLink(s3, s4, port1= 2, port2=2, bw=10, delay='5ms', loss=4, use_htb=True)
    net.addLink(s4, s5, port1= 3, port2=3, bw=10, delay='5ms', loss=4, use_htb=True)
    net.addLink(s5, s6, port1= 2, port2=2, bw=10, delay='5ms', loss=4, use_htb=True)
    net.addLink(s6, s3, port1= 4, port2=4, bw=10, delay='5ms', loss=4, use_htb=True)
    net.addLink(s4, s7, port1= 4, port2=4, bw=10, delay='5ms', loss=4, use_htb=True)
    net.addLink(s7, s8, port1= 3, port2=3, bw=10, delay='5ms', loss=4, use_htb=True)
    
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
    net.get('s5').start([c0])
    net.get('s6').start([c0])
    net.get('s7').start([c0])
    net.get('s8').start([c0])
    # net.get('s4').start([c1])
    print(h1.MAC())
    print(h5.MAC())
    print(h8.MAC())
    # print(h3.MAC())


    info( '*** Post configure switches and hosts\n')

    # net.pingAll()

    #time.sleep(15)
    # ham chinh de sinh thoi gian cho cac switch
    # generate_topo(net)

    CLI(net)
    # net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()
    # sudo mn -c
    # sudo python3 -E example2.py
