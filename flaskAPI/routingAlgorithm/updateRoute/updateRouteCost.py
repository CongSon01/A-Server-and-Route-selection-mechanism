import sys
import random, json, requests

PATH_ABSOLUTE = "/home/onos/Downloads/A-Server-and-Route-selection-mechanism/flaskAPI/"


sys.path.append(PATH_ABSOLUTE + 'model')
sys.path.append(PATH_ABSOLUTE + 'model/databaseHandler')
sys.path.append(PATH_ABSOLUTE + 'routingAlgorithm')

# from flaskAPI.routingAlgorithm.QoS_metrics_config import *
from QoS_metrics_config import *


# sys.path.append(PATH_ABSOLUTE + 'api')

from mongoDBHandler import MongoDbHandler


class RouteCost:
    def __init__(self, topo, list_ip):
        # data base route cost
        self.db = MongoDbHandler(database="SDN_data", collection="LinkCost")
        self.min_max_db = MongoDbHandler(database="SDN_data", collection="min_max_db")
        new_route = {
            "max_delay": INIT_MAX_DELAY,
            "min_delay": INIT_MIN_DELAY,
            "max_packet_loss": INIT_MAX_PACKET_LOSS_RATE,
            "min_packet_loss": INIT_MIN_PACKET_LOSS_RATE,
            "max_link_utilization": INIT_MAX_LINK_UTILZATION,
            "min_link_utilization": INIT_MIN_LINK_UTILZATION
        }
        self.min_max_db.insert_one_data(new_route)
        # self.db.remove_all()
        self.R_links_data = []
        self.list_ip = list_ip
        self.topo = topo
        self.link_versions = []
        self.topo

    def read_R_links_data_from_other_domains(self, R):
        # link_versions = []
        self.link_versions = []
        for ip in random.sample(self.list_ip, R):
            try:
                url = "http://" + ip['ip'] + ":5000/read_link_version/"
                response = requests.get(url)
                link_object = json.loads(response.text)
                self.link_versions.extend(link_object['link_versions'])
                print("Read data from R may")
            except:
                print("DOC API R LOI")
        # return link_versions

    def pull_new_cost_to_topology(self):
        self.topo.read_update_weight()

    def update_route_cost_in_data_base(self, service_type):

        # ####### xoa het link cost cu
        # self.db.remove_all()
        # self.link_versions = []
        # print("dataaaaaaaaaaaa")
        # print(self.link_versions)
        MIN_DELAY = 0
        MAX_DELAY = 1000
        for link_data in self.link_versions:
            src = link_data["src"]
            dst = link_data["dst"]
            delay = float(link_data["delay"])
            packet_loss = float(link_data["packetLoss"])
            link_utilization = float(link_data["linkUtilization"])   

            if (delay > MAX_DELAY):
                query = {}
                new_value = {"$set": {"max_delay": delay}}
                self.min_max_db.update_one(query, new_value)
            if (delay < MIN_DELAY):
                query = {}
                new_value = {"$set": {"min_delay": delay}}
                self.min_max_db.update_one(query, new_value)
            if (packet_loss > MAX_PACKET_LOSS_RATE):
                query = {}
                new_value = {"$set": {"max_packet_loss": packet_loss}}
                self.min_max_db.update_one(query, new_value)
            if (packet_loss < MIN_PACKET_LOSS_RATE):
                query = {}
                new_value = {"$set": {"min_packet_loss": packet_loss}}
                self.min_max_db.update_one(query, new_value)
            if (link_utilization_normalized > MAX_LINK_UTILZATION):
                query = {}
                new_value = {"$set": {"max_packet_loss": link_utilization_normalized}}
                self.min_max_db.update_one(query, new_value)
            if (link_utilization_normalized < MIN_LINK_UTILZATION):
                query = {}
                new_value = {"$set": {"min_packet_loss": link_utilization_normalized}}
                self.min_max_db.update_one(query, new_value)
                


            MIN_DELAY = self.min_max_db.find({}, {"min_delay": 1})
            MAX_DELAY = self.min_max_db.find({}, {"max_delay": 1})

            MIN_PACKET_LOSS_RATE = self.min_max_db.find({}, {"min_packet_loss": 1}) 
            MAX_PACKET_LOSS_RATE = self.min_max_db.find({}, {"max_packet_loss": 1})  

            MIN_LINK_UTILZATION = self.min_max_db.find({}, {"min_link_utilization": 1})
            MAX_LINK_UTILZATION = self.min_max_db.find({}, {"max_link_utilization": 1})

            delay_normalized = self.normalize_QoS_metric(QoS_metric=delay, 
                                                         min_range= MIN_DELAY, 
                                                         max_range= MAX_DELAY)
            
            packet_loss_normalized = self.normalize_QoS_metric(QoS_metric=packet_loss, 
                                                         min_range= MIN_PACKET_LOSS_RATE, 
                                                         max_range= MAX_PACKET_LOSS_RATE)
            
            link_utilization_normalized = self.normalize_QoS_metric(QoS_metric=link_utilization, 
                                                         min_range= MIN_LINK_UTILZATION, 
                                                         max_range= MAX_LINK_UTILZATION)
            
            ### tinh toan link cost 
            link_cost = self.calculate_link_cost_serivce(delay_normalized, packet_loss_normalized, 
                                                         link_utilization_normalized, service_type)
           
            # Define the filter to find the document with the matching "src" and "dst" values
            filter_route = {"src": src, "dst": dst}
            result_route = self.db.find_data(filter_route)

            # neu link khong ton tai trong DB thi chen link vao DB
            if result_route == False:       
                new_route = {
                        "src": src,
                        "dst": dst,
                        "link_cost": link_cost,
                        "service_type": service_type      
                    }
                self.db.insert_one_data(new_route)

               
            else: # neu tim thay link thi cap nhap lai cost moi vao DB  
                update = {
                        "$set": {"link_cost": link_cost, "service_type": service_type}}
                self.db.update_data(filter_route, update)

                # culmulative_link_cost = result_route['link_cost']
                # # cap nhap trong so link theo thoi gian
                # updated_link_cost = self.update_link_cost_through_time(
                #                                             current_link_cost= link_cost,
                #                                             culmulative_link_cost= culmulative_link_cost,
                #                                             )
                
                # # cap nhap new link cost vao vao DB
                # update = {
                #         "$set": {"link_cost": updated_link_cost, "link_version": new_link_version}}
                # self.db.update_data(filter_route, update)

    def calculate_link_cost_serivce(self, link_delay, link_loss, link_utilization, service_type):
        """
        formula of calculating link cost value based on service type
        ALPHA * PACKET LOSS + BETA * DELAY + GAMMA * LINK UTILIZATION
        """
        if  service_type == 0:
            return (ALPHA_FILE_TRANSFER * link_loss + 0.5 - ALPHA_FILE_TRANSFER) + (BETA_FILE_TRANSFER * link_delay + 0.5 - BETA_FILE_TRANSFER) + GAMMA_FILE_TRANSFER * link_utilization
        elif service_type == 1:
            return ALPHA_GOOGLE_MUSIC * link_loss + BETA_GOOGLE_MUSIC * link_delay + GAMMA_GOOGLE_MUSIC * link_utilization
        elif service_type == 2:
            return (ALPHA_GOOGLEHANGOUT_VOIP * link_loss - 0.5 - ALPHA_GOOGLEHANGOUT_VOIP) + (BETA_GOOGLEHANGOUT_VOIP * link_delay + 0.5 - BETA_GOOGLEHANGOUT_VOIP) + GAMMA_GOOGLEHANGOUT_VOIP * link_utilization
        elif service_type == 3:
            return (ALPHA_YOUTUBE * link_loss + 0.5 - ALPHA_YOUTUBE) + (BETA_YOUTUBE * link_delay + 0.5 - BETA_YOUTUBE) + GAMMA_YOUTUBE * link_utilization
        elif service_type == 5: # chay mac dinh youtube ko can update cost theo youtube
            return 0.35 * link_loss + 0.35 * link_delay + 0.3 * link_utilization
        
    def normalize_QoS_metric(self, QoS_metric, min_range, max_range):
        ###### cong them 1 luong 10^-7 de tranh mau so bang 0 
        if QoS_metric <= min_range: # chuan hoa de tranh gia tri am
            return 0
        else:
            return (QoS_metric - min_range) / (max_range - min_range + pow(10, -7))
        
    