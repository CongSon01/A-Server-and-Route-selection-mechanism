import networkx
import json
from mininet.net import Mininet
from mininet.node import RemoteController, OVSKernelSwitch, Host
from mininet.cli import CLI
from mininet.log import setLogLevel, info
import set_up_mininet
import numpy as np
import generate_topo


# os.system("sudo mn -c")
set_up_topo = json.load(open('/home/onos/Downloads/flaskSDN/flaskAPI/set_up/set_up_topo.json'))
MAX_CAPACITY_BW = set_up_mininet.MAX_CAPACITY_BW
LOSS_PER = set_up_mininet.LOSS_PER
LINK_DELAY = set_up_mininet.LINK_DELAY
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
filename = '/home/onos/Downloads/flaskSDN/flaskAPI/run/bridge.txt'
open(filename, "w").close()

for edge in edges:
    print("CANH: ", edge)
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
    Matrix_graph[int(edge[0].replace("s", ""))-1][int(edge[1].replace("s", ""))-1] = 1
    Matrix_graph[int(edge[1].replace("s", ""))-1][int(edge[0].replace("s", ""))-1] = 1
    
np.savetxt('graph_matrix.txt',Matrix_graph, fmt='%s')

#them canh noi switch -> host
for host_name in hosts_save:
    name_switch = host_name.replace("h", "s")
    net.addLink(hosts_save[host_name], switches_save[name_switch], delay=LINK_DELAY, loss=LOSS_PER, bw=MAX_CAPACITY_BW, use_htb=True)
    

# net.build() #sinh ip cho cac host

print("hosts: ", list(hosts_save.keys()))
print("num switch: ", len(switches_save))
print("num host: ", len(hosts_save))

info( '*** Starting network\n')
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

def ping_host_to_server(net, hosts, servers):
    for name_server in servers:
        net.ping([ hosts_save['h3'], hosts_save[name_server] ])
        net.ping([ hosts_save['h5'], hosts_save[name_server] ])


# ping_host_in_sdn(net, controllers, not_host)
# ping_host_to_server(net, set_up_topo['hosts'], set_up_topo['servers'])
# net.pingAll
CLI(net)
kq = input("Chay luon nhe:")
if kq == 'ok':
    generate_topo.generate_topo(net, hosts_save)
    CLI(net)

net.stop()

