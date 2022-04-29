
import requests
import json
from requests.auth import HTTPBasicAuth

def call_topo_api_sdn(list_ip):
  
    for ip in range(len(list_ip)):
      response = requests.get('http://' + list_ip[ip] + ':8181/onos/test/localTopology/getTopo',
      auth=HTTPBasicAuth('onos', 'rocks'))

      with open('/home/onos/Downloads/flaskSDN/flaskAPI/topos/topo_'+str(ip+1)+'.json', 'w') as f:
            json.dump(response.content, f)
    # print(response)


def call_host_api_sdn(list_ip):

    for ip in range(len(list_ip)):
      response = requests.get('http://' + list_ip[ip] + ':8181/onos/v1/hosts',
      auth=HTTPBasicAuth('onos', 'rocks'))

      with open('/home/onos/Downloads/flaskSDN/flaskAPI/hosts/host_'+str(ip+1)+'.json', 'w') as f:
            json.dump(response.content, f)