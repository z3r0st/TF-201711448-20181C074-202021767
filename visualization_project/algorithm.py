import json
import random as r
import math
import heapq as hq
import main
import paths as path_finding
from perlin_noise import PerlinNoise

# python -m pip install requests
G, Loc= main.create_graph_with_traffic("san_francisco_streets.al", "coordinates.txt", "19:38:29")


def graph():
    return json.dumps({"loc": Loc, "g": G})


def paths(s, t):
    paths, _ = path_finding.YenKSP(G, 0, 8823, 3)

    return json.dumps({"bestpath": paths[0], "path1": paths[1], "path2": paths[2]})
