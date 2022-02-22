class Criteria(object):

    def __init__(self, type):
        '''
        mac: mac address of device: string
        type: IN or OUT type of port 
        port: port of device
        '''
        self.mac = ""
        self.type = type
        self.port = ""

    def set_mac(self, mac):
        self.mac = mac

    def set_port(self, port):
        self.port = port
        
    def get_mac(self):
        return self.mac
    
    def get_type(self):
        return self.type

    def get_port(self):
        return self.port
