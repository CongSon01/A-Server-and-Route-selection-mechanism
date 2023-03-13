import sys
# from keras.models import load_model
import numpy as np

PATH_ABSOLUTE = "/usr/local/Downloads/A-Server-and-Route-selection-mechanism/"
sys.path.append(PATH_ABSOLUTE+'flaskAPI/linkTopo')
import learnWeight
# import predict_linkWeight, lstm_model
dicdata = [{
    "byteSent": 556,
    "byteReceived": 27630844,
    "IpSDN": "10.20.0.200",
    "src": "of:0000000000000001",
    "packetLoss": 0.08780589137688226,
    "dst": "of:0000000000000002",
    "label": 0,
    "delay": 146,
    "linkUtilization": 0.053605125332940304,
    "overhead": 37.6314
    },
    {
    "byteSent": 21655420,
    "byteReceived": 556,
    "IpSDN": "10.20.0.200",
    "src": "of:0000000000000004",
    "packetLoss": 0.09651080992406066,
    "dst": "of:0000000000000005",
    "label": 1,
    "delay": 886,
    "linkUtilization": 0.393645922541769,
    "overhead": 31.655976
    }
]
a = learnWeight.learnWeight()
for c in dicdata:
    a.get_learn_weight(c)