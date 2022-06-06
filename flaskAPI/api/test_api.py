
import sys, json
PATH_ABSOLUTE = "/home/onos/Downloads/flaskSDN/flaskAPI/"
IS_RUN_RRBIN = False
IS_RUN_QLEARNING = True

sys.path.append(PATH_ABSOLUTE+'model')
sys.path.append(PATH_ABSOLUTE+'handledata/models')
sys.path.append(PATH_ABSOLUTE+'core')
sys.path.append(PATH_ABSOLUTE+'routingAlgorithm')
sys.path.append(PATH_ABSOLUTE+'q_learning')

import CusTopo

# import from core
import connectGraph, Graph

import apiSDN

# get full ip of SDN
list_ip = json.load(open('/home/onos/Downloads/flaskSDN/flaskAPI/set_up/set_up_topo.json'))["controllers"]
# list_ip = [ controller['ip'] for controller in controllers]


# # goi api tu cac SDN 
apiSDN.call_topo_api_sdn(list_ip)
print("DOC XONG TOPO")
apiSDN.call_host_api_sdn(list_ip)

number_ip = len(list_ip) + 1
print(number_ip)

topo_files = [PATH_ABSOLUTE + 'topos/topo_' + str(index_path) + '.json' for index_path in range(1, number_ip)]
host_files = [PATH_ABSOLUTE + 'hosts/host_' + str(index_path) + '.json' for index_path in range(1, number_ip)]

# sinh ra file hop nhat giua cac mang: topo.json va host.json 
connectGraph.connectGraph(topo_files, host_files)

# khoi tao topo rong
topo_network = CusTopo.Topo()
# add do thi topo.json va host.json vao topo
graph = Graph.Graph(topo_network, 'topo.json', 'host.json')

print("GRAPH")
print(graph)

# get tap host va server tronng topo
hosts   = topo_network.get_hosts()
servers = topo_network.get_servers()
name_hosts = [ip_host.replace('10.0.0.', 'h') for ip_host in hosts.keys()]
name_servers = [ip_server.replace('10.0.0.', 'h') for ip_server in servers.keys()]
print("HOST: ",name_hosts)
print("SO HOST: " , len(name_hosts))
host_can = json.load(open('/home/onos/Downloads/flaskSDN/flaskAPI/set_up/set_up_topo.json'))["hosts"]
print("CAN: ", len(host_can))

print("SERVERS: ", name_servers)
print("SO SERVERS: " , len(name_servers))
server_can = json.load(open('/home/onos/Downloads/flaskSDN/flaskAPI/set_up/set_up_topo.json'))["servers"]
print("CAN: ", len(server_can))