import sys

PATH_ABSOLUTE = "/home/onos/"

sys.path.append(PATH_ABSOLUTE + 'dataBaseMongo')
# sys.path.append(PATH_ABSOLUTE + 'api')

from mongoDBHandler import MongoDbHandler


class RouteCost:
    def __init__(self):
        # data base route cost
        self.db = MongoDbHandler(database="SDN_data", collection="LinkVersion")
        # self.db.remove_all()

    def update_route_cost(self, link_data):
        
        src = link_data["src"]
        dst = link_data["dst"]
        delay = float(link_data["delay"])
        packet_loss = float(link_data["packetLossRate"])
        link_utilization = float(link_data["linkUtilization"])
        ### tinh toan link cost 
        link_cost = self.calculate_link_cost(delay, packet_loss, link_utilization)

        # Define the filter to find the document with the matching "src" and "dst" values
        filter_route = {"src": src, "dst": dst}
        result_route = self.db.find_data(filter_route)

        # neu link khong ton tai trong DB thi chen link vao DB
        if result_route == False:       
            new_route = {
                    "src": src,
                    "dst": dst,
                    "link_cost": link_cost,
                    "link_version": 1
                }
            self.db.insert_one_data(new_route)
            # neu tim thay link trong DB thi update link cost 
        else:
            culmulative_link_cost = result_route['link_cost']
            new_link_version = result_route['link_version'] + 1
            # cap nhap trong so link theo thoi gian
            updated_link_cost = self.update_link_cost_through_time(
                                                        current_link_cost= link_cost,
                                                        culmulative_link_cost= culmulative_link_cost,
                                                        time_step= new_link_version)
              
            # cap nhap new link cost vao vao DB
            update = {
                    "$set": {"link_cost": updated_link_cost, "link_version": new_link_version}}
            self.db.update_data(filter_route, update)

    def calculate_link_cost(self, link_delay, link_loss, link_utilization):
        """
        formula of calculating link cost value
        """
        return 0.4 * link_delay + 0.3 * link_loss + 0.3 * link_utilization
    
    def update_link_cost_through_time(self, current_link_cost, 
                                      culmulative_link_cost, time_step):
        """
        after t time steps, link cost is calculated as average from 0, ... to t times
        """
        return (current_link_cost + culmulative_link_cost) / time_step


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
    