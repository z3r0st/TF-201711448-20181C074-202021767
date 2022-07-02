from perlin_noise import PerlinNoise

def timeFactor(time):
    timeToTraffic = [(1, 1.5), (1, 1.3), (1, 1.1), (1, 1.2), (1, 1.5), (1, 2), (1.1, 3.2), (1.5, 5.5), 
               (1.3, 4), (1, 2.5), (1, 2), (1.1, 2.8), (1.3, 4), (1.4, 4.1), (1.1, 3), (1.1, 2.5), 
               (1.1, 2.6), (1.3, 4), (1.5, 5.2), (1.5, 5.5), (1.1, 4.4), (1, 2.2), (1, 2), (1, 1.6)]
    
    return timeToTraffic[int(time[:2])]


def addTraffic(G, nodeToIntercept, time):
    noise = PerlinNoise(octaves=3.5, seed=777)

    tMin, tMax = timeFactor(time)
    for u in range(len(G)):
        for i in range(len(G[u])):
            v, w = G[u][i]
            lon, lat = map(lambda c1, c2: 10*(c1+c2)/2, nodeToIntercept[u], nodeToIntercept[v])
            zoneFactor = noise([lon, lat]) + 0.707
            def linearRescale(x, l, r):
                return x*(r - l)/(0.707 - -0.707) # E [-0.707, 0.707]
            zoneFactor = linearRescale(zoneFactor, tMin, tMax)
            # convert to int because < 1m is a negligible value
            G[u][i][1] = int(w * (tMin + zoneFactor))