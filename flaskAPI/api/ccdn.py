import sys
import time
sys.path.append('/home/onos/Downloads/flaskSDN/flaskAPI/model')
sys.path.append('/home/onos/Downloads/flaskSDN/flaskAPI/routingAlgorithm')
sys.path.append('/home/onos/Downloads/flaskSDN/flaskAPI/q_learning')
import json
from numpy import average
import requests
import random
import CCDN_update
import CCDN, Version
import updateLinkTopo
import LinkVersion
import q_table
import numpy as np


class Update_weight_ccdn(object):

    def __init__(self, topo, update_server, list_ip):
        self.LinkVersions = ""
        self.R = 2
        self.W = 2
        self.count = 0
        self.topo = topo
        self.update_server = update_server
        self.list_ip = list_ip
        self.q_table = q_table.Q_table()
        self.time_run = 60*10 # 10ph
        self.start_run = time.time()

    def write_log_parameter(self,R, W,  read_delay, write_delay, time_staleness, version_staleness):
        self.count += 1
        data_insert = {'R':R, 'W':W,  'read_delay':read_delay, 
                'write_delay':write_delay, 'time_staleness':time_staleness, 'version_staleness':version_staleness}

        if ( time.time() - self.time_run == self.time_run ):
            print("STOP WRITE Q Table")
            np.save('qtable.npy',np.array(self.q_table.qtable))
        else:
            self.q_table.get_q_table(read_delay, write_delay, version_staleness, self.count)
        print("-----Q Table-----")

        CCDN.insert_data(data_insert)

    def calculate_version_staleness(self, link_versions):
        """
        link_versions: la list data cua cac canh
        """
        # dict_version = defaultdict(list)

        # for l_version in link_versions:
        #     key_version = {'src':l_version['src'], 'dst':l_version['dst']}
        #     dict_version[str(key_version)].append(l_version['version'])

        # averages = {i_version: sum(version) / len(version) for i_version, version in dict_version.items()}
        if len(link_versions) != 0:
            versions = [version['linkVersion'] for version in link_versions]
            return (int(average(versions)), int(max(versions)))
        else:
            return (0, 0)



    def read_R_SDN(self):
            print("call lan thu", self.count)
            link_versions = []
            list_WD = []
        # try:
            time_start_read = time.time()
            for ip in random.sample(self.list_ip, self.R):
                try:
                    url = "http://" + ip + ":5000/read_link_version/"
                    response = requests.get(url)
                    link_object = json.loads(response.text)
                    link_versions.extend(link_object[0]['link_versions'])
                    list_WD.append(link_object[1]['WD_SDN'])
                except:
                    print("GOI API LOI")


            # Response time: thoi gian khi gui yeu cau -> tra ve ket qua doc R SDN
            response_time = (time.time() - time_start_read) * 1000 # ms
            read_delay = response_time
            # tam thoi
            write_delay = average(list_WD) * 1000 #ms
            time_start_read = time.time()

            # version_staleness: Do ben cua tung version canh
            # version_staleness = Trung binh version cua moi canh
            version_staleness, max_version = self.calculate_version_staleness(link_versions)

            # Luu khi co version max
            if Version.get_version_max() != None:
                # time_staleness: tuoi tho cua data
                # time_staleness = time request doc xong R SDN - time version moi nhat dc ghi vao W SDN
                time_staleness = response_time - int(Version.get_version_max()['time'])
                print("MAX: ", Version.get_version_max()['version'])
                if Version.get_version_max()['version'] < max_version:
                    print('VERSION MOI: ' , str(max_version))
                    Version.insert_data({'version':max_version, 'time':time.time()})
            else:
                Version.insert_data({'version':max_version, 'time':time.time()})
                time_staleness = response_time - 0

            if ( version_staleness, max_version != 0, 0 ):
                self.write_log_parameter(self.R, self.W, int(read_delay), int(write_delay), time_staleness, version_staleness)
                # chen vao bang CCDN de luu vet ve sau
                LinkVersion.insert_n_data(link_versions)
            
            

            # update canh co version max
            # for data in link_object['link_versions']:
            #     data_search = {'src': data['src'], 'dst': data['dst']}
            #     data_update = {'linkVersion': data['linkVersion']}
            #     if CCDN_update.is_data_exits(data_search):
            #         CCDN_update.update_data(data_search, data_update)
            #     else:
            #         CCDN_update.insert_data(data)

            # print("Do dai data read = ", len(link_versions))
        # except:
        #     print("Flask Doc nhieu SDN loi")

        # tinh toan trong so theo thuat toan
            self.calculate_link_weight(link_versions)

    def calculate_link_weight(self, link_versions):

        link_weight = updateLinkTopo.updateLinkTopo(link_verions=link_versions)
        new_link_topo = link_weight.get_link_weight()

        # viet trong so da cap nhap vao mang Topo
        self.write_update_link_to_topo(new_link_topo)

    def write_update_link_to_topo(self, new_link_topo):
        self.topo.read_update_weight(new_link_topo)
