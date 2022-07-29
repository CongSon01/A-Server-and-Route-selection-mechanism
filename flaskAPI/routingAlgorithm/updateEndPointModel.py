import sys
sys.path.append('/home/onos/Downloads/A-Server-and-Route-selection-mechanism/flaskAPI/model')

import EndPointModel

class updateEndPointModel(object):

    def __init__(self, servers):
        self.servers = servers

    def update_server_cost(self):  
        current_server = []
        server_cost = EndPointModel.get_multiple_data()
        EndPointModel.remove_all()
  
        for server in server_cost:
            band_width = server['serverCost']
            server_ip = server['hostIP']
          
            server_object = self.find_server(server_ip)

            if server_object is not None:
                server_object.add_cost(band_width)
                if server_object not in current_server:
                    current_server.append(server_object)
               
        for server in current_server:
            server.calculate_final_cost()      

    def find_server(self, server_ip):
        for ip in self.servers:     
            if str(ip) == str(server_ip):         
                return self.servers[ip]
        return None


      
            


       
       
   

