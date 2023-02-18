import sys
import random, json, requests

PATH_ABSOLUTE = "/home/onos/Downloads/A-Server-and-Route-selection-mechanism/flaskAPI/"


sys.path.append(PATH_ABSOLUTE + 'model')
sys.path.append(PATH_ABSOLUTE + 'model/databaseHandler')

# sys.path.append(PATH_ABSOLUTE + 'api')

from mongoDBHandler import MongoDbHandler


class RouteCost:
    def __init__(self, topo, list_ip):
        # data base route cost
        self.db = MongoDbHandler(database="SDN_data", collection="LinkCost")
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
        for link_data in self.link_versions:
            src = link_data["src"]
            dst = link_data["dst"]
            delay = float(link_data["delay"])
            packet_loss = float(link_data["packetLoss"])
            link_utilization = float(link_data["linkUtilization"])   

            ### tinh toan link cost 
            link_cost = self.calculate_link_cost_serivce(delay, packet_loss, link_utilization, service_type)
           
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
        """
        if  service_type == 1:
            return 0.4 * link_delay + 0.3 * link_loss + 0.3 * link_utilization
        elif service_type ==2:
            return 0.1 * link_delay + 0.7 * link_loss + 0.2 * link_utilization
        elif service_type ==3:
            return 0.2 * link_delay + 0.5 * link_loss + 0.3 * link_utilization
        elif service_type ==4:
            return 0.6 * link_delay + 0.2 * link_loss + 0.2 * link_utilization

    # def update_link_cost_through_time(self, current_link_cost, 
    #                                   culmulative_link_cost):
        
    #     return (current_link_cost + culmulative_link_cost) / 2


        #  temp_data = {"src": src,
        #                  "dst": dst,
        #                  "delay": float(delay),
        #                  "linkUtilization": float(link_utilization),
        #                  "packetLoss": float(packet_loss),
        #                  "linkVersion": self.link_version,
        #                  "IpSDN": self.ip_local,
        #                  "overhead": float(overhead),
        #                  "byteSent": float(byte_sent),
        #                  "byt
    