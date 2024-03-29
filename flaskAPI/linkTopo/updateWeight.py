import sys

PATH_ABSOLUTE = "/home/onos/Downloads/A-Server-and-Route-selection-mechanism/"

sys.path.append(PATH_ABSOLUTE + 'dataBaseMongo')
sys.path.append(PATH_ABSOLUTE + 'api')

from mongoDBHandler import MongoDbHandler

import json, time
import requests
import random
import LinkVersion
import sub
import linkWeight

sys.path.append(PATH_ABSOLUTE + 'utils')
from get_local_ip import get_local_ip
suffix = get_local_ip("ens33").split(".")[-1]

class updateWeight(object):

    def __init__(self):
        self.params_data = ""
        self.link_set = list()
        self.consumer = sub.Sub()
        self.link_version = 0

        # So lan write ra nhieu SDN
        self.ip_local = str(json.load(open(PATH_ABSOLUTE + 'config/config-' + suffix + '.json'))['ip_local'])
        self.ip_remote = json.load(open(PATH_ABSOLUTE + 'config/config-' + suffix + '.json'))['ip_remote']
        self.ip_ccdn =  str(json.load(open(PATH_ABSOLUTE + 'config/config-' + suffix + '.json'))['ip_ccdn'])
        self.thread_overhead =  float(json.load(open(PATH_ABSOLUTE + 'config/config-' + suffix + '.json'))['thread_overhead'])
        self.count = 0
        # self.ip_sdn = ['10.20.0.251']

        self.db = MongoDbHandler(database="SDN_data", collection="LinkVersion")

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

    def write_update_link_to_data_base(self, link_data):
        # try:
        #     LinkVersion.remove_all()
        # except:
        #     print("Remove loi .................")

        # self.link_version += 1
        # self.count +=1
        src = link_data["src"]
        dst = link_data["dst"]
        delay = float(link_data["delay"])
        packet_loss = float(link_data["packetLossRate"])
        link_utilization = float(link_data["linkUtilization"])
        byte_sent = float(link_data["byteSent"])
        byte_received = float(link_data["byteReceived"])
        overhead = abs((byte_sent + byte_received)) / 1000000 + 10 # convert to MB
        
        try:
            data_search = { 'src': src, 'dst': dst }
            result_link = LinkVersion.find_data(query= data_search)
            
            # neu link ko co trong DB thi chen vao DB
            if result_link == False:  
                        # neu da chua ton tai thi chen vao
                        temp_data = {"src": src,
                                "dst": dst,
                                "delay": delay,
                                "linkUtilization": link_utilization,
                                "packetLoss": packet_loss,
                                "linkVersion": 1,
                                "IpSDN": self.ip_local,
                                "overhead": float(overhead),
                                "byteSent": byte_sent,
                                "byteReceived": byte_received
                                }
                        self.db.insert_one_data(temp_data) 
            else: 
                        # neu link da ton tai trong Db thi update version va QoS params 
                        current_link_version = result_link['linkVersion']
                        # cap nhap new Qos parameters cua link vao vao DB
                        update = {
                            "$set": {"delay": delay, 
                                    "linkUtilization": link_utilization,
                                    "packetLoss": packet_loss,
                                    "linkVersion": current_link_version+1,
                                    "IpSDN": self.ip_local,
                                    "overhead": float(overhead),
                                    "byteSent": byte_sent,
                                    "byteReceived": byte_received         
                                    }}   
                        self.db.update_data(data_search, update)                                  
        except:
            print("--------------- Write Local Link version loi")
        

    def write_W_SDN(self, num_W):
        try:
            data = LinkVersion.get_multiple_data()
            for ip in random.sample(self.ip_remote, num_W):
                # print('ghi vao ip: ', ip)
                url = "http://" + ip + ":5000/write_link_version/"
                requests.post(url, data=json.dumps({'link_versions': data}))
                # print("Thanh cong")
        except:
            print("flask Goi nhieu SDN loiiiiiiiiiiiiiiiiiiiii")
