import json
import ast

class connectGraph(object):
    def __init__(self, file_topos, file_hosts):
        self.file_topos = file_topos
        self.file_hosts = file_hosts
        self.merge_topo()
        self.merge_host()

    def merge_topo(self):   
        result_topo = { 
            "devices": [],
            "links": []
        }

        for file in self.file_topos:
            try:
                with open(file) as handle:
                    object = json.loads( handle.read() )
                    object = ast.literal_eval( object )
            except:
                print("Loi khi doc topo")
           
            devices = object['devices']
            links = object['links']
            # add links to Topo file
            result_topo['links'] = [ link for link in links ]

            # add bridges to Topo file
            bridges = open('/home/onos/Downloads/flaskSDN/flaskAPI/run/bridge.txt', 'r').readlines()
            # result_topo['links'] = [ json.loads(line) for line in bridges ]
            for line in bridges:
                result_topo['links'].append( json.loads(line) )


            # add switches to Topo file 
            # result_topo['devices'] = [ switch for switch in devices ]
            for switch in devices:
                result_topo['devices'].append( switch )
     
        # ghi ra file topo hop nhat mang
        file_topo_done =  '/home/onos/Downloads/flaskSDN/flaskAPI/topo.json'
        with open(file_topo_done, 'w') as output_file:
            json.dump(result_topo, output_file)

    def merge_host(self): 
        result_host = { 
            "hosts": []     
        }
        # load host tu file
        for file in self.file_hosts:
            with open(file) as handle:
                object = json.loads(handle.read())
                object = "\'" + object + "\'"
                object =  ast.literal_eval(object)
                object = json.loads(object) 

            for host in object['hosts']:
                    host_mac = str(host['mac'])   
                    try:    
                        host_ip = str(host['ipAddresses'][0]) 
                    except:
                        print("----------------------------------------rong host ip")
                        
                    locations = host['locations']                 
                    location = locations[0]        
                    port = int(location['port'])              
                    device_id = str(location['elementId'])

                    ####################### cau
                    bridges = open('/home/onos/Downloads/flaskSDN/flaskAPI/run/bridge.txt', 'r').readlines()
                    list_bridges = [ json.loads(host)['src']['id'] for host in bridges ]

                    # if  str(device_id) in list_bridges:
                    #     # print("XOA HOST ", host_ip)
                    #     # print("DEVICE :", device_id)
                    #     continue
                    # else:

                        # add host data to Host file
                    host_value = {
                                    'port': port,
                                    'mac': host_mac, 
                                    'deviceId': device_id,
                                    'ipAddresses': host_ip
                            }
                    result_host['hosts'].append(host_value)

        # ghi ra file host cuoi cung       
        file_host_done =  '/home/onos/Downloads/flaskSDN/flaskAPI/host.json'
        with open(file_host_done, 'w') as output_file:
            json.dump(result_host, output_file)

