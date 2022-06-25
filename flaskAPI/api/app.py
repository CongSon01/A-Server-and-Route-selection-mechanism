import logging
import sys

PATH_ABSOLUTE = "/home/onos/Downloads/flask_SDN/Flask-SDN/"
sys.path.append(PATH_ABSOLUTE+'flaskAPI/dataBaseMongo')
sys.path.append(PATH_ABSOLUTE+'flaskAPI/linkTopo')

from flask import Flask, request, jsonify
# import Params  # import from model
import LinkVersion, lstmWeight
import updateWeight, Lstm
import pub
import time
import json
import requests
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

# Init app
app = Flask(__name__)

# init W object included link version of each link
ip_ccdn = str(json.load(open('/home/onos/Downloads/flask_SDN/Flask-SDN/config.json'))['ip_ccdn'])
update = updateWeight.updateWeight()
starttime = time.time()

@app.route('/write_data_ryu/',  methods=['GET', 'POST'])
def write_data_ryu():
    content = request.data
    data = json.loads(content)
    if float(data['byteSent']) > 600 and float(data['byteReceived']) > 600:
        # Params.insert_n_data(data)
        pub.connectRabbitMQ(data=data)
    return 'Sondzai'



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
        check_overhead = (float(dicdata['byteSent']) + float(dicdata['byteReceived'])) / 20
        
        if check_overhead > 10000000:
            # day data vao rabbit
            pub.connectRabbitMQ(data=dicdata)
            # doc lai data tu rabbit
            update.read_params_from_rabbit()
            # day data vao Mongo DB
            # Params.insert_data(dicdata)
            # Tao du lieu cho lstm
            lstmWeight.lstmWeight().create_lstm_data(dicdata)

        # Sau 60s se lan truyen DB den cac SDN khac
        global starttime, WD_SDN

        if time.time() - starttime > 45:
            # write_time = time.time() - starttime
            # viet trong so ra local SDN
            update.write_update_link_to_data_base()

            starttime = time.time()
        try:
            write_ccdn()
            write_lstm_data()
        except:
            print("GHI VAO CCDN LOI")

        return content

def write_ccdn():
    data = LinkVersion.get_multiple_data()
    # Viet vao DB cua CCDN
    url_ccdn = "http://" + ip_ccdn + ":5000/write_full_data/"
    requests.post(url_ccdn, data=json.dumps({'link_versions': data}))
    return 

def write_lstm_data():
    data = Lstm.get_multiple_data()
    # Viet vao DB cua LSTM
    url_ccdn = "http://" + ip_ccdn + ":5000/write_lstm_data/"
    requests.post(url_ccdn, data=json.dumps({'link_data': data}))
    return 

# viet trong so ra nhieu SDN khac
@app.route('/write_W_SDN/',  methods=['GET', 'POST'])
def write_W_SDN():
    if request.method == 'POST':
        W_contant = request.data
        update.write_W_SDN(int(W_contant))
        return W_contant

@app.route('/write_link_version/',  methods=['GET', 'POST'])
def write_link_version():
    if request.method == 'POST':
        # app.logger.info("Da nhan dc POST")
        content = request.data
        for data in json.loads(content)['link_versions']:
            data_search = { 'src': data['src'], 'dst': data['dst'] }
            if LinkVersion.is_data_exit(data_search=data_search):
                LinkVersion.update_many(data_search, data)
            else:
                LinkVersion.insert_data(data=data)
        # print("Ghi vao local SDN tu SDN khac thanh cong")
        # time.sleep(1)
        return content


@app.route('/read_link_version/',  methods=['GET', 'POST'])
def read_link_version():
    if request.method == 'GET':
        data = LinkVersion.get_multiple_data()
        return jsonify({'link_versions': data})  # will return the json
        # return Response(json.dumps(data),  mimetype='application/json')


if __name__ == '__main__':
    ip_local = str(json.load(open(PATH_ABSOLUTE+'/config.json'))['ip_local'])
    app.run(host=ip_local, debug=True, use_reloader=False)
