import requests
print("call flask")
response = requests.post("http://10.20.0.250:5000/getIpServer", data= '10.0.0.4')  
dest_ip = response.text
print(str(dest_ip) )

# import random
# list_ip = ['10.20.0.248', '10.20.0.251', '10.20.0.249', '10.20.0.243']
# print(random.sample(list_ip, 2)