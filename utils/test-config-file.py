import json

set_up_topo = json.load(open('/home/onos/Downloads/A-Server-and-Route-selection-mechanism/flaskAPI/set_up/set_up_topo.json'))

service = set_up_topo['service-server']
print(service['1'])
