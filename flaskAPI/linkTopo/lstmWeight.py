import sys, json, random
sys.path.append('/home/onos/Downloads/flask_SDN/Flask-SDN/flaskAPI/dataBaseMongo')
import Lstm
class lstmWeight():
    def __init__(self):
        self.ip_local = str(json.load(open('/home/onos/Downloads/flask_SDN/Flask-SDN/config.json'))['ip_local'])
        self.ip_remote = json.load(open('/home/onos/Downloads/flask_SDN/Flask-SDN/config.json'))['ip_remote']
        self.ip_ccdn =  str(json.load(open('/home/onos/Downloads/flask_SDN/Flask-SDN/config.json'))['ip_ccdn'])
    def convert_delay(self, delay, delay_min, delay_max):
        return 1 if delay_min < delay < delay_max  else 0
    
    def convert_linkUtilization(self, linkUtilization, linkUtilization_min, linkUtilization_max):
        return 1 if linkUtilization_min < linkUtilization < linkUtilization_max  else 0

    def convert_packetLoss(self, packetLoss, packetLoss_min, packetLoss_max):
        return 1 if packetLoss_min < packetLoss < packetLoss_max  else 0

    def convert_linkVersion(self, linkVersion, linkVersion_min, linkVersion_max):
        return 1 if linkVersion_min < linkVersion < linkVersion_max  else 0
    
    def convert_overhead(self, overhead, overhead_min, overhead_max):
        return 1 if overhead_min < overhead < overhead_max  else 0


    def get_label(self, delay, linkUtilization, packetLoss, overhead):
        p_delay = self.convert_delay(delay=delay, delay_min=10, delay_max=200)
        p_linkUtilization = self.convert_linkUtilization(linkUtilization=linkUtilization, linkUtilization_min=0.2, linkUtilization_max=0.6)
        p_packetLoss = self.convert_packetLoss(packetLoss=packetLoss, packetLoss_min=0.0, packetLoss_max=0.22)
        # p_linkVersion = self.convert_linkVersion(linkVersion=linkVersion, linkVersion_min=0, linkVersion_max=1)
        p_overhead = self.convert_overhead(overhead=overhead, overhead_min=20000000, overhead_max=70000000)
        kq = p_delay + p_linkUtilization + p_packetLoss  + p_overhead
        return 1 if kq >= 3 else 0

    def create_lstm_data(self, dicdata):
        src = dicdata['src']
        dst = dicdata['dst']
        delay = dicdata['delay']
        linkUtilization = float(dicdata['linkUtilization']) if float(dicdata['linkUtilization']) == 1.0 else random.uniform(0, 0.7)
        packetLoss = float(dicdata['packetLoss']) + random.uniform(0.02, 0.26)
        byteSent = float(dicdata['byteSent']) / 10
        byteReceived = float(dicdata['byteReceived']) / 10
        overhead = (byteSent + byteReceived) / 2
        label = self.get_label(delay, linkUtilization, packetLoss, overhead)

        temp_data = {"src": src,
                     "dst": dst,
                     "delay": float(delay),
                     "linkUtilization": float(linkUtilization),
                     "packetLoss": float(packetLoss),
                     "IpSDN": self.ip_local,
                     "overhead": float(overhead),
                     "byteSent": float(byteSent),
                     "byteReceived": float(byteReceived),
                     "label": label,
                     }
        try:
            data_search = {'overhead': temp_data['overhead']}
            print('INSERT LSTM')
            if Lstm.is_data_exit(data_search=data_search):
                Lstm.update_many(data_search, temp_data)
            else:
                Lstm.insert_data(data=temp_data)
            # print("Ghi vao local may nay thanh cong")
        except:
            print("--------------- Write LSTM loi")


    