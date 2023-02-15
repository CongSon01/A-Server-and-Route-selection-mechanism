
# This is a basic forwarding component used in the article:
# Authors: Nam-Thang Hoang, Hai-Anh Tran, Cong-Son Duong, Le-Tuan Nguyen
# SOICT 

# In this program, there are 2 components: 
# Component 1: API to receive data from SINA system in the article: https://doi.org/10.3390/electronics11070975 
# data will be calculated by us QoS parameters save to local database
# Component 2: We implement apis to communicate with other SDNs with mechanism Adaptive Consistency and with CCDN

import logging
import sys

PATH_ABSOLUTE = "/home/onos/Downloads/A-Server-and-Route-selection-mechanism/"
sys.path.append(PATH_ABSOLUTE+'flaskAPI/dataBaseMongo')
sys.path.append(PATH_ABSOLUTE+'flaskAPI/linkTopo')

from flask import Flask, request, jsonify

# import database
import LinkVersion, learnWeight, lstmWeight
import updateWeight, LearnWeightModel
import pub
import time
import json
import requests

from updateRouteCost import RouteCost

# ignore log in flask
log = logging.getLogger('werkzeug')
log.setLevel(logging.INFO)

# Init app
app = Flask(__name__)

PATH_ABSOLUTE = "/home/onos/Downloads/A-Server-and-Route-selection-mechanism/"

sys.path.append(PATH_ABSOLUTE + 'utils')
from get_local_ip import get_local_ip
suffix = get_local_ip("ens33").split(".")[-1]

ip_ccdn = str(json.load(open(PATH_ABSOLUTE + 'config/config-' + suffix + '.json'))['ip_ccdn'])

update = updateWeight.updateWeight()
# update = RouteCost()

# _learnWeight = learnWeight.learnWeight()

# set start time of program
starttime = time.time()

# communicate with ryu controller
@app.route('/write_data_ryu/',  methods=['GET', 'POST'])
def write_data_ryu():
    content = request.data
    data = json.loads(content)
    if float(data['byteSent']) > 600 and float(data['byteReceived']) > 600:
        # Params.insert_n_data(data)
        pub.connectRabbitMQ(data=data)
    return 'Sondzai'


# communicate with onos controller
@app.route('/write_data/',  methods=['GET', 'POST'])
def write_data():
    if request.method == 'GET':
        return "Da nhan duoc GET"

    if request.method == 'POST':
        # app.logger.info("Da nhan dc POST")
        content = request.data.decode()
        dicdata = {}
        datas = content.split("&")

        # processing data
        for data in datas:
            d = data.split(":")
            if len(d) == 3:
                temp = [d[1], d[2]]
                dicdata[d[0]] = ":".join(temp)
            else:
                dicdata[d[0]] = d[1]

        #  remove default data
        check_overhead = (float(dicdata['byteSent']) + float(dicdata['byteReceived']))
        
        # if check_overhead > 15000000:
        if check_overhead > 600:
            print("****************** Cap nhat du lieu ******************")
            # push data to rabbit (mechanism pub/sub)
            # pub.connectRabbitMQ(data=dicdata)

            # # consume data from rabbit
            # update.read_params_from_rabbit()

            # Update QoS parameter and save to local database (using linkcost)
            update.write_update_link_to_data_base(link_data= dicdata)

            # # update link cost to DB
            # update.update_route_cost(link_data= dicdata)

            # ghi mac dinh vao ccdn de thong ke ve sau
            try:
                # upload link learn to ccdn database
                # lan truyen local data cho node khac
                write_ccdn()
            except:
                # neu thang nay loi thi kha nang do DB cac may khac chua bat
                print("GHI VAO CCDN LOI ~ NHO MONGOD")
        return content

def write_ccdn():
    # Get data from local and upload to ccdn database
    data = LinkVersion.get_multiple_data()
    url_ccdn = "http://" + ip_ccdn + ":5000/write_full_data/"
    requests.post(url_ccdn, data=json.dumps({'link_versions': data}))
    return 

@app.route('/write_link_version/',  methods=['GET', 'POST'])
def write_link_version():
    # API: receive data from other SDNs sent to
    if request.method == 'POST':
        content = request.data
        for data in json.loads(content)['link_versions']:
            data_search = { 'src': data['src'], 'dst': data['dst'] }
            if LinkVersion.is_data_exit(data_search=data_search):
                LinkVersion.update_many(data_search, data)
            else:
                LinkVersion.insert_data(data=data)
        return content

@app.route('/read_link_version/',  methods=['GET', 'POST'])
def read_link_version():
    # CCDN se doc api nay de get du lieu R may
    # API: get data from load send to CCDN when there is a request to read N_r SDNs
    if request.method == 'GET':
        data = LinkVersion.get_multiple_data()
        return jsonify({'link_versions': data})  # will return the json

@app.route('/write_W_SDN/',  methods=['GET', 'POST'])
def write_W_SDN():
    # API: Get N_w parameter from CCDN and write to local data of N_w SDNs
    if request.method == 'POST':
        W_contant = request.data
        learnWeight.write_W_SDN(int(W_contant))
        return W_contant

@app.route('/write_learn_link/',  methods=['GET', 'POST'])
def write_learn_link():
    # API: receive data from other SDNs sent to
    if request.method == 'POST':
        content = request.data
        for data in json.loads(content)['learn_link']:
            data_search = { 'src': data['src'], 'dst': data['dst'] }
            if LearnWeightModel.is_data_exit(data_search=data_search):
                LearnWeightModel.update_many(data_search, data)
            else:
                LearnWeightModel.insert_data(data=data)
        return content

@app.route('/read_learn_link/',  methods=['GET', 'POST'])
def read_learn_link():
    # API: get data from load send to CCDN when there is a request to read N_r SDNs
    if request.method == 'GET':
        data = LearnWeightModel.get_multiple_data()
        return jsonify({'learn_link': data})  # will return the json


if __name__ == '__main__':
    ip_local = str(json.load(open(PATH_ABSOLUTE+'config/config-' + suffix + '.json'))['ip_local'])
    app.run(host="0.0.0.0", debug=True, use_reloader=False)
