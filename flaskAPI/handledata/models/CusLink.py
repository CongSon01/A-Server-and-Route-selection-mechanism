# class Edge(object):

#     def __init__(self, id_src, id_dest, weight, port_in, port_out):
#         '''assume src and dest are nodes '''
#         self.id_src = id_src
#         self.id_dest = id_dest
#         self.weight = weight
#         self.port_in = port_in
#         self.port_out = port_out

#     def get_source(self):
#         return self.id_src

#     def get_destination(self):
#         return self.id_dest

#     def get_weight(self):
#         return self.weight

#     def get_port_in():
#         return self.port_in

#     def get_port_out():
#         return self.port_out

#     def __str__(self):
#         return  'From {} to {} has cost = {}'.format(self.get_source().get_id(), 
#                     self.get_destination().get_id(), self.get_weight() )
#         # self.get_source + '-->' + \
#         #    self.get_destination

# class DeviceEdge():

class Edge(object):
    """
    Abstract class holds Edge object
    """

    def __init__(self, src, dest, weight):
        '''
        src: source device object
        dest: dest device object
        weight: cost between src dest (float)
         '''
        self.src = src
        self.dest = dest
        self.weight = weight

    def set_src(self, src):
        self.src = src

    def set_dest(self, dest):
        self.dest = dest

    def set_weight(self, weight):
        self.weight = weight
 
    def get_src(self):
        return self.src

    def get_dest(self):
        return self.dest

    def get_weight(self):
        return self.weight

    def set_weight(self, weight):
        self.weight = weight

class DeviceEdge(Edge):
    """
    Inherited from Edge object
    """

    def __init__(self, src, dest, weight, port_in, port_out):
        super(DeviceEdge, self).__init__(src, dest, weight)
        self.port_in = port_in
        self.port_out = port_out
    
    def get_port_in(self):
        return self.port_in

    def get_port_out(self):
        return self.port_out

    def __str__(self):
        return  'From {} to {} has cost = {}'.format(self.get_src().get_id(), 
                    self.get_dest().get_id(), self.get_weight() )

class HostEdge(Edge):
    """Host object is inherited from Edge object"""
   
    def __init__(self, src, dest, weight, port):
        super(HostEdge, self).__init__(src, dest, weight)
        self.port = port
    
    def get_port(self):
        return self.port

 
    
        
       