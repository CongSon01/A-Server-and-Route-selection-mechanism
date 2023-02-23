from json import encoder
from flask import Flask, request, jsonify

import sys, json
from bson import json_util
import ast

PATH_ABSOLUTE = "/home/onos/Downloads/A-Server-and-Route-selection-mechanism/"
IS_RUN_RRBIN = False
# IS_RUN_QLEARNING = True

sys.path.append(PATH_ABSOLUTE+'flaskAPI/model')
sys.path.append(PATH_ABSOLUTE+'flaskAPI/handledata/models')
sys.path.append(PATH_ABSOLUTE+'flaskAPI/core')
sys.path.append(PATH_ABSOLUTE+'flaskAPI/run')
sys.path.append(PATH_ABSOLUTE+'flaskAPI/routingAlgorithm')
sys.path.append(PATH_ABSOLUTE+'flaskAPI/routingAlgorithm/updateRoute')

sys.path.append(PATH_ABSOLUTE+'flaskAPI/q_learning')


import numpy as np
import generate_topo
import DijkstraLearning, Round_robin
import ccdn
import time, Full_Data, EndPointModel,updateEndPointModel
import threading
import logging

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
# Init appV
app = Flask(__name__)

# get service-server mapping from config file
service_server_mapping = json.load(open(
    PATH_ABSOLUTE + 'flaskAPI/set_up/set_up_topo.json'))["service-server"]

# get full ip of SDN
list_ip = json.load(open(
    PATH_ABSOLUTE + 'flaskAPI/set_up/set_up_topo.json'))["controllers"]

number_ip = len(list_ip) + 1

generate_topo_info = generate_topo.generate_topo_info()
generate_topo_info.get_api()
# hien thi thong tin cac canh trong do thi
# print("thong tin canh trong do thi")
# generate_topo_info.display_topo_infor()

topo_network = generate_topo_info.get_topo_from_api()
# add do thi topo.json va host.json vao topo
graph = generate_topo_info.get_graph_from_api()

# get tap host va server tronng topo
hosts = generate_topo_info.get_host_from_api()
# servers = generate_topo_info.get_topo_from_api()
servers = generate_topo_info.get_server_from_api()


print("HOSTSsssss: ")
print(hosts.keys())

print("SERVERrrrrr: ")
print(servers.keys())
############################ CCDN ###############################
update_server = updateEndPointModel.updateEndPointModel(servers)
update_weight = ccdn.Update_weight_ccdn(
    topo=topo_network, update_server=update_server, list_ip=list_ip)

priority = 200
starttime = time.time()
index_server = 0

########################### route service anh hoang goi den
@app.route('/getIpServerBasedService', methods=['GET', 'POST'])
def get_ip_server_based_service():
    """
      input: ip_host
      output: ip_server
    """
    if request.method == 'POST':
        global priority
        global index_server
        priority += 10
        print("toi da di vao day")
        # input = json.loads(request.data, object_pairs_hook=deunicodify_hook)
        content = request.data
#       for learn_weight in json.loads(content)['learn_weights']:
        print("Errrrrrrrrrrrrrrrrrrrrrrrrrrr = ", content)
        host_ip = json.loads(content, object_pairs_hook=deunicodify_hook)['host_ip']
        print(host_ip)

        # end_point = json.loads(content)['EndPoint_datas']
        
        if host_ip not in hosts:
            return "not in hosts", 200
        host_object = hosts[host_ip]
        host_key_value = {
            host_ip: host_object
        }

        service_type = json.loads(content)['service_type']# string 

        server_ip = json.loads(content, object_pairs_hook=deunicodify_hook)['server_ip']# string
        server_object = servers[server_ip]
        server_key_value = {
            server_ip: server_object
        }


        print("Tap hosts va servers")
        print(host_key_value)
        print(server_key_value)

        '''filter server based services: de ve sau tai su dung 
        lay cum ip cua server theo service
        servers_ip_list = service_server_mapping[service_type]
        lay tap dictionary serverIp-serverObject theo service
        servers_objects = get_server_objects_from(servers_ip_list)
        print(servers_objects)

        thay doi params hostServerConnection(topo_network, hosts, servers_objects, priority)  
        '''

        # khoi tao object routing
        object = DijkstraLearning.hostServerConnection(topo_network, host_key_value, server_key_value, priority)  
        # truyen ip xuat phat va lay ra ip server dich den
        object.set_host_ip(host_ip=str(host_ip))
        dest_ip = object.find_shortest_path()

        return str(dest_ip)

