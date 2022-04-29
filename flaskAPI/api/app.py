from concurrent.futures import thread
from flask import Flask, request, jsonify

import sys, json
import random
PATH_ABSOLUTE = "/home/onos/Downloads/flaskSDN/flaskAPI/"
IS_RUN_RRBIN = False
IS_RUN_QLEARNING = True

sys.path.append(PATH_ABSOLUTE+'model')
sys.path.append(PATH_ABSOLUTE+'handledata/models')
sys.path.append(PATH_ABSOLUTE+'core')
sys.path.append(PATH_ABSOLUTE+'routingAlgorithm')
sys.path.append(PATH_ABSOLUTE+'q_learning')

import custom_env


# import from handledata/models 
import CusTopo

# import from core
import connectGraph, Graph

# import from routingAlgorithm
import destQueueRabbit, DijkstraLearning, Round_robin, updateServerCost
# import inside folder
import ccdn
import apiSDN, Full_Data
import time
import threading
import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
# Init app
app = Flask(__name__)

# get full ip of SDN
list_ip = json.load(open('/home/onos/Downloads/flaskSDN/flaskAPI/set_up/set_up_topo.json'))['ip_sdn']

# # goi api tu cac SDN 
apiSDN.call_topo_api_sdn(list_ip)
apiSDN.call_host_api_sdn(list_ip)

topo_files = [PATH_ABSOLUTE + 'topos/topo_' + str(index_path) + '.json' for index_path in range(1, 5)]
host_files = [PATH_ABSOLUTE + 'hosts/host_' + str(index_path) + '.json' for index_path in range(1, 5)]

# sinh ra file hop nhat giua cac mang: topo.json va host.json 
connectGraph.connectGraph(topo_files, host_files)

# khoi tao topo rong
topo_network = CusTopo.Topo()
# add do thi topo.json va host.json vao topo
graph = Graph.Graph(topo_network, 'topo.json', 'host.json')

# get tap host va server tronng topo
hosts   = topo_network.get_hosts()
servers = topo_network.get_servers()

############################ CCDN ###############################
update_server = updateServerCost.updateServerCost(servers)
update_weight = ccdn.Update_weight_ccdn(topo= topo_network, update_server= update_server, list_ip=list_ip)

if IS_RUN_RRBIN:
    # print("Doc Queue 1 lan duy nhat")
    # print(servers)
    # khoi tao queue co che Round robin
    queue_rr = destQueueRabbit.destQueueRabbit()

    # day tap server vao rabbit queue
    for ip in servers:
      queue_rr.connectRabbitMQ(ip_dest= ip)

# khoi tao bien CAP NHAP SERVER COST
# update_server = updateServerCost.updateServerCost(servers)

priority = 200
starttime = time.time()
      
@app.route('/getIpServer', methods=['POST'])

def get_ip_server():
  """
    input: ip_host
    output: ip_server
  """
  if request.method == 'POST':
    host_ip = request.data
    # print(host_ip)
    global priority 
    priority +=1

    # chay thuat toan Round Robin 
    if IS_RUN_RRBIN:
      object = Round_robin.hostServerConnectionRR(queue_rr, topo_network, hosts, servers, priority)
    # chay thuat toan Dinjkstra
    else:
      object = DijkstraLearning.hostServerConnection(topo_network, hosts, servers, priority)

    # truyen ip xuat phat va lay ra ip server dich den
    object.set_host_ip(host_ip= str(host_ip))
    dest_ip = object.find_shortest_path()

  return str(dest_ip)


@app.route('/write_full_data/',  methods=['GET', 'POST']) 
def write_full_data():
    if request.method == 'POST':
        # app.logger.info("Da nhan dc POST")
        content = request.data
        Full_Data.insert_n_data(json.loads(content)['link_versions'])
        return content


# threading flask api
def flask_ngu():
  app.run(host='10.20.0.201',debug=True, use_reloader=False, threaded=True)

def get_x(x):
    if (x >= 4):
        return 4
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
#     R = 4
#     W = 1
#     while True:
#         # print("123")
#         if time.time() - ", last_device_idstarttime > 10:
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
#             RD, WD, V_staleness = update_weight.load_CCDN(R, W)
            
#             new_state, reward, done = env.step(RD, WD, V_staleness)

#             # cap nhap trong so cho server
#             update_server.update_server_cost()
#             starttime = time.time()
                
#             if done:
#                 break
#             state = new_state

## fix cung R, W
def ccdn():
    global starttime
    R = 4
    W = 1
    while True:
        if time.time() - starttime > 60:
            RD, WD, V_staleness = update_weight.load_CCDN(R, W)
            # cap nhap trong so cho server
            update_server.update_server_cost()
            starttime = time.time()
          
            

if __name__ == '__main__':
    threading.Thread(target=flask_ngu).start()
    threading.Thread(target=ccdn).start()