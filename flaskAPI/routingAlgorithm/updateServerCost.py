import numpy as np
import sub
import sys
sys.path.append('/home/onos/Downloads/flask_SDN/Flask-SDN/flaskAPI/model')
import ServerCost

class updateServerCost(object):

    def __init__(self, servers):
        self.servers = servers

    def update_server_cost(self):
        #print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA server cost")
        current_server = []
        server_cost = ServerCost.get_multiple_data()
        ServerCost.remove_all()
        #print(server_cost)
        for server in server_cost:
            band_width = server['Bandwidth']
            server_ip = server['Servername']
            #print("bandwith", band_width)
            #print("server", server_ip)

            server_object = self.find_server(server_ip)

            if server_object is not None:
                server_object.add_cost(band_width)
                if server_object not in current_server:
                    current_server.append(server_object)
                # print( "server cost = ", server_object.get_server_cost() )
                #updated_ServerCost.insert_data(server_object)
            #     continue
            # else:
            #     server_object.add_cost(band_width)
            #     print( "Servercost= ",server_object.get_server_cost() )
        #print("-------------------------------------------", len(current_server))
        for server in current_server:
            server.calculate_final_cost()
            #print("server cost====================", server.get_server_cost())

    def find_server(self, server_ip):
        for ip in self.servers:
            # print("ip===", ip, "server_ip===", server_ip)
            if str(ip) == str(server_ip):
                #print("hellooooooooooooooooooooooooooooooooooooooooooo")
                return self.servers[ip]
        return None


      
            


       
       
   

