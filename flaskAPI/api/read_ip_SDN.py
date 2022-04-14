from concurrent.futures import thread
from flask import Flask, request, jsonify

import sys, json
import random
PATH_ABSOLUTE = "/home/onos/Downloads/flaskSDN/flaskAPI/"
IS_RUN_RRBIN = False

sys.path.append(PATH_ABSOLUTE+'model')
sys.path.append(PATH_ABSOLUTE+'handledata/models')
sys.path.append(PATH_ABSOLUTE+'core')
sys.path.append(PATH_ABSOLUTE+'routingAlgorithm')


# import from handledata/models 
import CusTopo

# import from core
import connectGraph, Graph

# import from routingAlgorithm
import destQueueRabbit, DijkstraLearning, Round_robin, updateServerCost

import ccdn
# import inside folder
import pub
import apiSDN
import time
import requests
import threading
import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
# Init app
app = Flask(__name__)

# get full ip of SDN
list_ip = json.load(open('/home/onos/Downloads/flaskSDN/flaskAPI/set_up/ip_SDN.json'))['ip_sdn']

# goi api tu cac SDN 
# apiSDN.call_topo_api_sdn(list_ip)
# apiSDN.call_host_api_sdn(list_ip)

topo_path_1 = PATH_ABSOLUTE + 'topo_1.json'
topo_path_2 = PATH_ABSOLUTE + 'topo_2.json'
topo_path_3 = PATH_ABSOLUTE + 'topo_3.json'
topo_path_4 = PATH_ABSOLUTE + 'topo_4.json'
host_path_1 = PATH_ABSOLUTE + 'host_1.json'
host_path_2 = PATH_ABSOLUTE + 'host_2.json'
host_path_3 = PATH_ABSOLUTE + 'host_3.json'
host_path_4 = PATH_ABSOLUTE + 'host_4.json'
topo_files = [topo_path_1, topo_path_2, topo_path_3, topo_path_4]
host_files = [host_path_1, host_path_2, host_path_3, host_path_4]

# # sinh ra file hop nhat giua cac mang: topo.json va host.json 
connectGraph.connectGraph(topo_files, host_files)

# khoi tao topo rong
topo_network = CusTopo.Topo()
# add do thi topo.json va host.json vao topo
graph = Graph.Graph(topo_network, 'topo.json', 'host.json')

#print(topo_network.get_topo(), "\n")
# get tap host va server tronng topo
hosts   = topo_network.get_hosts()
servers = topo_network.get_servers()

############################ CCDN ###############################
update_server = updateServerCost.updateServerCost(servers)
update_weight = ccdn.Update_weight_ccdn(topo= topo_network, update_server= update_server, list_ip=list_ip)

starttime = time.time()

def ccdn():
    global starttime
    while True:
        # print("123")
        if time.time() - starttime > 5:
          #  print("Time out")
          update_weight.read_R_SDN()
          # cap nhap trong so cho server
          update_server.update_server_cost()
          starttime = time.time()

ccdn()