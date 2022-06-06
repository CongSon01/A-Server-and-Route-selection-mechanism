import requests
import json
from requests.auth import HTTPBasicAuth

# {
#             "mac": "EA:33:49:3E:D8:71",
#             "port": 10,
#             "ipAddresses": "10.0.0.66",
#             "deviceId": "of:0000000000000056"
#         }

def call_host_api_sdn(list_ip):
    
    for ip in range(len(list_ip)):
        response = requests.get('http://' + list_ip[ip] + ':8080/hosts',
        auth=HTTPBasicAuth('onos', 'rocks'))
        
        object = json.loads(response.content)
    #   with open('/home/onos/Downloads/flaskSDN/flaskAPI/hosts/host_'+str(ip+1)+'.json', 'w') as f:
    #         json.dump(response.content, f)
    result_host = { 
            "hosts": []     
    }
    for host in object['hosts']:
        
        bridges = open('/home/onos/Downloads/flaskSDN/flaskAPI/run/bridge.txt', 'r').readlines()
        
        list_bridges = [ json.loads(hosts)['src']['id'] for hosts in bridges ]

        print(list_bridges)

        if (host['ipv4'] == []):
            print("BO QUA")
            continue

        locations = host['port']      
        device_id = 'of:' + str(locations['dpid'])
        print(device_id)

        if  str(device_id) in list_bridges:
            print("XOA HOST ", host_ip, "TU THIET BI", device_id)
            # print("DEVICE :", device_id)
            continue

        host_mac = str(host['mac'])
        try:    
            host_ip = str(host['ipv4'][0]) 
        except:
            print("----------------------------------------rong host ip")
                        
                    
             # add host data to Host file
        port = int(locations['port_no'])
        host_value = {
                        'port': port,
                        'mac': host_mac, 
                        'deviceId': device_id,
                        'ipAddresses': host_ip
        }
        result_host['hosts'].append(host_value)
    print("KET QUA CUOI")
    print(result_host)
call_host_api_sdn(['10.20.0.209'])