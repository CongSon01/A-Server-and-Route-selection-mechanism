import os
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from mininet.link import Intf
from mininet.node import Controller

import subprocess

virtualenv = '../../venv11/bin/python3'


class NetworkTopo( Topo ):
    # Builds network topology
    def build( self, **_opts ):

        s1 = self.addSwitch ( 's1', failMode='standalone' )
        # host_len = 3
        h1 = self.addHost('h1')        
        # Adding hosts
        
        # for host_no in host_len:
        #     hosts.append(self.addHost(f'h{}', ip='192.168.0.{number}/24' ))
        
        # Adding device



if __name__ == '__main__':

    topo = NetworkTopo()
    
    net = Mininet( topo=topo, controller=None )
    net.start()
    # Make Switch act like a normal switch
    #net['s1'].cmd('ovs-ofctl add-flow s1 action=normal')
    # Make Switch act like a hub
    #net['s1'].cmd('ovs-ofctl add-flow s1 action=flood')
    # CLI( net )
    # d1 = net.getNodeByName('d1')
    for host in net.hosts:
        print(host.popen('../../venv11/bin/python3 -V').communicate())

    net.stop()