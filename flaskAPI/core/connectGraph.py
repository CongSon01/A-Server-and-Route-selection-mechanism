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
            
            link_fix_xuoi_1 = {
                    "src": {
                        "port": 10,
                        "id": "of:0000000000000007"
                    },
                    "dst": {
                        "port": 10,
                        "id": "of:0000000000000008"
                    }
            }
  
            link_fix_nguoc_1 = {
                    "src": {
                        "port": 10,
                        "id": "of:0000000000000008"
                    },
                    "dst": {
                        "port": 10,
                        "id": "of:0000000000000007"
                    }
            }

            ###########################
            link_fix_xuoi_2 = {
                    "src": {
                        "port": 10,
                        "id": "of:0000000000000002"
                    },
                    "dst": {
                        "port": 10,
                        "id": "of:000000000000000e"
                    }
            }

            link_fix_nguoc_2 = {
                    "src": {
                        "port": 10,
                        "id": "of:000000000000000e"
                    },
                    "dst": {
                        "port": 10,
                        "id": "of:0000000000000002"
                    }
            }

            result_topo['links'].append(link_fix_xuoi_1)
            result_topo['links'].append(link_fix_nguoc_1)
            result_topo['links'].append(link_fix_xuoi_2)
            result_topo['links'].append(link_fix_nguoc_2)

            for switch in devices:
                result_topo['devices'].append(switch)
     
        # ghi ra file topo hop nhat mang
        file_topo_done =  '/home/onos/Downloads/flask_SDN/Flask-SDN/flaskAPI/topo.json'
        # file_host_done =  '/home/onos/Downloads/flask_SDN/Flask-SDN/flaskAPI/host.json'
        with open(file_topo_done, 'w') as output_file:
            json.dump(result_topo, output_file)

    def merge_host(self):
      
        result_host = { 
            "hosts": []     
        }
        ###############################################
        ######## xoa cac host tu tap switch bien
        #### alo ai dot nhap  alo vao hop di
        
        remove_host_from_device = ["02", "08", "07", "0e"]

        for file in self.file_hosts:

            with open(file) as handle:
                object = json.loads(handle.read())
                object = "\'" + object + "\'"
                object =  ast.literal_eval(object)
                object = json.loads(object) 
                
            #print(object)
            for host in object['hosts']:
                #print("123")
                host_mac = str(host['mac'])       
                host_ip = str(host['ipAddresses'][0]) 
                #print("--------------------------->IP-------------->", host_ip, "\n")
                # print(host['ipAddresses'][0])
                locations = host['locations']
                #print("==========================================\n", locations)
                location = locations[0]        
                port = int(location['port'])

                try:
                    device_id = str(location['elementId'])
                    #print("---------------------------ID-------------\n", device_id)

                    #neu dia chi device la 8 va 14 thi xoa het host o device day
                    #day la device cau noi giua 2 SDN
                    
                    # lay chi so Hexa o 2 phan tu cuoi cung cua device_id
                    last_device_id = device_id[ -2: len(device_id) ]
                    # if  int(device_id[-1:-3]) in remove_host_from_device:
                    #     print("Xoa host tu switch bien------------------------->", device_id[-1] ) 
                    #     continue

                    if  last_device_id in remove_host_from_device:
                        print("Xoa host tu switch bien------------------------->",  last_device_id ) 
                        continue
                    else:
                        print("hostip = ", host_ip)
                        print("Id", device_id)
                        host_value = {
                            'port': port,
                            'mac': host_mac, 
                            'deviceId': device_id,
                            'ipAddresses': host_ip
                    }

                    result_host['hosts'].append(host_value)
                    #print("hostip = ", host_ip)
                    print("Id", device_id)
                    host_value = {
                        'port': port,
                        'mac': host_mac, 
                        'deviceId': device_id,
                        'ipAddresses': host_ip
                    }

                    result_host['hosts'].append(host_value)
                except:
                    print("----------------------------Loiiiiiiiiiiiiiiiiiiii IP host ------------------------------------")

        file_host_done =  '/home/onos/Downloads/flask_SDN/Flask-SDN/flaskAPI/host.json'
        with open(file_host_done, 'w') as output_file:
            json.dump(result_host, output_file)


# PATH_ABSOLUTE = "/home/onos/Downloads/flask_SDN/Flask-SDN/flaskAPI/"    
# topo_path_1 = PATH_ABSOLUTE + 'topo_1.json'
# topo_path_2 = PATH_ABSOLUTE + 'topo_2.json'
# host_path_1 = PATH_ABSOLUTE + 'host_1.json'
# host_path_2 = PATH_ABSOLUTE + 'host_2.json'
# topo_files = [topo_path_1, topo_path_2]
# host_files = [host_path_1, host_path_2]
# connectGraph(topo_files, host_files)


