import networkx
import json
import random
from mininet.net import Mininet
from mininet.node import RemoteController, OVSKernelSwitch, Host
from mininet.cli import CLI
from mininet.log import setLogLevel, info
import set_up_mininet, os
import numpy as np
import generate_topo

os.system("sudo mn -c")
set_up_topo = json.load(open('/home/onos/Downloads/A-Server-and-Route-selection-mechanism/flaskAPI/set_up/set_up_topo.json'))
MAX_CAPACITY_BW = set_up_mininet.MAX_CAPACITY_BW
LINK_DELAY = set_up_mininet.LINK_DELAY
ARR_LOSS = set_up_mininet.ARR_LOSS
#Domain Controller
controllers = [ c for c in set_up_topo['controllers'] ]

net = Mininet( topo=None, build=False, ipBase='10.0.0.0/8')
#Cogentco
#Cesnet200706
#VtlWavenet2011
graph = networkx.read_graphml("/home/onos/Downloads/topologyzoo/"+set_up_topo['name_topo']+".graphml")
nodes_graph = graph.nodes()
edges = [[ "s"+str(int(edge[0].replace("n", ""))+1),  "s"+str(int(edge[1].replace("n", ""))+1)] for edge in graph.edges()] 
hosts_graph = ['h'+str(n+1) for n in range(len(nodes_graph))]
switches_graph = ['s'+str(n+1) for n in range(len(nodes_graph))]

# print("hosts ", hosts_graph)
# print("num hosts ", len(hosts_graph))
# print("nodes ", nodes_graph)
# print("edge ", edges)

controllers_save = {}
switches_save = {} #luu theo loai cu the
hosts_save = {}

info( '*** Adding controllers\n' )
for i in range(len(controllers)):
    controller_name = "c" + str(i)
    print(controller_name, " : ", controllers[i])
    controller_net = net.addController(name=controller_name, controller=RemoteController, ip=controllers[i]['ip'], protocol='tcp', port=controllers[i]['controller_port'])
    controllers_save[controller_name] = controller_net

not_host = [ str(host).replace('s', 'h') for host in sum(set_up_topo['bridges'], []) ]

info( '*** Add switches\n')
for switch_name in switches_graph:
    switch_net = net.addSwitch(switch_name, cls=OVSKernelSwitch)
    switches_save[switch_name] = switch_net


info( '*** Adding hosts\n' )
for host_name in hosts_graph:
    if host_name not in not_host:
        ipv4 = "10.0.0." + str(int(host_name.replace("h", "")))
        host_net = net.addHost(host_name,cls=Host, ip=ipv4, defaultRoute=None)
        hosts_save[host_name] = host_net

n = len(switches_graph)
Matrix_graph = [[0 for x in range(n)] for y in range(n)]

info( '*** Add links\n')
#them canh noi switch -> switch
filename = '/home/onos/Downloads/A-Server-and-Route-selection-mechanism/flaskAPI/run/bridge.txt'
open(filename, "w").close()

for edge in edges:
    print("CANH: ", edge)
    LOSS_PER = random.choice(ARR_LOSS)
    if edge in set_up_topo["bridges"]:
        net.addLink(switches_save[edge[0]], switches_save[edge[1]], port1= 10, port2=10, delay=LINK_DELAY, loss=LOSS_PER, bw=MAX_CAPACITY_BW, use_htb=True)
        with open(filename, 'a') as outfile:
            entry = {"src": {
                        "port": 10,
                        "id": "of:" + str(switches_save[edge[0]].dpid)
                    },
                    "dst": {
                        "port": 10,
                        "id": "of:" + str(switches_save[edge[1]].dpid)
                    }}
            outfile.write(json.dumps(entry))
            outfile.write("\n")
            entry = {"src": {
                        "port": 10,
                        "id": "of:" + str(switches_save[edge[1]].dpid)
                    },
                    "dst": {
                        "port": 10,
                        "id": "of:" + str(switches_save[edge[0]].dpid)
                    }}
            outfile.write(json.dumps(entry))
            outfile.write("\n")
            outfile.close()
    else:
        net.addLink(switches_save[edge[0]], switches_save[edge[1]], delay=LINK_DELAY, loss=LOSS_PER, bw=MAX_CAPACITY_BW, use_htb=True)
    # print("CONFIGSWITCH ", switches_save[edge[0]].dpid, " NHE: ", switches_save[edge[0]].config(loss=99, bw=5))
    Matrix_graph[int(edge[0].replace("s", ""))-1][int(edge[1].replace("s", ""))-1] = 1
    Matrix_graph[int(edge[1].replace("s", ""))-1][int(edge[0].replace("s", ""))-1] = 1
    
np.savetxt('graph_matrix.txt',Matrix_graph, fmt='%s')

#them canh noi switch -> host
print("Thong tin switch endPoint")
file_server_info = '/home/onos/Downloads/A-Server-and-Route-selection-mechanism/flaskAPI/run/server_info.txt'
open(file_server_info, "w").close()
for host_name in hosts_save:
    LOSS_PER = random.choice(ARR_LOSS)
    name_switch = host_name.replace("h", "s")
    if host_name in set_up_topo['servers']:
        with open(file_server_info, 'a') as outfile:
            host_ip = '10.0.0.' + host_name.replace("h", "")
            server_data = "of:" + switches_save[name_switch].dpid + ",3" + "," + host_ip
            outfile.write(server_data)
            outfile.write("\n")
            outfile.close()
            print(switches_save[name_switch].dpid, host_ip)
    net.addLink(hosts_save[host_name], switches_save[name_switch], delay=LINK_DELAY, loss=LOSS_PER, bw=MAX_CAPACITY_BW, use_htb=True)
    

# net.build() #sinh ip cho cac host
print("hosts: ", list(hosts_save.keys()))
print("num switch: ", len(switches_save))
print("num host: ", len(hosts_save))

info( '*** Starting network\n' )
net.build()
#====================map switch voi controller=========================
# info( '*** Starting switches\n')
# for key in switches_save.keys():
#     switches_save[key].start([])

info( '*** Starting controllers\n')
for key in controllers_save.keys():
    controllers_save[key].start()


map_switch_controller = {"c"+str(i): controllers[i]['switches'] for i in range(len(controllers))}

for c in controllers_save:
    for switch in map_switch_controller[c]:
        net.get(switch).start([controllers_save[c]])

def ping_host_in_sdn(net, controllers, not_host):
    for c in controllers:
        hst = [ "h" + str(int(switch.replace("s", ""))) for switch in c['switches'] if "h"+str(int(switch.replace("s", ""))) not in not_host]
        for h_i in range(len(hst)):
            net.ping([ hosts_save[hst[0]], hosts_save[hst[h_i]] ])


ping_host_in_sdn(net, controllers, not_host)
# change_network_condition_loss.main_change(net)
CLI(net)
kq = input("Chay luon nhe:")
if kq == 'ok':
    generate_topo.generate_topo(net, hosts_save)
    CLI(net)

net.stop()

