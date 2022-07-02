import requests
import distance as dis
import traffic


def load_data(url):
    file = requests.get(url).content
    f = file.decode('utf-8')

    data = f.split(sep='\n')[1:]
    intercepts = dict()
    streets = dict()
    nodes = dict()
    Loc = []
    c = 0

    for line in data:
        if(len(line) == 0):
            continue
        street, point = line.split(sep=',')[1:3]
        lon, lat = point[7:-2].split()
        intercept = (float(lon), float(lat))
        if street in intercepts.keys():
            intercepts[street].append(intercept)
        else:
            intercepts[street] = [intercept]
        if intercept in streets.keys():
            streets[intercept].append(street)
        else:
            streets[intercept] = [street]
            nodes[intercept] = c
            Loc.append(intercept)
            c += 1
    
    return nodes, Loc, streets, intercepts


def create_graph(url):
    nodes, Loc, streets, intercepts = load_data(url)

    G = [[] for i in range(len(streets.keys()))]
    
    for intercept in streets.keys():
        for street in streets[intercept]:
            neighbours = []
            for point in intercepts[street]:
                if point != intercept:
                    neighbours.append([point, dis.calculateDistance(intercept, point)])
            
            if len(neighbours) > 1:
                neighbours.sort(key=lambda ls: ls[1])
                neighbours = neighbours[0:2]
                if dis.calculateDistance(neighbours[0][0], neighbours[1][0]) < neighbours[1][1]:
                    neighbours.pop()
                
                G[nodes[intercept]].extend([[nodes[neighbours[x][0]], neighbours[x][1]] for x in range(len(neighbours))])
                
            elif len(neighbours) > 0:
                G[nodes[intercept]].append([nodes[neighbours[0][0]], neighbours[0][1]])
    
    return G, Loc

def create_graph_with_traffic(graph, locations, time):
    G = load_graph(graph)
    Loc = load_locations(locations)
    traffic.addTraffic(G, Loc, time)

    return G, Loc



def write_graph_al(path, G):
    f = open(path, "w")
    f.write(str(len(G))+'\n')
    n, c = len(G), 0
    for line in G:
        f.write(str(c)+' ')
        if len(line) > 0:
            for v, w in line:
                f.write(f"{v:.0f},{w:.0f} ")
        else:
            f.write('-')
        if c < n - 1: f.write('\n')
        c += 1


def load_graph(path):
    with open(path, "r") as f:
        n = int(f.readline().strip())
        G = [[] for _ in range(n)]
        c=0
        for line in f:
            c += 1
            line = line.strip().split()
            u = int(line[0])
            if line[1] == '-': continue
            for pair in line[1:]:
                v, w = pair.split(sep=',')
                G[u].append([int(v), int(w)])
    return G


def write_locations(path, Loc):
    f = open(path, "w")
    f.write(f"{len(Loc)}\n")
    n, c= len(Loc), 0
    
    for lon, lat  in Loc:
        f.write(f"{lon},{lat} ")
        if c < n - 1: f.write('\n')
        c += 1


def load_locations(path):
    with open(path, "r") as f:
        n = int(f.readline().strip())
        Loc = []
        
        for line in f:
            lon, lat = line.strip().split(',')
            Loc.append((float(lon), float(lat)))

    return Loc


G, Loc= create_graph("https://raw.githubusercontent.com/z3r0st/TF-201711448-20181C074-202021767/main/SF_street_intersections.csv")

write_graph_al("san_francisco_streets.al", G)
write_locations("coordinates.txt", Loc)


