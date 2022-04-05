import numpy as np
import sub
import sys, json, requests, random
sys.path.append('/home/onos/Downloads/flask_SDN/Flask-SDN/flaskAPI/model')
import LinkVersion

class updateWeight(object):

    def __init__(self, topo):
        self.params_data = ""
        self.link_set = list()
        self.consumer = sub.Sub()
        self.count = 0
        self.topo = topo
        self.link_version = 0

    def get_link_set(self):
        return self.link_set

    def get_count(self):
        return self.count

    def set_count(self, count):
        self.count = count

    def reset_link_set(self):
        self.link_set = list()

    def read_params_from_rabbit(self):
        # pop data from RAbbit Queue
        self.consumer.receive_queue()
        self.params_data = self.consumer.peek_stack()
        #print("dau vao canh-------------------->", self.params_data)
        self.count += 1

        self.update_link()

    def update_link(self):
        id_src = str (self.params_data['src'])
        id_dst = str (self.params_data['dst'])    
        link = self.has_link(target_src = id_src, target_dst = id_dst)
        
        # Neu link chua co trong tap canh thi khoi tao link
        if link == None:
            link_object = WeightLink(id_src= id_src, id_dst= id_dst)
            self.link_set.append(link_object)
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

    def write_update_link_to_data_base(self):

        # self.count +=1
        # print("Goi lan thu", self.count)
        
        print("LINK________________VERSION______________")
        # print(Link_Versions)
        # xoa het trong so cu o Mongo
        # model_250.remove_all()
        try:
            LinkVersion.remove_all()
        except:
            print("Remove loi .................")
        # model_1.remove_all()

        # print("-------------------Write update link weight to MONGO------------- ...")  
        # print("LINK_____LENGTH___________VERSION______________")
        # print(len(self.link_set))
        self.link_version +=1   
      
        for link in self.link_set:
            # print("\n")
            #print( link.get_id_src(), "----------------->",link.get_id_dst() )
            src = link.get_id_src()
            dst = link.get_id_dst()
            # weight = link.get_normalize_data()
          
            weight = link.find_link_cost()
            delay = weight[0]
            link_utilization = weight[1]
            packet_loss = weight[2]
            # print("src", src)
            # print("dst", dst)
            # print("delay:", delay)
            # print("link_utilization:", link_utilization)
            # print("packet_loss:", packet_loss)
            # print("linkVersion:", self.link_version)
          
            temp_data = { "src": src, 
                          "dst": dst,
                          "delay": float(delay),
                          "linkUtilization": float(link_utilization),
                          "packetLoss": float(packet_loss),
                          "linkVersion": float(self.link_version),
                          "IpSDN": "10.20.0.248"
                        } 
            # print(temp_data)
            # print("version =", self.link_version)
            # temp_data = {'src': 'of:0000000000000010', 'packetLoss': 1.0, 'dst': 'of:000000000000000d'{'src': 'of:0000000000000010', 'packetLoss', : 'linkVersion': 17, 'delay': 251.0, 'linkUtilization': 0.000112} 
            #         {'src': ''of:00000d0e00la0y0'000011', 'packetLoss': : 0.16666667169650.0, , 'dst''linkUtilization': 0.000112}: 'of:0000000000000012', 'linkVersion': 32, 'delay': 6237021600000000.0, 'linkUtilization': 0.000112}
            # print(temp_data)
            # save into update weight database mongoDB
            # model_250.insert_data(temp_data)

            # temp_data = { "src": src, "dst": dst, "LU": str(link_utilization)}
            try:
                 LinkVersion.insert_data(temp_data)
            except:
                 print("--------------- Local Link version update loi")
                
            # model_1.insert_data(temp_data)
            # history_weights.insert_data(temp_data)
        # Ghi W ong
        W = 2
        ip_sdn = ['10.20.0.251','10.20.0.243', '10.20.0.244']
        try:
            data = LinkVersion.get_multiple_data()
            for ip in random.sample(ip_sdn, W):  
                print("goi ip", ip)
                url = "http://" + ip + ":5000/write_link_version/"
                requests.post(url, data= json.dumps( { 'link_versions':data} ) )
        except:
            print("flask Goi nhieu SDN loiiiiiiiiiiiiiiiiiiiii")
        # # try:
        #     LinkVersion.insert_n_data(LinkVersions)
        # except:
        #     print("--------------- Link Nhieu version update loiiiiiiiiiiiiiiii")
        
        # reset link set
        self.reset_link_set()
       
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
            
            self.alpha = 0.4
            self.beta = 0.4
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
            self.delay = float( params_data['delay'] )
            self.link_utilization = float( params_data['linkUtilization'] )
            self.packet_loss = float( params_data['packetLoss'] )
            
            #print("input = ", self.delay, self.link_utilization, self.packet_loss)
            # day cac tham so vao stack
            self.delay_stack.append( self.delay )
            self.link_utilization_stack.append( self.link_utilization ) 
            self.packet_loss_stack.append( self.packet_loss )

        def find_link_cost(self):

            # if  not self.delay_stack or not self.link_utilization_stack or not self.packet_loss_stack:
            #     return self.normalize_cost
            # else:
                # convert list to vector with float type
                delay_vector            = np.array( self.delay_stack, dtype='f')
                link_utilization_vector = np.array( self.link_utilization_stack, dtype='f')
                packet_loss_vector      = np.array( self.packet_loss_stack, dtype='f')

                # print("Thay doiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii")
                # print(delay_vector)
                # print(link_utilization_vector)
                # print(packet_loss_vector)

                link_cost = list()
                self.W.append( delay_vector )
                self.W.append( link_utilization_vector )
                self.W.append( packet_loss_vector )
            
                # print("W =====================")
                # print(self.W)
                # print("len W ===================", len(self.W))
               
                # if len(self.W) > 3:
                #     print(len(self.W))
                #     print(self.id_src, "--------------------------------------------->", self.id_dst)
                for x in range( len(self.W) ):
                    # x_scale = self.get_min_max_scale(x= self.W[x])
                    # print("scale")
                    # print(x_scale)
                    # cong thuc tinh delay
                    if x == 0:
                        cost = np.prod( self.W[x] )
                        #print("delayyy", cost)
                    # cong thuc tinh trong so khac
                    else:
                        cost = np.mean(self.W[x])
                        #print("trong so khac", cost)

                    link_cost.append(cost)
                
                # print("link cost")
                # print(link_cost)
                # self.normalize_cost = self.get_normalize_cost(link_cost)

                #### giai phong het gia tri thoi gian cu
                
                # self.W = list()
                # del self.delay_stack
                # del self.link_utilization_stack
                # del self.packet_loss_stack 
                # return self.normalize_cost
                return link_cost
            
        def get_normalize_cost(self, link_cost):     
            return self.alpha * link_cost[0] + self.beta * link_cost[1] + self.gamma * link_cost[2]

        def get_min_max_scale(self, x):
            min, max = x.min(), x.max()
            # cong them 10^-7 de tranh mau so bang 0 
            return (x - min + 0.0000001) / (max - min + 0.0000001)
