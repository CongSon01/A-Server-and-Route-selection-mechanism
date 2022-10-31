import sys
PATH_ABSOLUTE = "/home/onos/Desktop/paper1/paper1/"
sys.path.append(PATH_ABSOLUTE+'flaskAPI/dataBaseMongo')
sys.path.append(PATH_ABSOLUTE+'flaskAPI/linkTopo')

from flask import Flask, request, jsonify
import Params  # import from model
import LinkVersion, json

content = {'link_versions': [{
    "byteSent": 0,
    "src": "of:0000000000000054",
    "packetLoss": 0,
    "dst": "of:0000000000000024",
    "linkVersion": 0,
    "delay": 0,
    "linkUtilization": 0,
    "overhead": 0,
    "byteReceived": 0,
    "IpSDN": "10.20.0.214"
},{
    "byteSent": 0,
    "src": "of:0000000000000024",
    "packetLoss": 0,
    "dst": "of:0000000000000054",
    "linkVersion": 0,
    "delay": 0,
    "linkUtilization": 0,
    "overhead": 0,
    "byteReceived": 0,
    "IpSDN": "10.20.0.214"
},{
    "byteSent": 1,
    "src": "of:0000000000000054",
    "packetLoss": 1,
    "dst": "of:0000000000000024",
    "linkVersion": 1,
    "delay": 1,
    "linkUtilization": 1,
    "overhead": 1,
    "byteReceived": 1,
    "IpSDN": "10.20.0.214"
}]}
for data in content['link_versions']:
    data_search = { 'src': data['src'], 'dst': data['dst'] }
    if LinkVersion.is_data_exit(data_search=data_search):
        LinkVersion.update_many(data_search, data)
    else:
        LinkVersion.insert_data(data=data)