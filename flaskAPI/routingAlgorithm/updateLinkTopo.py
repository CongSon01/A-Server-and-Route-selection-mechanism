import numpy as np
import sys

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
    # def write_update_link_to_data_base(self):
        
        # print(Link_Versions)
        # xoa het trong so cu o Mongo
        # model_250.remove_all()
        # LinkVersion.remove_all()
        # model_1.remove_all()

        #print("-------------------Write update link weight to MONGO------------- ...")  
        # self.count +=1
        # print("-------------------------------------goi lan thu", self.count)
        # print("do dai link set")
        # print(len(self.link_set))
        # self.link_version +=1   
        # self.count +=1 
        # print("call ", self.count)
        new_link_topo = list()
        for link in self.link_set:
            # print("\n")
            #print( link.get_id_src(), "----------------->",link.get_id_dst() )
            src = link.get_id_src()
            dst = link.get_id_dst()
            # weight = link.get_normalize_data()
          
            weight = link.find_link_cost()
            # delay = weight[0]
            # link_utilization = weight[1]
            # packet_loss = weight[2]
            # print("src", src)
            # print("dst", dst)
            # print("delay:", delay)
            # print("link_utilization:", link_utilization)
            # print("packet_loss:", packet_loss)
            # print("linkVersion:", self.link_version)    
            # print("canh co trong so =", weight)
            
            temp_data = { "src": src, 
                          "dst": dst,
                          "weight": weight
                        } 
            new_link_topo.append(temp_data)
           
            # print("Weight cua link =", weight)
            
            # temp_data = {'src': 'of:0000000000000010', 'packetLoss': 1.0, 'dst': 'of:000000000000000d'{'src': 'of:0000000000000010', 'packetLoss', : 'linkVersion': 17, 'delay': 251.0, 'linkUtilization': 0.000112} 
            #         {'src': ''of:00000d0e00la0y0'000011', 'packetLoss': : 0.16666667169650.0, , 'dst''linkUtilization': 0.000112}: 'of:0000000000000012', 'linkVersion': 32, 'delay': 6237021600000000.0, 'linkUtilization': 0.000112}
            # print(temp_data)
            # save into update weight database mongoDB
            # model_250.insert_data(temp_data)

            # # temp_data = { "src": src, "dst": dst, "LU": str(link_utilization)}
            # try:
            #      LinkVersion.insert_data(temp_data)
            #     #  print("+++++++++++++++ Link version update Thanh cong")
            # except:
            #      print("--------------- Link version update loi")
                
            # model_1.insert_data(temp_data)
            # history_weights.insert_data(temp_data)
        
        # LinkVersion.insert_n_data(Link_Versions)
        # reset link set
        self.link_set = list()
        return new_link_topo
        # self.write_update_link_to_topo()
        #print("lennn cua set", len(self.link_set))

    # def write_update_link_to_topo(self, link_versions):
    #     self.topo.read_update_weight(link_versions)
        
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
            
            self.alpha = 0.3
            self.beta = 0.5
            self.gamma = 0.2

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