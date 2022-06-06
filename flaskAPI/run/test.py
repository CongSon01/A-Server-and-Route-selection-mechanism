# switch_in_controllers =  {
#     "sw_0" : [85,84,86,63,87,88],
#     "sw_1" : [89,90,38,39,37],
#     "sw_2" : [19,31,30,18,33,1],
#     "sw_3" : [34,55,36,91,82],
#     "sw_4" : [35,83,22,23,20],
#     "sw_5" : [73,46,21,40,79],
#     "sw_6" : [78,2,3,4,5,6],
#     "sw_7" : [7,11,8,10,62],
#     "sw_8" : [9,41,0,32],
#     "sw_9" : [65,12,64,16,67,66],
#     "sw_10" : [69,68,71,70,14,52],
#     "sw_11" : [53,60,17,61,58],
#     "sw_12" : [59,56,57,54,72],
#     "sw_13" : [26,47,48,80,81],
#     "sw_14" : [27,24,25,15],
#     "sw_15" : [28,51,29,13],
#     "sw_16" : [77,50,45,76,44],
#     "sw_17" : [75,74,43,42,49]
#   }

# for key in switch_in_controllers:
#     for i in switch_in_controllers[key]:
#         print('ping: ',switch_in_controllers[key][0], '->', i)
#     print('-----')

# a =  [[11, 18], [2,14], [7, 8], [25, 26], [20, 28]]

# a = sum(a, [])

# a_new  = [i-1 for i in a]
# new = []

# new = [i for i in range(28) if i not in a_new]

# print(new)


import random
import time

from numpy import full


# h = ['h1','h2','h3','h4','h5','h6','h7','h8']
# h = ['h1','h2']
# period = 10
# life_time = 10
# interval = 2
# generate_flow = {}
# # generate_flow = {0: {'h2': 569, 'h1': 441}, 1: {'h2': 358, 'h1': 366}, 2: {'h2': 302, 'h1': 315}}
# for i in range(interval):
#     temp = {}
#     if i == 0:
#         for h_i in h:
#             temp[h_i] = random.randint(1, period)
#     else:
#         for h_i in h:
#             temp[h_i] =  generate_flow[i-1][h_i] + life_time + random.randint(0, 3)
#     generate_flow[i] = temp


# print(generate_flow)

# generate_flow = {0: {'h1': 4, 'h2': 8, 'h3': 7}, 1: {'h1': 26, 'h2': 29, 'h3': 29}, 2: {'h1': 46, 'h2': 51, 'h3': 52}, 3: {'h1': 67, 'h2': 72, 'h3': 75}, 4: {'h1': 90, 'h2': 95, 'h3': 98}}
# print(generate_flow.values())
# full_times = sum([ list(start_host.values()) for start_host in list(generate_flow.values()) ], [])
# full_values = [ start_host for start_host in generate_flow.values() ]
# full_times = []
# print(min(full_times))
# print(full_times)

# def get_host_affter_time(full_values, run_time):
#     for cluster_host in full_values:
#         for host in cluster_host:
#             if cluster_host[host] == run_time:
#                 return host

# # # # while True:
# start_time = time.time()
# stop_time = max(full_times)
# while True:
#     current_time = time.time() - start_time
#     if ( current_time in  full_times):
#         print(get_host_affter_time(full_values, current_time))
#     if ( current_time == stop_time ):
#         print("DONE")
#         break
# print("OK")

# import sys
# sys.path.append('/home/onos/Downloads/flaskSDN/flaskAPI/run/')


# start_time  = time.time()
# i = 0
# while True:
#     current = int(time.time() - start_time)
#     print(current)
#     if current > 10:
#         break

import json, requests
from requests.auth import HTTPBasicAuth
# switch_in_controllers = json.load(open('/home/onos/Downloads/flaskSDN/flaskAPI/set_up/set_up_topo.json'))['switch_in_controllers']

# for key in switch_in_controllers:
#     for i in switch_in_controllers[key]:
#         for j in range(len(switch_in_controllers[key])):
#             print(switch_in_controllers[key][j] , i)

# response = requests.get('http://' + '10.20.0.210' + ':8181/onos/v1/hosts', auth=HTTPBasicAuth('onos', 'rocks'))


# response_1 = requests.get('http://' + '10.20.0.209' + ':8080/onos/test/localTopogy/getTopo')

# print(response.text)

# print("-----")

# print({"hosts": json.loads(response_1.content)['hosts']})

# def call_routing_api_flask(host):
#     print("call flask")
#     response = requests.post("http://10.20.0.201:5000/getIpServer", data= host)  
#     dest_ip = response.text
#     return str(dest_ip)

# des = call_routing_api_flask( '10.0.0.16' )
# print("TRUYEN DU LIEU ", '10.0.0.16', "--->", des)



# controllers = [ 
#       {"ip":"10.20.0.200", "controller": "onos","controller_port": 6653, "rest_port": 8181, "switches" : ["s85","s84","s86","s63","s87","s88"]},
#       {"ip":"10.20.0.209", "controller": "ryu" ,"controller_port": 6633, "rest_port": 8080, "switches" : ["s89","s90","s38","s39","s37"]},
#       {"ip":"10.20.0.210", "controller": "onos" ,"controller_port": 6653, "rest_port": 8181, "switches" : ["s19","s31","s30","s18","s33","s1"]},
#       {"ip":"10.20.0.211", "controller": "ryu" ,"controller_port": 6633, "rest_port": 8080, "switches" : ["s34","s55","s36","s91","s82"]}
#   ]
# switch_in_controllers = {
#         "sw_0":[10,11,12,15,16,17,13],
#         "sw_1":[4,5,7,8,9],
#         "sw_2":[0,1,2,3,6,14,19,25,26],
#         "sw_3":[18,20,21,22,23,24,27]
# }
# new = {}
# for b in switch_in_controllers:
#     lists_tmp = []
#     for sw in switch_in_controllers[b]:
#         lists_tmp.append("s" + str(sw + 1))
#     print(lists_tmp)

import run_final
net = run_final.get_net()
hosts_save = run_final.get_hosts_save()