white = 0
gray = 1
black = 2

class Graph:
    
    def __init__(self):
        ''' Construct empty graph '''
        self.edges = {}
        
    def addVertex(self, v):
        ''' List of nodes that are not connected yet '''
        if v not in self.edges:
            self.edges[v] = []
            
    def addEdge(self, from_v, to_v):

        ''' Connected the vertices by edges '''
        if from_v not in self.edges:
            self.edges[from_v] = []
        if to_v not in self.edges:
            self.edges[to_v] = []
        
        ''' Adding neighboring vertex if not already present in the neighboring list '''
        if to_v not in self.edges[from_v]:
            self.edges[from_v].append(to_v)
        if from_v not in self.edges[to_v]:
            self.edges[to_v].append(from_v)           
    
    def isEdge(self, from_v, to_v):
        
        if to_v not in self.edges:
            return False
        if from_v not in self.edges:
            return False
        return to_v in self.edges[from_v]        
        
    def loadGraph(self, graph):
        for vertice in graph:
            for edge in graph[vertice]:
                self.addEdge(vertice, edge)

class DepthFirstTraversal:
        
    def __init__(self, graph, s):
        ''' Inititate a DFS traversal of graph '''
        self.graph = graph
        self.start = s
        self.color = {}
        self.parent = {}
        
        for v in graph.edges:
            self.color[v] = white
            self.parent[v] = None
            
        self.dfs_visit(s)
        
    def dfs_visit(self, u):
        ''' Recursive traversal '''
        self.color[u] = gray
        
        for v in self.graph.edges[u]:
            if self.color[v] is white: 
                self.parent[v] = u
                self.dfs_visit(v)
        # vertex is totally exposed      
        self.color[u] = black
        
    def solution(self, v):
        # Recover path from start to this vertex v        
        if v not in self.graph.edges:
            return None
        # Check for disconnected vertex
        if self.parent[v] is None:
            return None
        
        path = [v]       
        while v != self.start:
            v = self.parent[v]
            path.insert(0, v)
            
        return path
                            
simple = {1: [2, 3, 5],
          2: [1, 4],
          3: [1],
          4: [2, 5],
          5: [1, 4]}     
        
g = Graph()
g.loadGraph(simple)
dfs = DepthFirstTraversal(g, 3)
path = dfs.solution(5)
print(path)       
