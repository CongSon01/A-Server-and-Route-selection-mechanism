import json
import ast

class connectGraph(object):
    def __init__(self, file_topos, file_hosts):

        self.file_topos = file_topos
        self.file_hosts = file_hosts

        self.merge_topo()
        self.merge_host()

    def merge_topo(self):  
        result_links = list()
        result_devices = list()
        result_topo = { 
            "devices": [],
            "links": []
        }

        for file in self.file_topos:

            with open(file) as handle:
                object = json.loads( handle.read() )
                object = ast.literal_eval( object )

            print("-------------------------")
            devices = object['devices']
            links = object['links']
            for link in links:
                result_topo['links'].append(link)
            
            link_fix = {
                    "src": {
                        "port": 6,
                        "id": "of:0000000000000003"
                    },
                    "dst": {
                        "port": 7,
                        "id": "of:0000000000000004"
                    }
            }
            result_topo['links'].append(link_fix)
            for switch in devices:
                result_topo['devices'].append(switch)
     
        # ghi ra file topo hop nhat mang
        file_topo_done =  '/home/onos/Downloads/flaskSDN/flaskAPI/topo.json'
        # file_host_done =  '/home/onos/Downloads/flaskSDN/flaskAPI/host.json'
        with open(file_topo_done, 'w') as output_file:
            json.dump(result_topo, output_file)

    def merge_host(self):
      
        result_host = { 
            "hosts": []     
        }

        for file in self.file_hosts:

            with open(file) as handle:
                object = json.loads(handle.read())
                object = "\'" + object + "\'"
                object =  ast.literal_eval(object)
                object = json.loads(object)

            for host in object['hosts']:
                #print("123")
                host_mac = str(host['mac'])
                host_ip = str(host['ipAddresses'][0])
                    
                locations = host['locations']
                location = locations[0]
                port = int(location['port'])
                device_id = str(location['elementId'])

                host_value = {
                    'port': port,
                    'mac': host_mac, 
                    'deviceId': device_id,
                    'ipAddresses': host_ip

                }

                result_host['hosts'].append(host_value)


        file_host_done =  '/home/onos/Downloads/flaskSDN/flaskAPI/host.json'
        with open(file_host_done, 'w') as output_file:
            json.dump(result_host, output_file)


# PATH_ABSOLUTE = "/home/onos/Downloads/flaskSDN/flaskAPI/"    
# topo_path_1 = PATH_ABSOLUTE + 'topo_1.json'
# topo_path_2 = PATH_ABSOLUTE + 'topo_2.json'
# host_path_1 = PATH_ABSOLUTE + 'host_1.json'
# host_path_2 = PATH_ABSOLUTE + 'host_2.json'
# topo_files = [topo_path_1, topo_path_2]
# host_files = [host_path_1, host_path_2]
# connectGraph(topo_files, host_files)


