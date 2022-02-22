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

    def get_id(self):
        return self.id

    def get_device_id(self):
        return self.device.get_id()

    def get_port(self):
        return self.port

    def get_ip(self):
        return self.ip