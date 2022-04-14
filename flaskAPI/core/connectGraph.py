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
            try:
                with open(file) as handle:
                    object = json.loads( handle.read() )
                    object = ast.literal_eval( object )
            except:
                print("Loi khi doc topo")
           
            #print("-------------------------")
            devices = object['devices']
            links = object['links']
            for link in links:
                result_topo['links'].append(link)
            
            
            filename = '/home/onos/Downloads/flaskSDN/flaskAPI/run/bridge.txt'
            file1 = open(filename, 'r')
            Lines = file1.readlines()
            
            for line in Lines:
                result_topo['links'].append(json.loads(line))

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
        ###############################################
        ######## xoa cac host tu tap switch bien
        #### alo ai dot nhap  alo vao hop di
        
        remove_host_from_device = ["02", "0e", "07", "08", "0b", '12', '14', '1c', '19', '1a']
        # bridge = [['s11', 's18'], ['s2','s14'], ['s7', 's8'], ['s25', 's26'], ['s20', 's28']]

        for file in self.file_hosts:

            with open(file) as handle:
                object = json.loads(handle.read())
                object = "\'" + object + "\'"
                object =  ast.literal_eval(object)
                object = json.loads(object) 

            # try:
           
            # except:
            #     print("Loi khi doc host")
                
            #print(object)
            for host in object['hosts']:
                    # print("\n")
                    host_mac = str(host['mac'])   
                    try:    
                        host_ip = str(host['ipAddresses'][0]) 
                    except:
                        print("----------------------------------------rong host ip")
                            # print(host['ipAddresses'][0])
                    locations = host['locations']
                            #print("==========================================\n", locations)
                    location = locations[0]        
                    port = int(location['port'])
                   
                    device_id = str(location['elementId'])
                    
                    # lay chi so Hexa o 2 phan tu cuoi cung cua device_id
                    last_device_id = device_id[ -2: len(device_id) ]
                    # if  int(device_id[-1:-3]) in remove_host_from_device:
                    #     print("Xoa host tu switch bien------------------------->", device_id[-1] ) 
                    #     continue

                    # if  last_device_id in remove_host_from_device:
                    #     print("Xoa host tu switch bien------------------------->", last_device_id )
                    #     continue
                    # else:
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


