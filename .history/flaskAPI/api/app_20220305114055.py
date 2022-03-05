from flask import Flask, request

import sys, os
PATH_ABSOLUTE = "/home/onos/Downloads/flaskSDN/flaskAPI/"
IS_RUN_RRBIN = True


sys.path.append(PATH_ABSOLUTE+'model')
sys.path.append(PATH_ABSOLUTE+'handledata/models')
sys.path.append(PATH_ABSOLUTE+'core')
sys.path.append(PATH_ABSOLUTE+'routingAlgorithm')

# import from model
import params_model

# import from handledata/models 
import CusTopo

# import from core
import connectGraph, Graph

# import from routingAlgorithm
import destQueueRabbit, updateWeight, Round_robin, DijkstraLearning, connectGraph

# import inside folder
import pub
import apiSDN


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

pr

print(topo_network)


# get tap host va server tronng topo
hosts = topo_network.get_hosts()
servers = topo_network.get_servers()

if IS_RUN_RRBIN:
    print("Doc Queue 1 lan duy nhat")
    print(servers)
    # khoi tao queue co che Round robin
    queue_rr = destQueueRabbit.destQueueRabbit()

    # day tap server vao rabbit queue
    for ip in servers:
        queue_rr.connectRabbitMQ(ip_dest= ip)

# khoi tao bien CAP NHAP LINK COST
update = updateWeight.updateWeight()

@app.route('/getIpServer', methods=['POST'])
def get_ip_server():
  
  if request.method == 'POST':
    host_ip = request.data

    # chay thuat toan Round Robin 
    if IS_RUN_RRBIN:
        object = Round_robin.hostServerConnectionRR(queue_rr, topo_network, hosts, servers)
    # chay thuat toan Dinjkstra
    else:
        object = DijkstraLearning.hostServerConnection(topo_network, hosts, servers)

    # truyen ip xuat phat va lay ra ip server dich den
    object.set_host_ip(host_ip= str(host_ip))
    dest_ip = object.find_shortest_path()

  return str(dest_ip)

@app.route('/',  methods=['GET', 'POST'] )
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

    #  Khong chon data mac dinh
    if float(dicdata['byteSent']) > 556:
      
      # them du lieu vao rabbit de lay ra lien tuc
      pub.connectRabbitMQ( data = dicdata )

      # them du lieu vao MONGO de theo doi ve sau
      params_model.insert_data(dicdata)

      # doc data tu rabbit lien tuc
      update.read_params_from_rabbit()

      # Doc duoc 100 du lieu tu rabbit
      if update.get_count() == 100: 
          app.logger.info("Da nhan dc 100 du lieu tu rabbit")

          # viet trong so moi ra Mongo
          update.write_update_data_base()

          # reset bien doc du lieu
          update.set_count(count = 0)

    return content

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
  
    

   

   