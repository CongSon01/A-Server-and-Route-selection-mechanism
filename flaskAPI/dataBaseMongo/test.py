import sys
PATH_ABSOLUTE = "/home/onos/Downloads/flask_SDN/Flask-SDN/"
sys.path.append(PATH_ABSOLUTE+'flaskAPI/dataBaseMongo')
sys.path.append(PATH_ABSOLUTE+'flaskAPI/linkTopo')

from flask import Flask, request, jsonify
import Params  # import from model
import LinkVersion

LinkVersion.update_many(data_search={'src': 'of:0000000000000024', 'dst': 'of:0000000000000054'}, data_update={'LinkVersion': 99})
print(LinkVersion.is_data_exit(data_search={'src': 'of:0000000000000024', 'dst': 'of:0000000000000054'}))