
import sys, json, random

PATH_ABSOLUTE = "/usr/local/Downloads/A-Server-and-Route-selection-mechanism/"

sys.path.append(PATH_ABSOLUTE + 'flaskAPI/dataBaseMongo')
sys.path.append(PATH_ABSOLUTE + 'flaskAPI/model')
import LearnWeightModel
import lstm_model
import requests

sys.path.append(PATH_ABSOLUTE + 'utils')
from get_local_ip import get_local_ip
suffix = get_local_ip("ens33").split(".")[-1]
class learnWeight():
    def __init__(self):
        self.ip_local = str(json.load(open(PATH_ABSOLUTE +'config/config-' + suffix + '.json'))['ip_local'])
        self.ip_remote = json.load(open(PATH_ABSOLUTE +'config/config-' + suffix + '.json'))['ip_remote']
        self.ip_ccdn =  str(json.load(open(PATH_ABSOLUTE +'config/config-' + suffix + '.json'))['ip_ccdn'])
        self.thread_overhead =  float(json.load(open(PATH_ABSOLUTE +'config/config-' + suffix + '.json'))['thread_overhead'])
        self.lstm_model = lstm_model.lstm_model()

    # Predict label based on local model
    # Params: QoS
    # Return: 1 => good, 0 ==> bad
    predict_label = lambda self, data : self.lstm_model.predict(data)

    def get_learn_weight(self, dicdata):
        # update QoS from SINA data and insert into batabase (dataset)
        src = dicdata['src']
        dst = dicdata['dst']
        delay = dicdata['delay']
        linkUtilization = float(dicdata['linkUtilization']) if float(dicdata['linkUtilization']) == 1.0 else random.uniform(0, 0.7)
        packetLoss = float(dicdata['packetLoss']) if float(dicdata['packetLoss']) == 1.0 and float(dicdata['packetLoss']) == 0.0 else random.uniform(0.02, 0.26)
        byteSent = float(dicdata['byteSent']) 
        byteReceived = float(dicdata['byteReceived'])
        overhead = (byteSent + byteReceived) / 1000000 + 10 # convert to MB
        tmp_data = [delay, linkUtilization, overhead, packetLoss]
        label = self.predict_label(tmp_data)

        temp_data = {"src": src,
                     "dst": dst,
                     "IpSDN": self.ip_local,
                     "label": label,
                     }
        try:
            data_search = {'src': temp_data['src'], 'dst': temp_data['dst']}
            if LearnWeightModel.is_data_exit(data_search=data_search):
                LearnWeightModel.update_many(data_search, temp_data)
                print('UPDATE WEIGHT')
            else:
                LearnWeightModel.insert_data(data=temp_data)
                print('INSERT WEIGHT')
                # print("Ghi vao local may nay thanh cong")
        except:
            print("--------------- Write Predict_linkWeight loi")
    
    def write_W_SDN(self, num_W):
        try:
            data = LearnWeightModel.get_multiple_data()
            for ip in random.sample(self.ip_remote, num_W):
                # print('ghi vao ip: ', ip)
                url = "http://" + ip + ":5000/write_learn_weights/"
                requests.post(url, data=json.dumps({'learn_weights': data}))
                # print("Thanh cong")
        except:
            print("flask Goi nhieu SDN loiiiiiiiiiiiiiiiiiiiii")