import sys
sys.path.append('/home/onos/Downloads/flaskSDN/flaskAPI/core')
sys.path.append('/home/onos/Downloads/flaskSDN/flaskAPI/handledata/models')

import CusHost, Flow, Flows, Instruction, Selector, Treatment, Criteria
import json
import requests
from requests.auth import HTTPBasicAuth


class flowRule(object):
    """
    flowRule object generates json file which adds flow
    """
    def __init__(self, topo, shortest_path, src, dst):
        """
        topo: Custopo network object
        shortest_path: list of edge resuts in path
        src: starting node
        dst: ending node
        """
        self.topo = topo
        self.shortest_path = shortest_path
        self.src = src
        self.dst = dst
        self.json_rule = dict() 
        self.jsonRulePath = ""

    def get_json_rule(self):
        return self.json_rule

    def get_src(self):
        return self.src.get_id()

    def get_dst(self):
        return self.dst.get_id()

    def get_shortest_path(self):
        return self.shortest_path

    def create_flow_rule(self, flows, priority):  
        """
        Generates flow rule framework
        """
        for link in range ( len (self.shortest_path) ):
                    from_node = self.shortest_path[link].get_src()
                    to_node   = self.shortest_path[link].get_dest()
                    # abandon first edge 
                    if isinstance( from_node, CusHost.Host ):
                        continue                                         
                    elif isinstance( to_node, CusHost.Host):

                        device = from_node  
                        port_out =  self.shortest_path[link].get_port()

                        previous_link = self.shortest_path[ link -1 ]
                        from_node = previous_link.get_src()

                        if isinstance( from_node, CusHost.Host ):
                            port_in = previous_link.get_port()
                        else:
                            port_in = previous_link.get_port_in()                                 
                    else:            
                        port_out = self.shortest_path[link].get_port_out()
                        device = from_node
            
                        previous_link = self.shortest_path[ link - 1 ]
                        from_node = previous_link.get_src()

                        # trung gian dau tien bi vuong host
                        if isinstance( from_node, CusHost.Host ):
                            port_in = previous_link.get_port()
                        else: # cac trung gian con lai
                            port_in = self.shortest_path[link-1].get_port_in()

                    # priority +=1
                    flow = Flow.Flow(priority = priority, timeout = 600, isPermanent = True, deviceId = device.get_id()  )
                    treatment = Treatment.Treatment()
                    selector = Selector.Selector()

                    # add instruction to treatment
                    instruction = Instruction.Instruction(type = "OUTPUT", port = port_out)
                    # set port out
                    treatment.set_instructions( instruction_object = instruction )

                    # set criteria oobject
                    criteria = Criteria.Criteria(type = "IN_PORT")
                    criteria_src = Criteria.Criteria(type = "ETH_SRC")
                    criteria_dst = Criteria.Criteria(type = "ETH_DST")
                        
                    # set port in
                    criteria.set_port(port_in)

                    criteria_src.set_port(0) 
                    criteria_dst.set_port(0)

                    criteria_src.set_mac( self.src.get_id() )
                    criteria_dst.set_mac( self.dst.get_id() )
                    # add criteria to selector
                    selector.set_criterias(criteria_object = criteria)
                    selector.set_criterias(criteria_object = criteria_src)
                    selector.set_criterias(criteria_object = criteria_dst)

                    # add treat ment and selector to flow object
                    flow.set_treatment( treatment_object = treatment)
                    flow.set_selector( selector_object = selector)
                    # add each flow to flows object
                    flows.set_flows(flow_object = flow)

    def add_flow_rule(self, priority):
        """
        set attributes of flow rule
        """
        flows = Flows.Flows()
        self.create_flow_rule(flows, priority)

        json_flows = []
        self.json_rule['flows'] = json_flows

        # add flow rule value
        for f in flows.get_flows():
            json_flow = dict()
            json_flows.append( json_flow )
            json_flow['priority'] = f.get_priority()
            json_flow['timeout'] = f.get_timeout()
            json_flow['isPermanent'] = f.get_isPermanent()
            json_flow['deviceId'] = f.get_deviceId()

            # treatment dictionary
            json_treatment = dict()
            json_instructions = []
            json_treatment['instructions'] = json_instructions

            for instruct in f.get_treatment().get_instructions():
                json_instruction = dict() 
                json_instructions.append( json_instruction )  
                json_instruction['port'] = instruct.get_port()
                json_instruction['type'] = instruct.get_type()
              
            # add treatment dictionary to each flow
            json_flow['treatment'] = json_treatment

            # selector dictionary
            json_selector = dict()
            # add selector dictionary to each flow
            json_flow['selector'] = json_selector

            json_criterias = []
            json_selector['criteria'] = json_criterias

            count = 1
            for crite in f.get_selector().get_criterias():
                json_criteria = dict()
                json_criterias.append ( json_criteria )          
                json_criteria['port'] = crite.get_port()
                json_criteria['type'] = crite.get_type()

                # using count to avoid 'mac' key in the first instruction object
                if count != 1:
                    json_criteria['mac'] = crite.get_mac()
                else:
                    count += 1
              

    def write_json_rule_to_file(self, json_rule_path, json_rule_reversing_path):
        flows_reversing_path = json_rule_reversing_path['flows']
        flows_path = json_rule_path['flows']
        #print(flows_path)
     
        for elem in range ( len (flows_reversing_path) ):     
            temp =  flows_reversing_path[elem]
            flows_path.append( temp )

        #print( len (flows_path))
        self.jsonRulePath = json_rule_path
        #self.call_routing_api()
        
        with open('/home/onos/Downloads/flaskSDN/flaskAPI/jsonRulePath.json', 'w') as json_file:
            json.dump( json_rule_path, json_file)

        self.call_routing_api()
    
    def add_flow_ryu(self, data, ip_sdn):
        # flows_dict = { (str(int(dpid["deviceId"][-3:], 16))):list() for dpid in data["flows"] }
        for flow in data["flows"]:
            flow_value = {}
            dpid = flow["deviceId"][-3:]
            criteria = flow["selector"]["criteria"]
            for i in range(len(flow["selector"]["criteria"])):
                if criteria[i]["type"] == "IN_PORT":
                    in_port = criteria[i]["port"]
                if criteria[i]["type"] == "ETH_SRC":
                    dl_src = criteria[i]["mac"]
                if criteria[i]["type"] == "ETH_DST":
                    dl_dst = criteria[i]["mac"]
            # convert hex => int
            # flows_dict[str(int(dpid, 16))].append({
            flow_value = {
                "dpid": int(dpid, 16),
                "priority": int(flow["priority"]),
                "hard_timeout": int(flow["timeout"]),
                "actions": [
                    {
                        "type": flow["treatment"]["instructions"][0]["type"],
                        "port": int(flow["treatment"]["instructions"][0]["port"])
                    }
                ],
            
                "match": {
                    "in_port": int(in_port),
                    "dl_src": str(dl_src),
                    "dl_dst": str(dl_dst),
                }
            }
            print("add flow cho swich ",  int(dpid, 16))

            print(requests.post("http://"+ip_sdn+":8080/stats/flowentry/add", data=str(flow_value), headers={'Content-type': 'text/plain'}))
    
    def get_flow_of_controller(self, data, list_sw):
        flows = {"flows": []}
        for flow in data["flows"]:
            if ("s"+str(int(flow["deviceId"][-3:], 16) ))in list_sw:
                flows["flows"].append(flow)
        return flows


    def call_routing_api(self):
        """
        Automatically POST rulePath to API
        return 200 if successul routing
        """
        with open("/home/onos/Downloads/flaskSDN/flaskAPI/jsonRulePath.json") as json_file:
                data_raw = json.load(json_file)

        headers = {
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                    "Authorization": "Basic a2FyYWY6a2FyYWY="
                    }

        # try:
            # get full ip of SDN
        set_up_topo = json.load(open('/home/onos/Downloads/flaskSDN/flaskAPI/set_up/set_up_topo.json'))
        controllers = [controller for controller in set_up_topo["controllers"]]
    
        for i in range(len(controllers)):
            # id of flow
            query = {'appID': "test" + str(i)}
            list_sw = controllers[i]['switches']
            flows_value = self.get_flow_of_controller(data_raw, list_sw)
            if controllers[i]['controller'] == "onos":
                print("Add flow cho onos")
                print(flows_value)
                url_post = "http://"+ controllers[i]["ip"] + ":8181/onos/v1/flows?appId=onos.onosproject.routing"
                response = requests.post(url_post, params=query,auth=HTTPBasicAuth('onos', 'rocks'), data = json.dumps(flows_value), headers=  headers )
                print("Add flow may "+str(controllers[i]['ip']) +" : "+ str(response))

            elif controllers[i]['controller'] == "ryu":
                print("Add flow cho ryu")
                self.add_flow_ryu(flows_value, str(controllers[i]['ip']))

        # except:
        #     print("add flow xitttttttt")
        
        
    