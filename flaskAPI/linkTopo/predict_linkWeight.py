
import sys, json, random
sys.path.append('/home/onos/Downloads/flask_SDN/Flask-SDN/flaskAPI/dataBaseMongo')
sys.path.append('/home/onos/Downloads/flask_SDN/Flask-SDN/flaskAPI/model')
import Predict_linkWeight
import lstm_model
class lstmWeight():
    def __init__(self):
        self.ip_local = str(json.load(open('/home/onos/Downloads/flask_SDN/Flask-SDN/config.json'))['ip_local'])
        self.ip_remote = json.load(open('/home/onos/Downloads/flask_SDN/Flask-SDN/config.json'))['ip_remote']
        self.ip_ccdn =  str(json.load(open('/home/onos/Downloads/flask_SDN/Flask-SDN/config.json'))['ip_ccdn'])
        self.thread_overhead =  float(json.load(open('/home/onos/Downloads/flask_SDN/Flask-SDN/config.json'))['thread_overhead'])
        self.lstm_model = lstm_model.lstm_model()

    # Predict label based on local model
    # Params: QoS
    # Return: 1 => good, 0 ==> bad
    predict_label = lambda self, delay, linkUtilization, packetLoss, overhead : self.lstm_model.predict(delay, linkUtilization, packetLoss, overhead)

    def create_lstm_data(self, dicdata):
        # update QoS from SINA data and insert into batabase (dataset)
        src = dicdata['src']
        dst = dicdata['dst']
        delay = dicdata['delay']
        linkUtilization = float(dicdata['linkUtilization']) if float(dicdata['linkUtilization']) == 1.0 else random.uniform(0, 0.7)
        packetLoss = float(dicdata['packetLoss']) if float(dicdata['packetLoss']) == 1.0 and float(dicdata['packetLoss']) == 0.0 else random.uniform(0.02, 0.26)
        byteSent = float(dicdata['byteSent']) 
        byteReceived = float(dicdata['byteReceived'])
        overhead = (byteSent + byteReceived) / 1000000 + 10 # convert to MB
        
        label = self.predict_label(delay, linkUtilization, packetLoss, overhead)

        temp_data = {"src": src,
                     "dst": dst,
                     "IpSDN": self.ip_local,
                     "label": label,
                     }
        try:
            data_search = {'src': temp_data['src'], 'dst': temp_data['dst']}
            print('INSERT WEIGHT')
            if Predict_linkWeight.is_data_exit(data_search=data_search):
                Predict_linkWeight.update_many(data_search, temp_data)
            else:
                Predict_linkWeight.insert_data(data=temp_data)
            # print("Ghi vao local may nay thanh cong")
        except:
            print("--------------- Write Predict_linkWeight loi")