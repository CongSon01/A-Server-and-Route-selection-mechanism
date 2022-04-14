import sys
PATH_ABSOLUTE = "/home/onos/Downloads/flask_SDN/Flask-SDN/"
sys.path.append(PATH_ABSOLUTE+'flaskAPI/dataBaseMongo')
sys.path.append(PATH_ABSOLUTE+'flaskAPI/linkTopo')

from flask import Flask, request, jsonify
import Params  # import from model
import LinkVersion
import updateWeight  # import from routingAlgorithm
import pub
import time
import json


# Init app
app = Flask(__name__)

# init W object included link version of each link
update = updateWeight.updateWeight()
starttime = time.time()
WD_starttime = time.time()
# WD = 0

@app.route('/write_data/',  methods=['GET', 'POST'])
def write_data():
    if request.method == 'GET':
        return "Da nhan duoc GET"

    if request.method == 'POST':
        # app.logger.info("Da nhan dc POST")
        content = request.data
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

        #  Khong chon data mac dinh
        if float(dicdata['byteSent']) > 600 and float(dicdata['byteReceived']) > 600:
            pub.connectRabbitMQ(data=dicdata)
            update.read_params_from_rabbit()
            Params.insert_data(dicdata)

        # Sau 60s se lan truyen DB den cac SDN khac
        # global starttime, WD_starttime, WD
        global starttime
        
        if time.time() - starttime > 30:
            write_time = time.time() - starttime
            # viet trong so ra local SDN
            update.write_update_link_to_data_base(write_time)
            starttime = time.time()
            # viet trong so ra nhieu SDN khac
            
            # WD = time.time()
            update.write_W_SDN()
            # WD = time.time - WD_starttime

        return content


@app.route('/write_link_version/',  methods=['GET', 'POST'])
def write_link_version():
    if request.method == 'POST':
        # app.logger.info("Da nhan dc POST")
        content = request.data
        LinkVersion.insert_n_data(json.loads(content)['link_versions'])
        print("Ghi vao local SDN thanh cong")
        return content


@app.route('/read_link_version/',  methods=['GET', 'POST'])
def read_link_version():
    # global WD
    if request.method == 'GET':
        data = LinkVersion.get_multiple_data()
        return jsonify({'link_versions': data})  # will return the json
        # return Response(json.dumps(data),  mimetype='application/json')


if __name__ == '__main__':
    ip_local = str(json.load(open(PATH_ABSOLUTE+'/config.json'))['ip_local'])
    app.run(host='10.20.0.248', debug=True, use_reloader=False)