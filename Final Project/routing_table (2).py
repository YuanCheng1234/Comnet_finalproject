
import sys 
from collections import deque
import numpy as np 
class Graph(): 
  
    def __init__(self, vertices): 
        self.V = vertices 
        self.graph = [[0 for column in range(vertices)] for row in range(vertices)] 
  
    def printSolution(self,dist,nodelist): 
        print "Vertex tDistance from Source"
        for node in range(self.V): 
            print nodelist[node], "t", dist[node] 
  
    # A utility function to find the vertex with  
    # minimum distance value, from the set of vertices  
    # not yet included in shortest path tree 
    def minDistance(self, dist, sptSet): 
  
        # Initilaize minimum distance for next node 
        min = sys.maxint 
  
        # Search not nearest vertex not in the  
        # shortest path tree 
        for v in range(self.V): 
            if dist[v] < min and sptSet[v] == False: 
                min = dist[v] 
                min_index = v 
  
        return min_index 
  
    # Funtion that implements Dijkstra's single source  
    # shortest path algorithm for a graph represented  
    # using adjacency matrix representation 
    def dijkstra(self, src, nodelist): 
  
        dist = [sys.maxint] * self.V 
        dist[src] = 0
        sptSet = [False] * self.V 
        neigh = [[None for i in range(mat_cols)] for j in range(mat_rows)]
  
        for cout in range(self.V): 
  
            # Pick the minimum distance vertex from  
            # the set of vertices not yet processed.  
            # u is always equal to src in first iteration 
            u = self.minDistance(dist, sptSet) 
  
            # Put the minimum distance vertex in the  
            # shotest path tree 
            sptSet[u] = True
  
            # Update dist value of the adjacent vertices  
            # of the picked vertex only if the current  
            # distance is greater than new distance and 
            # the vertex in not in the shotest path tree 
            for v in range(self.V): 
                if self.graph[u][v] > 0 and sptSet[v] == False and  dist[v] > dist[u] + self.graph[u][v]: 
                    dist[v] = dist[u] + self.graph[u][v] 
                    neigh[u][v] = nodelist[v]
  
        #self.printSolution(dist,nodelist) 
        return neigh

def dict_to_mat(graph,node_list):
    mat_graph = [[0 for i in range(len(node_list))] for j in range(len(node_list))]
    for i in range(0,len(nodes)):
        for j in range(0,len(nodes)):
            if(nodes[i] == nodes[j]):
                mat_graph[i][j] = 0
            elif(nodes[j] not in network[nodes[i]]):
                mat_graph[i][j]=0
            else:
                mat_graph[i][j]=1
    return mat_graph

def router_table(router,m_graph,nodes):
    print
    g = Graph(len(nodes))
    g.graph = mat_graph
    mat= g.dijkstra(router,nodes)
    print 'route for ' + nodes[router]
    for i in range(len(nodes)):
        stack = list()
        if(nodes[i] == nodes[router]):
            stack.append(i)
            route = []
            for k in range(len(stack)-1,-1,-1):
                route.append(nodes[(stack[k])])
            print 'destination: %s | path : %s | distance: %3d' %(nodes[i],route,len(stack)-1)
            continue
        stack.append(i)
        src_col = [sub[i] for sub in mat]
        while True:
           # src_col = mat[:,0]
            for j in range(len(src_col)):
                if src_col[j] is not None:
                    addr_index = j
                    stack.append(j)
                    break
            if nodes[j] == nodes[router]:
                break
            src_col = [sub[j] for sub in mat]

        route = []
        for k in range(len(stack)-1,-1,-1):
            route.append(nodes[(stack[k])])
        print 'destination: %s | path : %s | distance: %3d' %(nodes[i],route,len(stack)-1)



r1,r2,r3,r4,r5,r6,r7 = '192.168.4.2 (r1)','192.168.1.3 (r2)','192.168.2.3 (r3)','192.168.3.3 (r4)','192.168.1.2 (r5)','192.168.2.2 (r6)','192.168.3.2 (r7)'
h1,h2,h3 =  '192.168.1.1 (h1)','192.168.2.1 (h2)','192.168.3.1 (h3)'
src = '192.168.4.3 (src)'
routers = [r1,r2,r3,r4,r5,r6,r7]
hosts = [h1,h2,h3]
nodes = [src,r1,r2,r3,r4,r5,r6,r7,h1,h2,h3]

    
network = {src: {r1}, 
        r1: {src,r2, r3}, 
        r2: {r1,r4}, 
        r3:{r1,r5,r6},
        r4:{r2,r7},
        r5:{r3,h2}, 
        r6:{r3,h3}, 
        r7:{r4,h1}, 
        h1:{r7}, 
        h2:{r5}, 
        h3:{r6},}

mat_rows,mat_cols = (len(nodes), len(nodes))
mat_graph = [[0 for i in range(mat_cols)] for j in range(mat_rows)]
mat_graph = dict_to_mat(network,nodes)
for i in range(len(nodes)):
    router_table(i,mat_graph,nodes)














