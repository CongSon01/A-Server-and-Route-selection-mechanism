import json
from requests.auth import HTTPBasicAuth
import requests

class BytesEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bytes):
            return obj.decode('utf-8')
        return json.JSONEncoder.default(self, obj)

def call_topo_api_sdn(list_ip):
    print("HELLo")
    for i in range(len(list_ip)):
        if list_ip[i]['controller'] == "onos":
            response = requests.get('http://' + list_ip[i]['ip'] + ':8181/onos/test/localTopology/getTopo',
                auth=HTTPBasicAuth('onos', 'rocks'))

        elif list_ip[i]['controller'] == "ryu":
            response = requests.get(
                'http://' + list_ip[i]['ip'] + ':8080/onos/test/localTopology/getTopo')
        with open('/home/onos/Downloads/A-Server-and-Route-selection-mechanism/flaskAPI/topos/topo_'+str(i+1)+'.json', 'w') as f:
            json.dump(response.content, f, cls=BytesEncoder)
        print(response)

def call_host_api_sdn(list_ip):
    print("HELLo2")
    for i in range(len(list_ip)):
        if list_ip[i]['controller'] == "onos":
            response = requests.get('http://' + list_ip[i]['ip'] + ':8181/onos/v1/hosts',
                auth=HTTPBasicAuth('onos', 'rocks'))

        elif list_ip[i]['controller'] == "ryu":
            response = requests.get(
                'http://' + list_ip[i]['ip'] + ':8080/onos/test/localTopology/getTopo')
        with open('/home/onos/Downloads/A-Server-and-Route-selection-mechanism/flaskAPI/hosts/host_'+str(i+1)+'.json', 'w') as f:
            json.dump(response.content, f, cls=BytesEncoder)
        print(response)

list_ip = [
      {"ip":"10.20.0.202", "controller": "onos","controller_port": 6653, "rest_port": 8181, "switches" : ["s1", "s2", "s3", "s60", "s4", "s5"]},
      {"ip":"10.20.0.203", "controller": "onos","controller_port": 6653, "rest_port": 8181, "switches" : ["s6", "s7", "s62", "s61", "s63", "s8"]},
      {"ip":"10.20.0.204", "controller": "onos","controller_port": 6653, "rest_port": 8181, "switches" : ["s89", "s92", "s91", "s90"]},
      {"ip":"10.20.0.205", "controller": "onos","controller_port": 6653, "rest_port": 8181, "switches" : ["s39", "s68", "s40", "s67", "s66"]},
      {"ip":"10.20.0.206", "controller": "onos","controller_port": 6653, "rest_port": 8181, "switches" : ["s41", "s64", "s9", "s65", "s10"]},
      {"ip":"10.20.0.207", "controller": "onos","controller_port": 6653, "rest_port": 8181, "switches" : ["s11", "s12", "s13", "s14"]},
      {"ip":"10.20.0.208", "controller": "onos","controller_port": 6653, "rest_port": 8181, "switches" : ["s54", "s53", "s52", "s51", "s82"]},
      {"ip":"10.20.0.209", "controller": "onos","controller_port": 6653, "rest_port": 8181, "switches" : ["s70", "s71", "s29", "s28"]},
      {"ip":"10.20.0.210", "controller": "onos","controller_port": 6653, "rest_port": 8181, "switches" : ["s27", "s15", "s72", "s73"]},
      {"ip":"10.20.0.211", "controller": "onos","controller_port": 6653, "rest_port": 8181, "switches" : ["s26", "s25", "s74", "s75", "s76", "s24"]},
      {"ip":"10.20.0.212", "controller": "onos","controller_port": 6653, "rest_port": 8181, "switches" : ["s23", "s77", "s22", "s78", "s79", "s21"]},
      {"ip":"10.20.0.213", "controller": "onos","controller_port": 6653, "rest_port": 8181, "switches" : ["s20", "s80", "s81", "s18"]},
      {"ip":"10.20.0.214", "controller": "onos","controller_port": 6653, "rest_port": 8181, "switches" : ["s16", "s17", "s19"]},
      {"ip":"10.20.0.215", "controller": "onos","controller_port": 6653, "rest_port": 8181, "switches" : ["s31", "s32", "s33", "s34", "s35", "s36"]},
      {"ip":"10.20.0.216", "controller": "onos","controller_port": 6653, "rest_port": 8181, "switches" : ["s69", "s38", "s37", "s85", "s86", "s59"]},
      {"ip":"10.20.0.217", "controller": "onos","controller_port": 6653, "rest_port": 8181, "switches" : ["s58", "s88", "s57", "s84", "s56", "s55"]},
      {"ip":"10.20.0.218", "controller": "onos","controller_port": 6653, "rest_port": 8181, "switches" : ["s50", "s49", "s48", "s83", "s47"]},
      {"ip":"10.20.0.219", "controller": "onos","controller_port": 6653, "rest_port": 8181, "switches" : ["s46", "s45", "s44", "s43", "s42", "s30"]}
  ]

# call_topo_api_sdn(list_ip)
call_host_api_sdn(list_ip)
