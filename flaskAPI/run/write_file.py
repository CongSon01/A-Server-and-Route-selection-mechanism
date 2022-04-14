filename = '/home/onos/Downloads/flaskSDN/flaskAPI/run/bridge.txt'
import json
# JSON file
# Using readlines()
file1 = open(filename, 'r')
Lines = file1.readlines()
 
count = 0
# Strips the newline character
for line in Lines:
    print(json.loads(line))