def get_server_objects_from(servers_ip_list):

    results = dict()
    for server_ip in servers_ip_list:
        server_ip = '10.0.0.' + server_ip.encode('utf-8')[1:]
        server_object = topo_network.get_server_object(server_ip)
        # key_value = {
        #     server_ip: server_object
        # }
        results[server_ip] = server_object
    return results
        
@app.route('/getIpServer', methods=['POST'])
def get_ip_server():
    """
      input: ip_host
      output: ip_server
    """
    if request.method == 'POST':
        global priority
        global index_server
        priority += 10

        # chay thuat toan Round Robin
        if IS_RUN_RRBIN:
            if index_server < len(servers):
                host_ip = request.data
                print("HOST IP: ", host_ip)
                object = Round_robin.hostServerConnectionRR(
                        topo_network, hosts, servers, index_server, priority)
                # truyen ip xuat phat va lay ra ip server dich den
                object.set_host_ip(host_ip=str(host_ip))
                dest_ip = object.find_shortest_path()
                index_server += 1
                print("Server: ", dest_ip)
                return str(dest_ip)
            else:
                host_ip = request.data
                print("HOST IP: ", host_ip)
                index_server = 0
                # truyen ip xuat phat va lay ra ip server dich den
                object = Round_robin.hostServerConnectionRR(topo_network, hosts, servers, index_server, priority)
                object.set_host_ip(host_ip=str(host_ip))
                
                dest_ip = object.find_shortest_path()
                print("Server: ", dest_ip)
                return str(dest_ip)

        # chay thuat toan Dijkstra
        else:
            host_ip = request.data
            object = DijkstraLearning.hostServerConnection(topo_network, hosts, servers, priority)
            # object = LSTM_Learning.hostServerConnection(
            #     topo_network, hosts, servers, priority)

            # truyen ip xuat phat va lay ra ip server dich den
            object.set_host_ip(host_ip=str(host_ip))
            update_server.update_server_cost()
            dest_ip = object.find_shortest_path()

            return str(dest_ip)

def deunicodify_hook(pairs):
    new_pairs = []
    for key, value in pairs:
        if isinstance(value, unicode):
            value = value.encode('utf-8')
        if isinstance(key, unicode):
            key = key.encode('utf-8')
        new_pairs.append((key, value))
    return dict(new_pairs)


@app.route('/write_full_data/',  methods=['GET', 'POST'])
def write_full_data():
  if request.method == 'POST':
    content = request.data
    data = json.loads(content,  object_pairs_hook=deunicodify_hook)
    #   del data["_id"]
    Full_Data.insert_n_data([data['link_versions']])
    # print(data)
    return content

# Lay BW
@app.route('/write_EndPoint/',  methods=['GET', 'POST'])
def write_EndPoint():
  if request.method == 'POST':
    content = request.data
    # print(json.loads(content)['EndPoint_datas'])
    end_point = json.loads(content)['EndPoint_datas']
    data_search = {
        'srcLink': end_point['srcLink'], 'portInfo': end_point['portInfo']}
    if EndPointModel.is_data_exit(end_point):
        EndPointModel.update_many(data_search, end_point)
    else:
        EndPointModel.insert_data(end_point)
    return content

from updateRouteCost import RouteCost
route_cost = RouteCost(topo=topo_network, list_ip=list_ip)

