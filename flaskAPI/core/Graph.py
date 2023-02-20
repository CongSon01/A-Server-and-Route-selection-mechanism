import sys
sys.path.append('/home/onos/Downloads/A-Server-and-Route-selection-mechanism/flaskAPI/handledata/models')
import CusHost, CusLink, CusDevice
import json
import ast, os

set_up_topo = json.load(open('/home/onos/Downloads/A-Server-and-Route-selection-mechanism/flaskAPI/set_up/set_up_topo.json'))

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
        PATH_CURRENT = '/home/onos/Downloads/A-Server-and-Route-selection-mechanism/flaskAPI/'
        self.topo_path = PATH_CURRENT + topo_path
        self.host_path = PATH_CURRENT + host_path

        # day la name cua host va server
        self.name_hosts =   set_up_topo['hosts']
        self.name_servers = set_up_topo['servers']
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
        """
        connects links between device A and device B
        """
        for link in self.topo_file['links']:
            src = link['src']
            dst = link['dst']
       
            id_src = src['id']
            id_dst = dst['id']
            port_out = src['port']
            port_in = dst['port']
            
            # get device src and dst objects
            d_src = self.find_device(id_src)
            d_dst = self.find_device(id_dst)

            # get label of link

            # add edge between src and dst devices
            # trong so mac dinh la 10^-7
            ###### trong so ban dau la 1
            ######### ve sau trong so thay doi tu 0 den 1
            edge1 = CusLink.DeviceEdge(d_src, d_dst, 1, port_in, port_out)
            edge2 = CusLink.DeviceEdge(d_dst, d_src, 1, port_out, port_in)
            
            # add edges to topo
            self.topo.add_edge(edge1)
            self.topo.add_edge(edge2)
    

    def add_devices(self):
        for device in self.topo_file['devices']:
            id = device['id']
            # create device object
            device = CusDevice.Device(id)

            # print("device", device.get_id())
            # add device object to topo object
            self.topo.add_node(device)

    def add_hosts(self):
        """
        connect links between hosts/servers and devices
        """
        with open(self.host_path) as handle:
            self.host_file = json.loads(handle.read())
            # self.host_file = "\'" + self.host_file + "\'"
            # self.host_file=  ast.literal_eval(self.host_file)
            # self.host_file = json.loads(self.host_file)

        hosts = dict()
        servers = dict()
        for host in self.host_file['hosts']:
            host_mac = str(host['mac'])
            host_ip = str(host['ipAddresses'])
            port = int(host['port'])
            device_id = str(host['deviceId'])
            
            device = self.find_device(device_id)
            host_object = CusHost.Host( id = host_mac, device = device, port = port, ip= host_ip)

            # Tach chuoi va lay so cuoi dia chi ip cua host
            host_ip_split = host_ip.split(".")
            name_host_tmp = "h"+str(host_ip_split[-1])
            # print(name_host_tmp)

            if  name_host_tmp in self.name_hosts and host_ip not in hosts:

                    hosts[host_ip] = host_object               
                    self.topo.add_node(host_object)
                    
                    ######### trong so ban dau la 1
                    ######### ve sau trong so thay doi tu 0 den 1
                    edge1 = CusLink.HostEdge(host_object, device, 1 , port)
                    edge2 = CusLink.HostEdge(device, host_object, 1 , port)
                        
                    self.topo.add_edge(edge1)
                    self.topo.add_edge(edge2)

            elif name_host_tmp  in self.name_servers and host_ip not in servers:
                    # print("Number Server IP", host_ip)
                    servers[host_ip] = host_object
                                     
                    self.topo.add_node(host_object)

                    ######### trong so ban dau la 1
                    ######### ve sau trong so thay doi tu 0 den 1
                    edge1 = CusLink.HostEdge(host_object, device, 1 , port)
                    edge2 = CusLink.HostEdge(device, host_object, 1 , port)
                        
                    self.topo.add_edge(edge1)
                    self.topo.add_edge(edge2)

        self.topo.set_hosts(hosts= hosts)
        self.topo.set_servers(servers= servers)
    
        print("TAP HOSTS")
        for h in hosts:
            print(h)
        
        print("TAP SERVERS")
        for s in servers:
            file_name = "/home/onos/Downloads/A-Server-and-Route-selection-mechanism/flaskAPI/run/server_info/" + str(s) + ".txt"
            if os.path.isfile(file_name): 
                os.remove(file_name) 
            f= open(file_name,"w+")
            print(s)

    def find_device(self, target):
        nodes = self.topo.get_nodes()
        for device in nodes:
            if device.get_id() == target:
                return device
