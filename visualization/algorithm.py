import json
import random as r
import math
import heapq as hq
import main
import paths as path_finding
from perlin_noise import PerlinNoise

# python -m pip install requests
G, Loc= main.create_graph_with_traffic("san_francisco_streets.al", "coordinates.txt", "09:38:29")


def graph():
    return json.dumps({"loc": Loc, "g": G})


def paths(s, t):
    tuple = path_finding.YenKSP(G, s, t, 3)
    paths, _ = tuple

    n = len(G)
    parents = [[-1]*n, [-1]*n, [-1]*n]
    
    for i in range(len(paths)):
      for j in range(1, len(paths[i])):
        parents[i][paths[i][j]] = paths[i][j-1]

    return json.dumps({"bestpath": parents[0], "path1": parents[1], "path2": parents[2]})
