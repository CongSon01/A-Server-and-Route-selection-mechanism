class Instruction(object):

    def __init__(self, type, port):
        """
        type: IN our OUT type of port (string)
        port: port number (int)
        """
        self.type = type
        self.port = port

    def set_port(self, port):
        self.port = port
        
    def get_type(self):
        return self.type
    
    def get_port(self):
        return self.port

        
