import sys
sys.path.append('/home/onos/Downloads/A-Server-and-Route-selection-mechanism/Desktop/paper1/paper1/dataBaseMongo')
sys.path.append('/home/onos/Downloads/A-Server-and-Route-selection-mechanism/Desktop/paper1/paper1/api')
import numpy as np

class linkWeight(object):
    def __init__(self, id_src, id_dst):
        self.id_src = id_src
        self.id_dst = id_dst

        # WEIGHT MATRIX INCLUDES [DELAY, LINK_U, PACKET_LOSS]
        self.W = list()
        self.delay_stack = []
        self.link_utilization_stack = []
        self.packet_loss_stack = []

        self.byte_sent_stack = []
        self.byte_received_stack = []

        self.delay = 0.0
        self.link_utilization = 0.0
        self.packet_loss = 0.0

        self.byte_sent = 0.0
        self.byte_received = 0.0
            
    def get_id_src(self):
        return self.id_src

    def get_id_dst(self):
        return self.id_dst

    def update_weight(self, params_data):
        """
        Ham cap nhap trong so lien tuc khi co thay doi tu mang
        """
        self.delay = float(params_data['delay'])
        self.link_utilization = float(params_data['linkUtilization'])
        self.packet_loss = float(params_data['packetLoss'])
        self.byte_sent = float(params_data['byteSent'])
        self.byte_received = float(params_data['byteReceived'])

        self.delay_stack.append(self.delay)
        self.link_utilization_stack.append(self.link_utilization)
        self.packet_loss_stack.append(self.packet_loss)

        self.byte_sent_stack.append( self.byte_sent )
        self.byte_received_stack.append(self.byte_received)

    def find_link_cost(self):
        delay_vector            = np.array(self.delay_stack, dtype='f')
        link_utilization_vector = np.array(self.link_utilization_stack, dtype='f')
        packet_loss_vector      = np.array(self.packet_loss_stack, dtype='f')
        byte_sent_vector        = np.array(self.byte_sent_stack, dtype='f')   
        byte_received_vector    = np.array(self.byte_received_stack, dtype='f')     

        link_cost = list()
     
        self.W.append(delay_vector)
        self.W.append(link_utilization_vector)
        self.W.append(packet_loss_vector)
        self.W.append(byte_sent_vector)
        self.W.append(byte_received_vector)
        
        # print("len cua W", self.W)
        # print("-----------------")

        for x in range(len(self.W)):
            cost = np.mean(self.W[x])
            link_cost.append(cost)

        return link_cost

    