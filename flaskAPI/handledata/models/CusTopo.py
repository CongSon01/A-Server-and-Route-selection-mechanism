import sys
import json
sys.path.append('/home/onos/Downloads/flaskSDN/flaskAPI/model')
# from flaskAPI.model import model
import model, model_1
class Topo(object):
    """Topology network object """
    def __init__(self):
        """
        nodes: array holds each Node object (Host or Switch)
        edges: dictionary has key:Source object and value: [Dest object, weight, Edge between]
        """
        self.nodes = []
        self.edges = {}
        # dicttionary has key: ip and value: host/server object
        self.hosts = dict() 
        self.servers = dict()

    def set_hosts(self, hosts):
        self.hosts = hosts

    def set_servers(self, servers):
        #print("da set server", servers)
        self.servers = servers

    def get_hosts(self):  
        return self.hosts

    def get_servers(self):
        #print("da return server")
        return self.servers

    def add_node(self, node):
        """
        node: Host or Switch object
        """
        if node in self.nodes:
            raise ValueError('Duplicate Node')
        else:
            self.nodes.append(node)
            self.edges[node] = []
       
    def add_edge(self, edge):
        """
        edge: Edge object
        """
        src_object = edge.get_src()
        dest_object = edge.get_dest()
        weight = edge.get_weight()
            
        if not (src_object in self.nodes and dest_object in self.nodes):
            raise ValueError('Node not in graph')

        # check does edge already added
        found = False
        for e in self.edges[src_object]:
            if e[0].get_id() == dest_object.get_id():
                found = True
                break

        # if edge not added  
        if found == False:
            self.edges[src_object].append( [dest_object, weight, edge] )
     
    def children_of(self, node):
        """
        Return children of any node object
        node: Host or Switch object
        """
        children = []
        for child in self.edges[node]:
            children.append(child)
        return children

    def has_node(self, node):
        return node in self.nodes

    def __str__(self):
        for src in self.nodes:
            for child in self.edges[src]:
                print( '{} --> {} has cost {} \n'.format(src.get_id(), child[0].get_id(), child[1]) )
        return "OK"

    def get_nodes(self):
        return self.nodes

    def get_edges(self):
        return self.edges

    def find_edge(self, src, dest):
        """
        Return edge object given src and dest object, else return None
        """
        found = None
        for child in self.edges[src]:
            if child[0].get_id() == dest.get_id():
                return child
        return found

    def find_device(self, node_id):
        """
        Return device object given node id, else return None
        """
        found = None
        for device in self.nodes:
            if device.get_id() == node_id:    
                return device
        return found

    def read_update_weight(self):
        """
        Read data from update_weights table-Mongo in SDN 248/250 and update new weight in each links
        """
        params_248 = model.get_multiple_data()
        params_250 = model_1.get_multiple_data()

        params = params_250 + params_248
        # print("+++++++truy van+++++++++++")
        # print(new_params)
        # print("+++++++truy cap+++++++++++")
        # print(new_params)
        # print(new_params[0]['src'])

        for link in params:
            src = link['src']
            dst = link['dst']
            weight = link['weight']

            src_object = self.find_device(src)
            dest_object = self.find_device(dst)             
            edge = self.find_edge(src= src_object, dest= dest_object)
            
            if edge == None:
                print("Not found edge")
                continue
            else:
                edge[1] = weight # update new weight in edge list
                edge[2].set_weight(weight= weight) # update new weight in edge object

    def add_topo(self, topo):
        print(topo)
               
       
 