# Lay BW
@app.route('/update_cost_base_on_service',  methods=['GET', 'POST'])
def update_cost():
  if request.method == 'POST':
    print("chay update cost based on services")
    """
    content: service type (int): 1,2,3,4
    """

    try:
        content = request.data
        service_type = json.loads(content)['service_type']
        print(service_type)

        # content = json.loads(request.data, object_pairs_hook=deunicodify_hook)
        # content = request.data

        route_cost.read_R_links_data_from_other_domains(3)
        route_cost.update_route_cost_in_data_base(service_type)
        route_cost.pull_new_cost_to_topology()
        # print("Typeeeeeeeeeeeeeeeeeeeee")
        # print(type(content['service_type']))
    except Exception as ex:
        print(ex)
    
    return content

# @app.route('/write_learn_weights/',  methods=['GET', 'POST'])
# def write_learn_weights():
#   if request.method == 'POST':
#       # app.logger.info("Da nhan dc POST")
#       content = request.data
#       for learn_weight in json.loads(content)['learn_weights']:
#           data_search = {
#               'src': learn_weight['src'], 'dst': learn_weight['dst']}
#           if LearnWeightModel.is_data_exit(learn_weight):
#               LearnWeightModel.update_many(data_search, learn_weight)
#           else:
#               LearnWeightModel.insert_data(learn_weight)
#       return content

# threading flask api


def flask_ngu():
    app.run(host='10.20.0.201', debug=True, use_reloader=False, threaded=True)


def get_x(x):
    if (x >= number_ip-1):
        return number_ip-1
    elif (x <= 0):
        return 1
    else:
        return x


def change_acction(x, r, w):
    # print(r, w)
    return {
        0: (get_x(r - 1), get_x(w - 1)),
        1: (get_x(r - 1), get_x(w)),
        2: (get_x(r - 1), get_x(w + 1)),
        3: (get_x(r), get_x(w - 1)),
        4: (get_x(r), get_x(w)),
        5: (get_x(r), get_x(w + 1)),
        6: (get_x(r + 1), get_x(w - 1)),
        7: (get_x(r + 1), get_x(w)),
        8: (get_x(r + 1), get_x(w + 1)),
    }[x]


# threading ccdn
# def ccdn():
#     global starttime
#     env = custom_env.Custom_env()
#     R = 18
#     W = 1
#     while True:
#         # print("123")
#         if time.time() - starttime > 60:
#             state = env.reset(R, W)
#             qtable_new = np.load('/home/onos/Downloads/flaskSDN/flaskAPI/api/qtable.npy')
#             print(state)
#             step = 0
#             done = False

#             env.render()
#             # Take the action (index) that have the maximum expected future reward given that state
#             if sum(qtable_new[state, :]) == 0:
#                 action = random.randint(0, 8)
#             else:
#                 action = np.argmax(qtable_new[state,:])

#             R, W = change_acction(action, R, W)
#             if R + W > 18:
#                   R = random.randint(4, 7)
#                   W = random.randint(4, 7)
#             RD, WD, V_staleness = update_weight.load_CCDN(R, W)

#             new_state, reward, done = env.step(RD, WD, V_staleness)

#             # cap nhap trong so cho server
#             update_server.update_server_cost()
#             starttime = time.time()

#             if done:
#                 break
#             state = new_state

# fix cung R, W
def ccdn():
    global starttime
    R = 4
    W = 0
    while True:
        if time.time() - starttime > 45:
            RD, WD, V_staleness = update_weight.load_CCDN(R, W)

            # cap nhap trong so cho server
            # update_server.update_server_cost()
            starttime = time.time()

if __name__ == '__main__':
    # threading.Thread(target=flask_ngu).start()
    app.run(host='10.20.0.201', debug=True, use_reloader=True)
    # tat luong ccdn de chay luong anh hoang
    # threading.Thread(target=ccdn).start()

# cmt dong 192 va 194 de chay round robin
