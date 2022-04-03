from flask import Flask, request, Response, jsonify


import sys, os, json
PATH_ABSOLUTE = "/home/onos/Downloads/flask_SDN/Flask-SDN/flaskAPI/"
IS_RUN_RRBIN = False

sys.path.append(PATH_ABSOLUTE+'model')
sys.path.append(PATH_ABSOLUTE+'handledata/models')
sys.path.append(PATH_ABSOLUTE+'core')
sys.path.append(PATH_ABSOLUTE+'routingAlgorithm')

# import from model
import Params, LinkVersion

# import from handledata/models 
import CusTopo

# import from core
import connectGraph, Graph

# import from routingAlgorithm
import destQueueRabbit, DijkstraLearning, Round_robin, updateServerCost, updateWeight

# import inside folder
import pub
import apiSDN
import time
import requests

# Init app
app = Flask(__name__)

# goi api tu cac SDN 
apiSDN.call_topo_api_sdn_1()
apiSDN.call_topo_api_sdn_2()
apiSDN.call_host_api_sdn_1()
apiSDN.call_host_api_sdn_2()

topo_path_1 = PATH_ABSOLUTE + 'topo_1.json'
topo_path_2 = PATH_ABSOLUTE + 'topo_2.json'
host_path_1 = PATH_ABSOLUTE + 'host_1.json'
host_path_2 = PATH_ABSOLUTE + 'host_2.json'
topo_files = [topo_path_1, topo_path_2]
host_files = [host_path_1, host_path_2]
# sinh ra file hop nhat giua cac mang: topo.json va host.json 
connectGraph.connectGraph(topo_files, host_files)

# khoi tao topo rong
topo_network = CusTopo.Topo()
# add do thi topo.json va host.json vao topo
graph = Graph.Graph(topo_network, 'topo.json', 'host.json')


#print(topo_network.get_topo(), "\n")
# get tap host va server tronng topo
hosts = topo_network.get_hosts()
servers = topo_network.get_servers()
print(hosts)
print(servers)

if IS_RUN_RRBIN:
    print("Doc Queue 1 lan duy nhat")
    print(servers)
    # khoi tao queue co che Round robin
    queue_rr = destQueueRabbit.destQueueRabbit()

    # day tap server vao rabbit queue
    for ip in servers:
        queue_rr.connectRabbitMQ(ip_dest= ip)

# khoi tao bien CAP NHAP SERVER COST
update_server = updateServerCost.updateServerCost(servers)
# khoi tao bien CAP NHAP LINK COST
update = updateWeight.updateWeight(topo= topo_network)
# uu tien flow rule theo thu tu tu dau den cuoi
priority = 200

starttime = time.time()
# def get_BW_from_server(file_name, name_host):
#     results = []
#     with open(file_name) as file_in:
#         for line in file_in:
#             list_col = line.split()
#             if list_col[0] == '[SUM]':
#                 # new_df = { 'Transfer': list_col[4], 'Bandwidth': list_col[6], 'Jitter': list_col[8], 'Lost': list_col[10],'Total': list_col[9], 'Datagrams': list_col[10] }
#                 # print(list_col)
#                 # if list_col[0][-1] == '-':
#                 if len(list_col) == 13:
#                     results.append( {"NameHost":name_host,"Bandwidth":float(list_col[6])})
#                     # new_df =  [float(list_col[4]), float(list_col[6]), float(list_col[8]), float(list_col[10][:-1]), float(list_co[11]), float(list_col[12][1:-2]) ]
#                 elif len(list_col) == 12:
#                     results.append( {"NameHost":name_host,"Bandwidth":float(list_col[5])})
#                     # new_df = [float(list_col[3]), float(list_col[5]), float(list_col[7]),  float(list_col[9][:-1]), float(list_co[10]), float(list_col[11][1:-2])]
#                 else:
#                     continue
#         return results

      
@app.route('/getIpServer', methods=['POST'])
def get_ip_server():
  
  if request.method == 'POST':
    host_ip = request.data
    global priority 
    priority +=1

    # chay thuat toan Round Robin 
    if IS_RUN_RRBIN:
        object = Round_robin.hostServerConnectionRR(queue_rr, topo_network, hosts, servers, priority)
    # chay thuat toan Dinjkstra
    else:
        object = DijkstraLearning.hostServerConnection(topo_network, hosts, servers, priority)

    # truyen ip xuat phat va lay ra ip server dich den
    object.set_host_ip(host_ip= str(host_ip))
    dest_ip = object.find_shortest_path()

  return str(dest_ip)

