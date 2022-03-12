import numpy as np
import pandas as pd
import sub
import sys
sys.path.append('/home/onos/Downloads/flaskSDN/flaskAPI/model')
import model_250


class updateWeight(object):

    def __init__(self):
        self.params_data = ""
        self.link_set = set()
        self.consumer = sub.Sub()
        self.count = 0
       
    def get_link_set(self):
        return self.link_set

    def get_count(self):
        return self.count

    def set_count(self, count):
        self.count = count

    def reset_link_set(self):
        self.link_set = set()

    def read_params_from_rabbit(self):
        # pop data from RAbbit Queue
        self.consumer.receive_queue()
        self.params_data = self.consumer.peek_stack()
        self.count += 1

        self.update_link()

    def update_link(self):
        id_src = str (self.params_data['src'])
        id_dst = str (self.params_data['dst'])    
        link = self.has_link(target_src = id_src, target_dst = id_dst)
        
        # Neu link chua co trong tap canh thi khoi tao link
        if link == None:
            link_object = WeightLink(id_src= id_src, id_dst= id_dst)
            self.link_set.add(link_object)
            link_object.update_weight(params_data= self.params_data)
        # neu link da co trong tap canh thi cap nhat lai weight
        else:
            link.update_weight(params_data= self.params_data)
 
    def has_link(self, target_src, target_dst):
        found = None
        for link in self.link_set:
            if link.get_id_src() == target_src and link.get_id_dst() == target_dst:
                found = True
                return link
        return None

    def write_update_data_base(self):
        
        # xoa het trong so cu o Mongo
        model_250.remove_all()
        # model_1.remove_all()
        print("Write update weight to file ...")
        
        for link in self.link_set:
            src = link.get_id_src()
            dst = link.get_id_dst()
            weight = link.get_normalize_data()
           
            temp_data = { "src": src, "dst": dst, "weight": weight }
            # save into update weight database mongoDB
            model_250.insert_data(temp_data)
            # model_1.insert_data(temp_data)
            #history_weights.insert_data(temp_data)
        
class WeightLink(object):
        def __init__(self, id_src, id_dst):
            self.id_src = id_src
            self.id_dst = id_dst
           
            # WEIGHT MATRIX INCLUDES [DELAY, LINK_U, PACKET_LOSS] 
            self.W = []
            self.delay_stack = []
            self.link_utilization_stack = []
            self.packet_loss_stack = []

            self.delay = 0.0
            self.link_utilization = 0.0
            self.packet_loss = 0.0
            
            self.alpha = 0.2
            self.beta = 0.4
            self.gamma = 0.4

        def get_id_src(self):
            return self.id_src

        def get_id_dst(self):
            return self.id_dst
    
        def get_link_cost(self, mean_W):     
            link_cost = self.alpha * mean_W[0] + self.beta * mean_W[1] + self.gamma * mean_W[2]
            return link_cost

        def get_min_max_scale(self, x):
            min, max = x.min(), x.max()
            # cong them 0.1 de tranh mau so bang 0 
            x_scaled = (x - min) / (max - min + 0.1)
            return x_scaled

        def update_weight(self, params_data):
        
            self.delay = float( params_data['delay'] )
            self.link_utilization = float( params_data['linkUtilization'] )
            self.packet_loss = float( params_data['packetLoss'] )
            
            # day cac tham so vao stack
            self.delay_stack.append( self.delay )
            self.link_utilization_stack.append( self.link_utilization ) 
            self.packet_loss_stack.append( self.packet_loss )

        def get_normalize_data(self):

            # convert list to vector with float type
            delay_vector            = np.array( self.delay_stack, dtype='f')
            link_utilization_vector = np.array( self.link_utilization_stack, dtype='f')
            packet_loss_vector      = np.array( self.packet_loss_stack, dtype='f')

            # tinh trung binh cac tham so
            mean_W = []
            self.W.append( delay_vector )
            self.W.append( link_utilization_vector )
            self.W.append( packet_loss_vector )
        
            for x in self.W:
                x = self.get_min_max_scale(x= x)
                mean = np.average(x)
                mean_W.append(mean)

            link_cost = self.get_link_cost(mean_W)
            return link_cost