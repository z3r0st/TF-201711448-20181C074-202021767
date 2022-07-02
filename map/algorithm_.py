import requests #pip install requests
import math
import matplotlib.pyplot as plt #pip install matplotlib
from perlin_noise import PerlinNoise #pip install perlin_noise
import heapq as hq
import json

url = "https://raw.githubusercontent.com/z3r0st/TF-201711448-20181C074-202021767/main/SF_street_intersections.csv"
file = requests.get(url).content
f = file.decode('utf-8')

data = f.split(sep='\n')[1:]
intercepts = dict()
streets = dict()
nodes = dict()
nodeToIntercept = dict()
c = 0
for line in data:
    if(len(line) == 0):
        continue
    street, point = line.split(sep=',')[1:3]
    lon, lat = point[7:-2].split()
    intercept = (float(lat), float(lon))
    if street in intercepts.keys():
        intercepts[street].append(intercept)
    else:
        intercepts[street] = [intercept]
    if intercept in streets.keys():
        streets[intercept].append(street)
    else:
        streets[intercept] = [street]
        nodes[intercept] = c
        nodeToIntercept[c] = intercept
        c += 1

def toRadians(valor):
  return (math.pi/180.0)*valor

def calculateDistance(intercept1, intecerpt2):
    Lat1, Lon1 = intercept1
    Lat2, Lon2 = intecerpt2
    difLat = toRadians(Lat2 - Lat1)
    difLon = toRadians(Lon2 - Lon1)

    a = math.sin(difLat/2)**2 + math.cos(toRadians(Lat1))*math.cos(toRadians(Lat2))*(math.sin(difLon/2))**2
    c = 2*math.atan2(math.sqrt(a),math.sqrt(1-a))

    return  6371000.0*c

def createGraph(streets, intercepts, nodes):
    G = [[] for i in range(len(streets.keys()))]
    
    for intercept in streets.keys():
        for street in streets[intercept]:
            neighbours = []
            for point in intercepts[street]:
                if point != intercept:
                    neighbours.append([point, calculateDistance(intercept, point)])
            
            if len(neighbours) > 1:
                neighbours.sort(key=lambda ls: ls[1])
                neighbours = neighbours[0:2]
                if calculateDistance(neighbours[0][0], neighbours[1][0]) < neighbours[1][1]:
                    neighbours.pop()
                
                G[nodes[intercept]].extend([[nodes[neighbours[x][0]], neighbours[x][1]] for x in range(len(neighbours))])
                
            elif len(neighbours) > 0:
                G[nodes[intercept]].append([nodes[neighbours[0][0]], neighbours[0][1]])
    
    return G

G_al = createGraph(streets, intercepts, nodes)
def writing():
    f = open("weighted_graph.al", "w")
    f.write(str(len(G_al))+'\n')
    c = 0
    for line in G_al:
        f.write(str(c)+' ')
        if len(line) > 0:
            for x, y in line:
                f.write(str(x)+','+str(y)+' ')
        else:
            f.write('-')
        f.write('\n')
        c += 1

def reading():
    with open("weighted_graph.al", "r") as f:
        n = int(f.readline().strip())
        G = [[] for _ in range(n)]
        
        for line in f:
            line = line.strip().split()
            u = int(line[0])
            for pair in line[1:]:
                G[u].append([int(v), float(w)] for v, w in pair.split(sep=','))


noise = PerlinNoise(octaves=3.5, seed=777)
def timeFactor(time):
    timeToTraffic = [(1, 1.5), (1, 1.3), (1, 1.1), (1, 1.2), (1, 1.5), (1, 2), (1.1, 3.2), (1.5, 5.5), 
               (1.3, 4), (1, 2.5), (1, 2), (1.1, 2.8), (1.3, 4), (1.4, 4.1), (1.1, 3), (1.1, 2.5), 
               (1.1, 2.6), (1.3, 4), (1.5, 5.2), (1.5, 5.5), (1.1, 4.4), (1, 2.2), (1, 2), (1, 1.6)]
    
    return timeToTraffic[int(time[:2])]

def addTraffic(G, nodeToIntercept, time):
    tMin, tMax = timeFactor(time)
    for u in range(len(G)):
        for i in range(len(G[u])):
            v, w = G[u][i]
            lat, lon = map(lambda c1, c2: 10*(c1+c2)/2, nodeToIntercept[u], nodeToIntercept[v])
            zoneFactor = noise([lat, lon]) + 0.707
            def linearRescale(x, l, r):
                return x*(r - l)/(0.707 - -0.707) # E [-0.707, 0.707]
            zoneFactor = linearRescale(zoneFactor, tMin, tMax)
            # convert to int because < 1m is a negligible value
            G[u][i][1] = int(w * (tMin + zoneFactor))

addTraffic(G_al, nodeToIntercept, "19:38:29")

def dijkstra(G, source, sink=None, parent=None):
    n = len(G)
    if parent is None: parent = [None]*n
    heap = [(0, source, None)]
    
    while heap:
        c, u, p = hq.heappop(heap)
        
        if parent[u] is not None: continue
            
        parent[u] = (p, c)
        
        if sink and u == sink:
            path = [u]
            cost = [parent[u][1]]
            while(u != source):
                u = parent[u][0]
                path.append(u)
                cost.append(parent[u][1])
            
            for i in range(len(cost)-1):
                cost[i] -= cost[i+1]
            path.reverse()
            cost.reverse()
            return [path, cost]
        
        for v, w in G[u]:
            if parent[v] is None and w > 0:
                hq.heappush(heap, (c + w, v, u))

def YenKSP(G, source, sink, K=0):
    A = [[] for _ in range(K)]
    A[0] = dijkstra(G, source, sink)
    B = []
    
    if A[0] is None: return A
    
    for k in range(K-1):
        for i in range(len(A[k][0]) - 1):
            parent = [None]*len(G)
            
            spurNode = A[k][0][i]
            rootPath = [A[k][0][:i+1], A[k][1][:i+1]]
#             print(f"i={i}", A, rootPath, sep='\n')
            
            disabledEdges = []
            for path in A+B:
                if path == []: continue
                if path[0][:i+1] == rootPath[0]:
                    u = path[0][i]
                    for j in range(len(G[u])):
                        v, w = G[u][j]
                        if v == path[0][i+1] and w != 0: 
                            disabledEdges.append((u, j, w))
                            G[u][j][1] = 0
            
            for node in rootPath[0][:-1]:
                parent[node] = -1
            
            spurPath = dijkstra(G, spurNode, sink, parent)
            
            for u, j, w in disabledEdges:
                G[u][j][1] = w
            
            if spurPath is None: continue
            
            totalPath = spurPath if i == 0 else [rootPath[0] + spurPath[0][1:], rootPath[1] + spurPath[1][1:]]
            B.append(totalPath)
            
        if B == []: break
        
        B = sorted(B, key=lambda b: sum(b[1]))
#         print("Weights -> {k} iteration:", [sum(b) for a, b in B], sep='\n')
        A[k+1] = B.pop(0)
        
    return A

##User interface
G = G_al
Loc = [nodeToIntercept[u] for u in range(len(G))]
def graph():
    response = {"loc": Loc, "g": G}

    return json.dumps(response)
def paths():
    return ""