import sys,os
PATH_ABSOLUTE = str(os.environ.get('PATH_ABSOLUTE'))
sys.path.append(PATH_ABSOLUTE+'handledata/models')
sys.path.append(PATH_ABSOLUTE+'core')
sys.path.append(PATH_ABSOLUTE+'api')

import flowRule
import Dijkstra

class hostServerConnection(object):

    def __init__(self, topo_network, hosts, servers, priority):
        """
        topo: object topo network
        hosts: dictionary of host (key: ip, value: object)
        servers: dictionary of server (key: ip, value: object)
        """
        self.topo = topo_network
        self.hosts = hosts
        self.servers = servers
        self.priority = priority

        # cap nhap trong so do thi
        # self.update_topo()

        # khoi tao thuat toan tim duong
        self.sol = ""
        self.reverse_sol = ""
        
        # add flow
        self.flow = ""
        self.reverse_flow = ""

        # host ip
        self.host_ip = ""
        self.dest_ip = ""

    def set_host_ip(self, host_ip):
        self.host_ip = host_ip
    
    def update_topo(self, link_versions):
        self.topo.read_update_weight(link_versions)
    
    def find_src(self):
        
        host_object = self.hosts[self.host_ip]     
          
        return host_object

    def find_shortest_path(self):

        ##### alpha * path cost + beta * server cost
        # print("123")
        min_cost = 0
        host_object = self.find_src()
        the_first_key = list(self.servers)[0]
        dest_object = self.servers[the_first_key]
        path = ""

        # duyet qua tat ca server chieu xuoi
        for server in self.servers:       
            # chay thuat toan
            self.sol = Dijkstra.Dijkstra( topo=self.topo, start= host_object, end= self.servers[server])

            # reset routing
            self.sol.routing()
            ############### COST FUNCTION
            current_cost = 0.55 * self.sol.get_minimum_cost() + 0.45 * self.servers[server].get_server_cost()
            # print("2 ong chau")
            # print( self.sol.get_minimum_cost(), self.servers[server].get_server_cost())
            # print("current=", current_cost)
            # print("cost duong di=", self.sol.get_minimum_cost())
            # print("cost server=", self.servers[server].get_server_cost())
            # print("Current cost hien tai=", current_cost, "VOI DEST=", str(server) )
            # print("tap canh trong so tim thay")
            # print(self.sol.display_result())

            # print(min_cost, current_cost)
            if min_cost == 0:
                min_cost = current_cost

            if min_cost >= current_cost: 
                min_cost = current_cost
                # get server co cost be nhat va path den server do
                dest_object = self.servers[server]
                # print("SON TUAN DANG TEST: ", self.servers[server])
                path = self.sol.get_result()

        print("-------Duong tot nhat ok------", self.sol.display_result() )
        # bat dau goi flow rule 
        # print(path)
        print("Server cost cua path =", dest_object.get_server_cost())

        self.add_flow(host_object, dest_object, path)
      
        return dest_object.get_ip()
      
    def add_flow(self, host_object, dest_object, path):

        # di chieu nguoc den tu server duoc chon quay ve goc
        self.reverse_sol = Dijkstra.Dijkstra( topo=self.topo, start= dest_object, end= host_object)
        self.reverse_sol.routing()
        reverse_path = self.reverse_sol.get_result()

        # add flow chieu thuan
        #print("\n\nadd flow JSon")
        flow = flowRule.flowRule(topo = self.topo, shortest_path = path, src = host_object, dst = dest_object)
        flow.add_flow_rule(self.priority)
        flow_rule = flow.get_json_rule()

        #print("\n\nadd reverse flow JSon")
        reverse_flow = flowRule.flowRule(topo = self.topo, shortest_path = reverse_path, src = dest_object, dst = host_object)
        reverse_flow.add_flow_rule(self.priority)
        reverse_flow_rule = reverse_flow.get_json_rule()
        
        flow.write_json_rule_to_file(json_rule_path = flow_rule, 
                                 json_rule_reversing_path= reverse_flow_rule)