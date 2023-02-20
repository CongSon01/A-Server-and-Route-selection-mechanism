import numpy as np
class Host(object):
    def __init__(self, id, device, port, ip):
        ''' 
        id: id of host (string)
        device: switch object that connects to host 
        port: connnect port (int)
        ip: ip Address of host (string)
        '''
        self.id = id
        self.device = device
        self.port = port
        self.ip = ip
        self.server_cost_list = list()
        ############### khoi tao ban dau trong so max la 0.1
        ############ ve sau trong so duoc dieu chinh
        self.server_cost = 0.1

    def get_id(self):
        return self.id

    def get_device_id(self):
        return self.device.get_id()

    def get_port(self):
        return self.port

    def get_ip(self):
        return self.ip

    def add_cost(self, current_cost):
        self.server_cost_list.append(float(current_cost))
    
    def get_server_cost(self):
        return self.server_cost

    def calculate_final_cost(self):
        server_cost_vector = np.array( self.server_cost_list, dtype='f')
        self.server_cost = np.mean( self.get_min_max_scale(server_cost_vector) )
        
    def get_min_max_scale(self, x):
        min, max = x.min(), x.max()
        # cong them 10^-7 de tranh mau so bang 0 
        return (x - min + 10**-7) / (max - min + 10**-7)
    