import heapq as hq

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


def YenKSP(G, source, sink, K=3):
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
        
    paths = [A[k][0] for k in range(len(A))]
    weights = [A[k][1] for k in range(len(A))]

    return paths, weights