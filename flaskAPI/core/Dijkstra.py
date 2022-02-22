import heapq

class Dijkstra(object):
    """Dijktra shortest path algorithm"""
    def __init__(self, topo, start, end):
       """
       topo: Custopo object hold network
       start: starting node object
       end: ending node object
       nodes: list of node object
       edges: dictionary of edge object
       """
       self.topo = topo
       self.nodes = topo.get_nodes()
       self.edges = topo.get_edges()
       self.start = start
       self.end = end

       self.distance = dict()  # minimum distance from start to each node in shortest path
       self.path = dict()   # parent of each node in shortest path
       self.minimum_cost = 0
       self.result = [] # tap cac canh di tu start den end
       self.heap = []

       self.routing_preparation()

    def set_start(self, start):
         self.start = start

    def set_end(self, end):
        self.end = end

    def get_distance(self):
        return self.distance

    def get_path(self):
        return self.path

    def get_result(self):
        return self.result

    def get_minimum_cost(self):
        return self.minimum_cost

    def routing_preparation(self):
       # neu tap ket qua khong rong thi reset lai
       if self.result:
            self.reset_route()

       # khoi tao cac gia tri ban dau
       for node in self.nodes:
            self.distance[node] = (0 if node == self.start else float('inf') )
            self.path[node] = None    

    def reset_route(self):
       self.distance = dict()  
       self.path = dict()  
       self.minimum_cost = 0
       self.result = []
       self.heap = []

    def routing(self):  
        self.routing_preparation()
        self.heap = [ (0, self.start) ]  # cost from start node
        visited = set()

        while self.heap:
            (current_cost, u) = heapq.heappop(self.heap)
    
            if u in visited:
                continue
            visited.add(u)

            if u.get_id() == self.end.get_id():
                self.minimum_cost = current_cost
                # backtrack to save shortest path
                self.save_result()
                return 
                
            for v, c, edge_address in self.edges[u]:
                #print("vertex", v, "cost", v)
                if v not in visited and current_cost + c < self.distance[v]:
                    next = current_cost + c
                    self.path[v] = u  # parent of v is u
                    self.distance[v] = next # update new distance
                    heapq.heappush(self.heap, (next, v))
        return -1
  
    def save_result(self):
        current = self.end
        
        while current != self.start:
            parent = self.path[current]
            edge_object = self.topo.find_edge(src= parent, dest = current)

            weight = edge_object[1] # access weight in list
            self.result.append( edge_object[2] ) # access edge address in list
            current = parent

        # reverse result
        self.result = self.result[::-1]

    def __str__(self):
        for e in self.result:
            print("from", e.get_src().get_id(), "->", e.get_dest().get_id(), 
                    " = ", e.get_weight() )
        return "OK"

