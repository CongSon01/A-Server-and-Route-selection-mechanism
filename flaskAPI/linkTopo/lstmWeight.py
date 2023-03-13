
import sys, json, random
PATH_ABSOLUTE = "/usr/local/"

sys.path.append(PATH_ABSOLUTE + 'dataBaseMongo')
import Lstm

sys.path.append(PATH_ABSOLUTE + 'utils')
from get_local_ip import get_local_ip
suffix = get_local_ip("eth0").split(".")[-1]
class lstmWeight():
    def __init__(self):
        self.ip_local = str(json.load(open(PATH_ABSOLUTE +'config/config-' + suffix + '.json'))['ip_local'])
        self.ip_remote = json.load(open(PATH_ABSOLUTE +'config/config-' + suffix + '.json'))['ip_remote']
        self.ip_ccdn =  str(json.load(open(PATH_ABSOLUTE +'config/config-' + suffix + '.json'))['ip_ccdn'])
        self.thread_overhead =  float(json.load(open(PATH_ABSOLUTE +'config/config-' + suffix + '.json'))['thread_overhead'])

    convert_delay = lambda self, delay, delay_min, delay_max: 1 if delay_min < delay < delay_max  else 0
    
    convert_linkUtilization = lambda self, linkUtilization, linkUtilization_min, linkUtilization_max: 1 if linkUtilization_min < linkUtilization < linkUtilization_max  else 0

    convert_packetLoss = lambda self, packetLoss, packetLoss_min, packetLoss_max: 1 if packetLoss_min < packetLoss < packetLoss_max  else 0

    convert_linkVersion = lambda self, linkVersion, linkVersion_min, linkVersion_max: 1 if linkVersion_min < linkVersion < linkVersion_max  else 0
    
    convert_overhead = lambda self, overhead, overhead_max: 1 if overhead < overhead_max  else 0


    def get_label(self, delay, linkUtilization, packetLoss, overhead):
        # Get label based on conditions
        # Params: QoS
        # Return: 1 => good, 0 ==> bad

        p_delay = self.convert_delay(delay=delay, delay_min=10, delay_max=500)
        p_linkUtilization = self.convert_linkUtilization(linkUtilization=linkUtilization, linkUtilization_min=0.2, linkUtilization_max=0.6)
        # p_packetLoss = self.convert_packetLoss(packetLoss=packetLoss, packetLoss_min=0.0, packetLoss_max=0.22)

        # p_linkVersion = self.convert_linkVersion(linkVersion=linkVersion, linkVersion_min=0, linkVersion_max=1)
        p_overhead = self.convert_overhead(overhead=overhead, overhead_max=40)
        kq = p_delay + p_linkUtilization + packetLoss  + p_overhead
        return 1 if kq >= 3 else 0

    def create_lstm_data(self, dicdata):
        # update QoS from SINA data and insert into batabase (dataset)
        src = dicdata['src']
        dst = dicdata['dst']
        delay = dicdata['delay']
        linkUtilization = float(dicdata['linkUtilization']) if float(dicdata['linkUtilization']) == 1.0 else random.uniform(0, 0.7)
        packetLoss = float(dicdata['packetLoss']) 
        byteSent = float(dicdata['byteSent']) 
        byteReceived = float(dicdata['byteReceived'])
        overhead = (byteSent + byteReceived) / 1000000 + 10 # convert to MB
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


    