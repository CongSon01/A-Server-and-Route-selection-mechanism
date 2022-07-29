import networkx
import set_up_mininet
import numpy as np

#Domain Controller

#Cogentco
#Cesnet200706
#VtlWavenet2011
graph = networkx.read_graphml("/home/onos/Downloads/topologyzoo/"+"Dataxchange"+".graphml")
nodes_graph = graph.nodes()
edges = [[ "s"+str(int(edge[0].replace("n", ""))+1),  "s"+str(int(edge[1].replace("n", ""))+1)] for edge in graph.edges()] 
hosts_graph = ['h'+str(n+1) for n in range(len(nodes_graph))]
switches_graph = ['s'+str(n+1) for n in range(len(nodes_graph))]

n = len(switches_graph)
Matrix_graph = [[0 for x in range(n)] for y in range(n)]


for edge in edges:
    Matrix_graph[int(edge[0].replace("s", ""))-1][int(edge[1].replace("s", ""))-1] = 1
    Matrix_graph[int(edge[1].replace("s", ""))-1][int(edge[0].replace("s", ""))-1] = 1
    
np.savetxt('graph_matrix.txt',Matrix_graph, fmt='%s')