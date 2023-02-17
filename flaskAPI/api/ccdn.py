import sys
import time

# from importlib_metadata import version
sys.path.append('/home/onos/Downloads/A-Server-and-Route-selection-mechanism/flaskAPI/model')
sys.path.append('/home/onos/Downloads/A-Server-and-Route-selection-mechanism/flaskAPI/routingAlgorithm')
sys.path.append('/home/onos/Downloads/A-Server-and-Route-selection-mechanism/flaskAPI/q_learning')
import json
from numpy import NaN, average
import requests
import random
# import CCDN_update
import CCDN, Version
import updateLinkTopo
import q_table
import numpy as np


class Update_weight_ccdn(object):

    def __init__(self, topo, update_server, list_ip):
        self.LinkVersions = ""
        self.count = 0
        self.topo = topo
        self.update_server = update_server
        self.list_ip = list_ip
        self.q_table = q_table.Q_table()
        self.time_run = 60*60*5 # 60ph
        self.start_run = time.time()

    def write_log_parameter(self,R, W,  read_delay, write_delay, time_staleness, version_staleness, avg_overhead):
        self.count += 1
        time_current = int(time.time() - self.start_run)
        print("GHI tai gay thu : ", time_current)
        data_insert = {'R':18, 'W':1,  'read_delay':read_delay, 
                'write_delay':write_delay, 'time_staleness':time_staleness, 'version_staleness':version_staleness, 'time': time_current
                ,'overhead': avg_overhead}

        if ( time_current > self.time_run ):
            print("STOP WRITE Q Table")
            np.save('qtable.npy',np.array(self.q_table.qtable))
        else:
            self.q_table.get_q_table(read_delay, write_delay, version_staleness, self.count)

        if ( avg_overhead != NaN ):
            CCDN.insert_data(data_insert)

    def calculate_version_staleness(self, link_versions, version_mongo_max):
        """
        link_versions: la list data cua cac canh
        """
        if len(link_versions) != 0:
            versions = [version['linkVersion'] for version in link_versions]
            if version_mongo_max != None :
                versions_st = abs(version_mongo_max['version'] - np.array(versions))
            else:
                versions_st = versions
            return (int(np.mean(versions_st)), int(max(versions)))
        else:
            return (0,0)
        
    def calculate_avg_overhead(self, link_versions):
        overheads = [version['overhead'] for version in link_versions]
        # print('AVG', average(overheads))
        # neu overheads ma rong 
        if not overheads:
            return 0
        else: 
            return np.mean(overheads)
        # print('MEAN',np.mean(overheads))
        # return np.mean(overheads)

    def read_R_SDN(self, R):
        link_versions = []
        for ip in random.sample(self.list_ip, R):
            try:
                url = "http://" + ip['ip'] + ":5000/read_link_version/"
                response = requests.get(url)
                link_object = json.loads(response.text)
                link_versions.extend(link_object['link_versions'])
            except:
                print("GOI API R LOI")
        return link_versions
    
    def write_W_SDN(self, W):
        list_time_write = []
        for ip in self.list_ip:
            time_start_write = time.time()
            try:
                url = "http://" + ip['ip'] + ":5000/write_W_SDN/"
                repo = requests.post(url, data=str(W))
            except:
                print("GOI API W LOI")
            list_time_write.append( time.time() - time_start_write )
            time_start_write = time.time()
        return int(average(list_time_write) * 1000)
        

    def load_CCDN(self, R, W):
            print("call lan thu", self.count)
            
            write_delay = self.write_W_SDN(W)

            time_start_read = time.time()
            link_versions = self.read_R_SDN(R)
            # Response time: thoi gian khi gui yeu cau -> tra ve ket qua doc R SDN
            response_time = (time.time() - time_start_read) * 1000 # ms
            read_delay = abs(response_time)
            time_start_read = time.time()

            # version max in mongo
            version_mongo_max = Version.get_version_max()
            print("versionnnnnnnnnn", version_mongo_max)
            # version_staleness: Do ben cua tung version canh
            # version_staleness = Trung binh version cua moi canh
            version_staleness, max_version = self.calculate_version_staleness(link_versions, version_mongo_max)
            avg_overhead = self.calculate_avg_overhead(link_versions)

            # Luu khi co version max
            if version_mongo_max != None:
                # time_staleness: tuoi tho cua data
                # time_staleness = time request doc xong R SDN - time version moi nhat dc ghi vao W SDN
                time_staleness = abs(response_time - int(version_mongo_max['time']))
                print("MAX: ", version_mongo_max['version'])
                if version_mongo_max['version'] < max_version:
                    print('VERSION MOI: ' , str(max_version))
                    Version.insert_data({'version':max_version, 'time':int(time.time() - self.start_run)})
            else:
                Version.insert_data({'version':max_version, 'time':int(time.time() - self.start_run)})
                time_staleness = response_time - 0

            if ( version_staleness, max_version != 0, 0 ):
                self.write_log_parameter(R, W, int(read_delay), int(write_delay), time_staleness, version_staleness, avg_overhead)
            
            

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
        # link versions la tap cac data doc duoc tu may phu
            self.calculate_link_weight(link_versions)
            return (read_delay, write_delay, version_staleness)

    def calculate_link_weight(self, link_versions):
        print('Tinh trong so')
        link_weight = updateLinkTopo.updateLinkTopo(link_verions= link_versions)
        link_weight.get_link_weight()
        self.topo.read_update_weight()
      