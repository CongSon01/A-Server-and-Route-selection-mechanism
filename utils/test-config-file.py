import json
import requests

url = "http://localhost:5000//getIpServerBasedService"
data = {

    "host_ip": "10.0.0.1",
    "server_ip": "10.0.0.11",
    "service_type": 0
}
response = requests.post("http://10.20.0.201:5000/getIpServerBasedService", data= json.dumps(data))  
# response = requests.post(url, json = data)

# set_up_topo = json.load(open('/home/onos/Downloads/A-Server-and-Route-selection-mechanism/flaskAPI/set_up/set_up_topo.json'))

# service = set_up_topo['service-server']
# print(service['1'])
