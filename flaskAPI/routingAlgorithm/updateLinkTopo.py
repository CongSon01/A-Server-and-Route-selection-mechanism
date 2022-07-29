import numpy as np
import sys
sys.path.append("/home/onos/Downloads/A-Server-and-Route-selection-mechanism/flaskAPI/model")
import LinkCost

class updateLinkTopo(object):

    def __init__(self, link_verions):
        self.link_versions = link_verions
        self.link_set = list()
        self.update_link()
        self.count = 0
        
    def update_link(self):
        # print("Do dai data doc tu R con ", len(self.link_versions))
        for link_params in self.link_versions:
            id_src = str( link_params['src'] )
            id_dst = str( link_params['dst'] )
            link = None
 
            link = self.has_link(target_src = id_src, target_dst = id_dst)
            
            # Neu link chua co trong tap canh thi khoi tao link
            if link == None:
                link_object = WeightLink(id_src= id_src, id_dst= id_dst)
                self.link_set.append(link_object)
                link_object.update_weight(params_data= link_params)
            # neu link da co trong tap canh thi cap nhat lai weight
            else:
                link.update_weight(params_data= link_params)
 
    def has_link(self, target_src, target_dst):
        found = None
        for link in self.link_set:
            if link.get_id_src() == target_src and link.get_id_dst() == target_dst:
                found = True
                return link
        return None

    def get_link_weight(self):
    
        LinkCost.remove_all()
        for link in self.link_set:  
            src = link.get_id_src()
            dst = link.get_id_dst()
           
            weight = link.find_link_cost()       
            temp_data = { "src": src, 
                          "dst": dst,
                          "weight": float(weight)
                        }     
            try:
                 LinkCost.insert_data(temp_data)            
            except:
                 print("--------------- Write Link Cost loi")
                
        self.link_set = list()
           
class WeightLink(object):
        def __init__(self, id_src, id_dst):
            self.id_src = id_src
            self.id_dst = id_dst
           
            # WEIGHT MATRIX INCLUDES [DELAY, LINK_U, PACKET_LOSS] 
            self.W = list()
            self.delay_stack = []
            self.link_utilization_stack = []
            self.packet_loss_stack = []

            self.delay = 0.0
            self.link_utilization = 0.0
            self.packet_loss = 0.0
            
            self.alpha = 0.4
            self.beta = 0.3
            self.gamma = 0.3

            # self.normalize_cost = 0.0000001

        def get_id_src(self):
            return self.id_src

        def get_id_dst(self):
            return self.id_dst

        def update_weight(self, params_data):
            """
            Ham cap nhap trong so lien tuc khi co thay doi tu mang
            """
            # print("params", params_data)
            self.delay = float( params_data['delay'] )
            self.link_utilization = float( params_data['linkUtilization'] )
            self.packet_loss = float( params_data['packetLoss'] )
            
            #print("input = ", self.delay, self.link_utilization, self.packet_loss)
            # day cac tham so vao stack
            self.delay_stack.append( self.delay )
            self.link_utilization_stack.append( self.link_utilization ) 
            self.packet_loss_stack.append( self.packet_loss )

        def find_link_cost(self):
                delay_vector            = np.array( self.delay_stack, dtype='f')
                link_utilization_vector = np.array( self.link_utilization_stack, dtype='f')
                packet_loss_vector      = np.array( self.packet_loss_stack, dtype='f')
 
                self.W.append( delay_vector )
                self.W.append( link_utilization_vector )
                self.W.append( packet_loss_vector )
                scaled_params = list()       
             
                for x in self.W:                  
                    x = np.mean(x)
                    scaled_params.append(x)
                        
                scaled_params = self.get_min_max_scale(scaled_params)                    
                training_cost = self.get_training_cost(scaled_params)            
                      
                #### giai phong het gia tri cu       
                self.W = list()
                del self.delay_stack
                del self.link_utilization_stack
                del self.packet_loss_stack 
                return training_cost
            
        def get_training_cost(self, link_cost):    
            return self.alpha * link_cost[0] + self.beta * link_cost[1] + self.gamma * link_cost[2]

        def get_min_max_scale(self, x):
            x = np.array(x)
            min, max = x.min(), x.max()
            # cong them 10^-7 de tranh mau so bang 0 
            return (x - min) / (max - min)