@app.route('/write_data/',  methods=['GET', 'POST'] )
def write_data():
  
  if request.method == 'GET':
    return "Da nhan duoc GET"

  if request.method == 'POST':
    #app.logger.info("Da nhan dc POST")
    # get data from API
    content = request.data
    dicdata={}
    datas=content.split("&")

    # processing data
    for data in datas:
      d=data.split(":")
      if len(d) == 3:
        temp = [ d[1], d[2] ]
        dicdata[ d[0] ] = ":".join(temp)
      else:
        dicdata[ d[0] ] = d[1] 
    # print( "nhan data", dicdata['byteSent'] )
    
    #  Khong chon data mac dinh
    # if float(dicdata['byteSent']) > 600:
    # print( "--------nhan data onos-------------", dicdata['byteSent'] )

      # version = params_model.count_link_version(dicdata['src'], dicdata['dst'])

      
      # dicdata['link_version'] = version + 1

      # them du lieu vao rabbit de lay ra lien tuc
    pub.connectRabbitMQ( data = dicdata )

      # doc data tu rabbit lien tuc
    update.read_params_from_rabbit()


      # # Cap nhat lai version trong bang version
      # if link_version != None:
      #   link_version.insert_data({"version":1})
      # else:
      #   if version + 1 > link_version.get_version_max():
      #     link_version.insert_data({"version":version + 1})

    global starttime
    if time.time() - starttime > 5: 
          # app.logger.info("Da nhan dc 100 du lieu tu rabbit")
          # app.logger.info("Cap nhat sau 10s")
          # print(LinkVersion.get_multiple_data())
          
          # Doc R ong
          try:
              data_250 = requests.get("http://10.20.0.248:5000/read_link_version/") 

              LinkVersions = data_250.text
              update.write_update_link_to_data_base(LinkVersions)
              # print(data_250.text)
          except:
            print("Doc data loi")
          
          # Ghi W ong
          try:
              response = requests.post("http://10.20.0.250:5000/write_link_version/", data= dicdata)
          except:
              print("Goi nhieu SDN loiiiiiiiiiiiiiiiiiiiii")


          # viet trong so moi ra Mongo

          

          # cap nhap trong so cho server
          # update_server.update_server_cost()

              # them data vao MONGO o moi SDN de theo doi ve sau
          # params_model_248.insert_data(dicdata) # DB may 248
          # Params.insert_data(dicdata) # DB may 250
          # Params.insert_data(dicdata) # DB may 250


          






          # viet trong so moi ra Mongo
          # update.write_update_link_to_data_base()

          # cap nhap trong so cho server
          update_server.update_server_cost()

          # global update
          # # reset
          # update = updateWeight.updateWeight()

          # reset bien doc du lieu
          #update.set_count(count = 0)
          starttime = time.time()

# # print str after 2 minutes
# print('start time: ' + str(starttime))

# if time.time() - starttime > 120:
#     print("Time out")
# print('end time: ' + str(time.time()))

      # Doc duoc 100 du lieu tu rabbit 
      # if update.get_count() == 100: 
    return content

@app.route('/write_link_version/',  methods=['GET', 'POST'] )
def write_link_version():
  if request.method == 'POST':
    #app.logger.info("Da nhan dc POST")
    # get data from API
    content = request.data
    print(content)
    LinkVersion.insert_data(content)

@app.route('/read_link_version/',  methods=['GET', 'POST'] )
def read_link_version():
  if request.method == 'GET':
    data = LinkVersion.get_multiple_data()
    return jsonify({'link_versions':data})  #will return the json
    # return Response(json.dumps(data),  mimetype='application/json')

if __name__ == '__main__':
    app.run(host='10.20.0.248',debug=True, use_reloader=False)
   