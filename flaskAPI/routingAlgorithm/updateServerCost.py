import sys
sys.path.append('/home/onos/Downloads/flaskSDN/flaskAPI/model')
import ServerCost

class updateServerCost(object):

    def __init__(self, servers):
        self.servers = servers

    def update_server_cost(self):  
        current_server = []
        server_cost = ServerCost.get_multiple_data()
        ServerCost.remove_all()
  
        for server in server_cost:
            band_width = server['Bandwidth']
            server_ip = server['Servername']
          
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


      
            


       
       
   

