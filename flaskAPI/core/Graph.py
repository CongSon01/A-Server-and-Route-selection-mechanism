import sys
sys.path.append('/home/onos/Downloads/flaskSDN/flaskAPI/handledata/models')
import CusHost, CusLink, CusDevice
import json
import ast

class Graph(object):
    """
    Graph object adds topology network from file Json to Custopo object 
    """
    def __init__(self, topo, topo_path, host_path):
       """
       topo: Custopo object
       topo_file: holds json data file
       """
       self.topo = topo
       self.topo_file = ""
       self.host_file = ""
       PATH_CURRENT = '/home/onos/Downloads/flaskSDN/flaskAPI/'
       self.topo_path = PATH_CURRENT + topo_path
       self.host_path = PATH_CURRENT + host_path

       self.index_hosts = [20, 21, 23, 22]
       self.index_servers = [11,10,17] 
       self.load_topo()

    def load_topo(self):
        """
        Read topo json and save it to topo_file
        """
        with open(self.topo_path) as handle:
            self.topo_file = json.loads(handle.read())
            #self.topo_file =  ast.literal_eval(self.topo_file)
            #print(self.topo_file)
        
        self.create_topo()
        
    def create_topo(self):
        """  Adds data from topo_file to our topo object """
        self.add_devices()
        self.add_links()
        self.add_hosts()

    def add_links(self):
        for link in self.topo_file['links']:
            # extract data from dictionary
            src = link['src']
            dst = link['dst']
       
            id_src = src['id']
            id_dst = dst['id']
            port_out = src['port']
            port_in = dst['port']
            
            # get device src and dst objects
            d_src = self.find_device(id_src)
            d_dst = self.find_device(id_dst)
            # print("--------------------------------")
            # print(src)
            # print(dst)
            # print("--------------------------------")
            # print("src=", d_src.get_id())  
            # print("dst=", d_dst.get_id())
            

            # add edge between src and dst devices
            # trong so mac dinh la 10^-7
            edge1 = CusLink.DeviceEdge(d_src, d_dst, 0.0000001, port_in, port_out)
            edge2 = CusLink.DeviceEdge(d_dst, d_src, 0.0000001, port_out, port_in)
            
            # add edges to topo
            self.topo.add_edge(edge1)
            self.topo.add_edge(edge2)

    def add_devices(self):
        for device in self.topo_file['devices']:
            id = device['id']
            # create device object
            device = CusDevice.Device(id)
            # add device object to topo object
            self.topo.add_node(device)

    def add_hosts(self):
        with open(self.host_path) as handle:
            self.host_file = json.loads(handle.read())
            # self.host_file = "\'" + self.host_file + "\'"
            # self.host_file=  ast.literal_eval(self.host_file)
            # self.host_file = json.loads(self.host_file)

        hosts = dict()
        servers = dict()

        for host in self.host_file['hosts']:
            #print("123")
            host_mac = str(host['mac'])
            host_ip = str(host['ipAddresses'])
            port = int(host['port'])
            device_id = str(host['deviceId'])
            
            device = self.find_device(device_id)
            host = CusHost.Host( id = host_mac, device = device, port = port, ip= host_ip)

            # Tach chuoi va lay so cuoi dia chi ip cua host
            host_ip_split = host_ip.split(".")
            num_ip = int(host_ip_split[-1])
            print("Number Host IP", num_ip)

            # index_hosts = [20, 21, 23, 22]
            # index_servers = [11,10,17]
            # index_host = [1,2,3,4,5,6]
            # index_hosts = [0,2,3,4,5,6,7,8,9,10,11,12]
            # index_servers = [40,41,42,43,44,45,46,47,48,49,50,51]

            if num_ip in self.index_hosts:
                hosts[host_ip] = host   
            elif num_ip in self.index_servers:
                servers[host_ip] = host
               
            self.topo.add_node(host)
 
            edge1 = CusLink.HostEdge(host, device, 0.1 , port)
            edge2 = CusLink.HostEdge(device, host, 0.1 , port)
            
            self.topo.add_edge(edge1)
            self.topo.add_edge(edge2)

        self.topo.set_hosts(hosts= hosts)
        self.topo.set_servers(servers= servers)
        
    def find_device(self, target):
        nodes = self.topo.get_nodes()
        for device in nodes:
            if device.get_id() == target:
                return device
