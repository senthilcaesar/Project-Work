import math
class ShortestPath:
    
    def __init__(self):
        self.edges = {}
        self.weights = {}
        
    def add_vertex(self, v):
        self.edges[v] = []
        
    def add_edge(self, from_v, to_v, distance):
        self.edges[from_v].append(to_v)
        self.weights[(from_v, to_v)] = distance
        
    def print_edges(graph):
        print("Adjacency List")
        for key in graph.edges:
            print(key, end=" ")
            for neighbor in graph.edges[key]:
                print(neighbor, end=" ")
            print()       
        
    def dijkstra(self, weight, start):
        ''' Contians the set of vertices we know the shortest paths already '''
        graph = self
        S = set()
        delta = {}
        parent = {}
        short = []
        ''' set of vertices that need to be processed '''
        queue = list(graph.edges.keys())
        for v in queue:
            delta[v] = math.inf       
        delta[start] = 0
        while len(delta) > 0:
            u = min(delta, key=delta.get)
            S.add(u)
            ''' Relax Edges '''
            for v in graph.edges[u]:
                new_path = delta[u] + graph.weights[u, v]
                if delta[v] > new_path:
                    delta[v] = new_path
                    parent[v] = u           
            tup = (u, delta[u])
            short.append(tup)
            del delta[u]
        return parent, short
    
g = ShortestPath()
g.add_vertex('a')
g.add_vertex('b')
g.add_vertex('c')
g.add_vertex('d')
g.add_vertex('e')
g.add_edge('a', 'c', 8)
g.add_edge('a', 'b', 2)
g.add_edge('a', 'd', 5)
g.add_edge('b', 'c', 1)
g.add_edge('d', 'e', 4)
g.add_edge('c', 'e', 3)
parent, short = g.dijkstra(g.weights, 'a')

''' Print Shortest Path '''
for key in parent:
    value = parent[key]
    for i in range(0, len(short)):
        if short[i][0] == key:
            distance = short[i][1]
    print(distance, key, value, end=" ")
    for edges in parent:
        if value in parent:
            print(parent[value], end=" ")
        try:
            value = parent[value]
        except KeyError:
            pass
    print()
