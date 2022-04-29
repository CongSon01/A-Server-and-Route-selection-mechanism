filename = '/home/onos/Downloads/flaskSDN/flaskAPI/run/bridge.txt'
import json
file1 = open(filename, 'r')
Lines = file1.readlines()

list_bridges = [ json.loads(host)['src']['id'] for host in Lines ]            

print(list_bridges)
