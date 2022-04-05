
import requests
import json
from requests.auth import HTTPBasicAuth

# def call_topo_api_sdn_1():
    
#     # print("GOI API TAP TOPO")
#     response = requests.get('http://10.20.0.250:8181/onos/test/localTopology/getTopo',
#       auth=HTTPBasicAuth('onos', 'rocks'))

#     with open('/home/onos/Downloads/flask_SDN/Flask-SDN/flaskAPI/topo_1.json', 'w') as f:
          # json.dump(response.content, f)
    # print(response)

def call_topo_api_sdn_2():
    
    # print("GOI API TAP TOPO")
    response = requests.get('http://10.20.0.248:8181/onos/test/localTopology/getTopo',
      auth=HTTPBasicAuth('onos', 'rocks'))

    with open('/home/onos/Downloads/flask_SDN/Flask-SDN/flaskAPI/topo_2.json', 'w') as f:
          json.dump(response.content, f)
    # print(response)


def call_host_api_sdn_1():

    response = requests.get('http://10.20.0.250:8181/onos/v1/hosts',
      auth=HTTPBasicAuth('onos', 'rocks'))

    with open('/home/onos/Downloads/flask_SDN/Flask-SDN/flaskAPI/host_1.json', 'w') as f:
          json.dump(response.content, f)

def call_host_api_sdn_2():

    response = requests.get('http://10.20.0.248:8181/onos/v1/hosts',
      auth=HTTPBasicAuth('onos', 'rocks'))

    with open('/home/onos/Downloads/flask_SDN/Flask-SDN/flaskAPI/host_2.json', 'w') as f:
          json.dump(response.content, f)
