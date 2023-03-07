
import requests
import json
from requests.auth import HTTPBasicAuth

class BytesEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bytes):
            return obj.decode('utf-8')
        return json.JSONEncoder.default(self, obj)
"""
  Lay topo tu onos 
"""


def call_topo_api_sdn(list_ip):
    # print("Doc Topo API")
    for i in range(len(list_ip)):
        try:
            if list_ip[i]['controller'] == "onos":
                response = requests.get('http://' + list_ip[i]['ip'] + ':8181/onos/test/localTopology/getTopo',
                    auth=HTTPBasicAuth('onos', 'rocks'))
                print("DOC TOPO ", list_ip[i]['ip'], response)
                

            elif list_ip[i]['controller'] == "ryu":
                response = requests.get(
                    'http://' + list_ip[i]['ip'] + ':8080/onos/test/localTopology/getTopo')
            with open('/home/onos/Downloads/A-Server-and-Route-selection-mechanism/flaskAPI/topos/topo_'+str(i+1)+'.json', 'w') as f:
                json.dump(response.content, f, cls=BytesEncoder)
        except requests.exceptions.RequestException as e:
             print("Error when calling topo API from", list_ip[i]['ip'])
            #  print(response)


def call_host_api_sdn(list_ip):
    # print("Doc host API")
    for i in range(len(list_ip)):
        if list_ip[i]['controller'] == "onos":
            response = requests.get('http://' + list_ip[i]['ip'] + ':8181/onos/v1/hosts',
                auth=HTTPBasicAuth('onos', 'rocks'))
            print("DOC HOST ", list_ip[i]['ip'], response)
            

        elif list_ip[i]['controller'] == "ryu":
            response = requests.get(
                'http://' + list_ip[i]['ip'] + ':8080/onos/test/localTopology/getTopo')
        with open('/home/onos/Downloads/A-Server-and-Route-selection-mechanism/flaskAPI/hosts/host_'+str(i+1)+'.json', 'w') as f:
            json.dump(response.content, f, cls=BytesEncoder)
        # print(response)
