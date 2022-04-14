import sys
sys.path.append('/home/onos/Downloads/flask_SDN/Flask-SDN/flaskAPI/dataBaseMongo')
sys.path.append('/home/onos/Downloads/flask_SDN/Flask-SDN/flaskAPI/api')

import json
import requests
import random
import LinkVersion
import sub
import linkWeight

class updateWeight(object):

    def __init__(self):
        self.params_data = ""
        self.link_set = list()
        self.consumer = sub.Sub()
        self.link_version = 0

        # So lan write ra nhieu SDN
        self.num_W = 2
        self.ip_local = str(json.load(open('/home/onos/Downloads/flask_SDN/Flask-SDN/config.json'))['ip_local'])
        self.ip_remote = json.load(open('/home/onos/Downloads/flask_SDN/Flask-SDN/config.json'))['ip_remote']
        self.ip_ccdn =  str(json.load(open('/home/onos/Downloads/flask_SDN/Flask-SDN/config.json'))['ip_ccdn'])
        self.count = 0
        # self.ip_sdn = ['10.20.0.251']

    def get_link_set(self):
        return self.link_set

    def get_count(self):
        return self.count

    def set_count(self, count):
        self.count = count

    def reset_link_set(self):
        self.link_set = list()

    def read_params_from_rabbit(self):
        # pop data from RAbbit Queue
        self.consumer.receive_queue()
        self.params_data = self.consumer.peek_stack()

        self.update_link()

    def update_link(self):
        id_src = str(self.params_data['src'])
        id_dst = str(self.params_data['dst'])
        link = self.has_link(target_src=id_src, target_dst=id_dst)

        # Neu link chua co trong tap canh thi khoi tao link
        if link == None:
            link_object = linkWeight.linkWeight(id_src=id_src, id_dst=id_dst)
            self.link_set.append(link_object)
            link_object.update_weight(params_data=self.params_data)
        # neu link da co trong tap canh thi cap nhat lai weight
        else:
            link.update_weight(params_data=self.params_data)

    def has_link(self, target_src, target_dst):
        found = None
        for link in self.link_set:
            if link.get_id_src() == target_src and link.get_id_dst() == target_dst:
                found = True
                return link
        return None

    def write_update_link_to_data_base(self, write_time):
        try:
            LinkVersion.remove_all()
        except:
            print("Remove loi .................")

        self.link_version += 1
        self.count +=1
        for link in self.link_set:
            src = link.get_id_src()
            dst = link.get_id_dst()
            print("chay lan thu", self.count)
            weight = link.find_link_cost()

            delay = weight[0]
            link_utilization = weight[1]
            packet_loss = weight[2]

            temp_data = {"src": src,
                         "dst": dst,
                         "delay": float(delay),
                         "linkUtilization": float(link_utilization),
                         "packetLoss": float(packet_loss),
                         "linkVersion": self.link_version,
                         "IpSDN": self.ip_local,
                         "writeTime": write_time}
            try:
                LinkVersion.insert_data(temp_data)
            except:
                print("--------------- Write Local Link version loi")
            self.reset_link_set()

    def write_W_SDN(self):
        try:
            data = LinkVersion.get_multiple_data()

            # Viet vao DB cua CCDN
            url_ccdn = "http://" + self.ip_ccdn + ":5000/write_full_data/"
            requests.post(url_ccdn, data=json.dumps({'link_versions': data}))

            for ip in random.sample(self.ip_remote, self.num_W):
                print('ghi vao ip: ', ip)
                url = "http://" + ip + ":5000/write_link_version/"
                requests.post(url, data=json.dumps({'link_versions': data}))
                # print("Thanh cong")
        except:
            print("flask Goi nhieu SDN loiiiiiiiiiiiiiiiiiiiii")

  
        # data = LinkVersion.get_multiple_data()
        # ip = "10.20.0.251"
        # print('ghi vao ip: ', ip)
        # url = "http://" + ip + ":5000/write_link_version/"
        # requests.post(url, data=json.dumps({'link_versions': data}))
       
