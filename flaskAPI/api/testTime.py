from flask import Flask, request, Response, jsonify


import sys, os, json
PATH_ABSOLUTE = "/home/onos/Downloads/flask_SDN/Flask-SDN/flaskAPI/"
IS_RUN_RRBIN = False

sys.path.append(PATH_ABSOLUTE+'model')
sys.path.append(PATH_ABSOLUTE+'handledata/models')
sys.path.append(PATH_ABSOLUTE+'core')
sys.path.append(PATH_ABSOLUTE+'routingAlgorithm')

# import from model
import Params, LinkVersion

# import from handledata/models 
import CusTopo

# import from core
import connectGraph, Graph

# import from routingAlgorithm
import destQueueRabbit, DijkstraLearning, Round_robin, updateServerCost, updateWeight

# import inside folder
import pub
import apiSDN
import time
import requests


# goi api tu cac SDN 
apiSDN.call_topo_api_sdn_1()
apiSDN.call_topo_api_sdn_2()
apiSDN.call_host_api_sdn_1()
apiSDN.call_host_api_sdn_2()

topo_path_1 = PATH_ABSOLUTE + 'topo_1.json'
topo_path_2 = PATH_ABSOLUTE + 'topo_2.json'
host_path_1 = PATH_ABSOLUTE + 'host_1.json'
host_path_2 = PATH_ABSOLUTE + 'host_2.json'
topo_files = [topo_path_1, topo_path_2]
host_files = [host_path_1, host_path_2]
# sinh ra file hop nhat giua cac mang: topo.json va host.json 
connectGraph.connectGraph(topo_files, host_files)

# khoi tao topo rong
topo_network = CusTopo.Topo()
# add do thi topo.json va host.json vao topo
graph = Graph.Graph(topo_network, 'topo.json', 'host.json')


#print(topo_network.get_topo(), "\n")
# get tap host va server tronng topo
hosts = topo_network.get_hosts()
servers = topo_network.get_servers()
print(hosts)
print(servers)

# khoi tao bien CAP NHAP SERVER COST
update_server = updateServerCost.updateServerCost(servers)
# khoi tao bien CAP NHAP LINK COST
update = updateWeight.updateWeight(topo= topo_network)

try:
    data_250 = requests.get("http://10.20.0.248:5000/read_link_version/") 

    LinkVersions = json.loads(data_250.text)

    print(len(LinkVersions['link_versions']))
    LinkVersion.remove_all()
    print("XOa thanh cong")
    print("GHI ", len(LinkVersions['link_versions']), " vao DB")
    LinkVersion.insert_n_data(LinkVersions['link_versions'])
              # print(data_250.text)
except:
    print("flask Doc data loi")
          # Ghi W ong
try:
    data = LinkVersion.get_multiple_data()
    print("GHI W ONG")
    print (len(data) )
    requests.post("http://10.20.0.250:5000/write_link_version/", data= json.dumps({'link_versions':data}) )
except:
    print("flask Goi nhieu SDN loiiiiiiiiiiiiiiiiiiiii")

try:
    data_250 = requests.get("http://10.20.0.248:5000/read_link_version/") 

    LinkVersions = json.loads(data_250.text)

    print(len(LinkVersions['link_versions']))
    LinkVersion.remove_all()
    print("XOa thanh cong")
    print("GHI ", len(LinkVersions['link_versions']), " vao DB")
    LinkVersion.insert_n_data(LinkVersions['link_versions'])
              # print(data_250.text)
except:
    print("flask Doc data loi")
          # Ghi W ong
try:
    data = LinkVersion.get_multiple_data()
    print("GHI W ONG")
    print (len(data) )
    requests.post("http://10.20.0.250:5000/write_link_version/", data= json.dumps({'link_versions':data}) )
except:
    print("flask Goi nhieu SDN loiiiiiiiiiiiiiiiiiiiii")