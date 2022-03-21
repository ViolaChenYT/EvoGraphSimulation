
import random, math, string, sys
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_pydot import *

import random, math
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_pydot import *


GRAPH_SIZE = 10

ringgraph = [[(i-1)%GRAPH_SIZE, (i+1)%GRAPH_SIZE] for i in range(GRAPH_SIZE)]
stargraph = [[i for i in range(1,GRAPH_SIZE)]] + [[0] for _ in range(GRAPH_SIZE-1)]
wellmixed = []
for i in range(GRAPH_SIZE):
    neighbors = []
    for j in range(GRAPH_SIZE):
        if j!=i: neighbors.append(j)
    wellmixed.append(neighbors)
    
def newgraph(graph):
    G = nx.Graph()
    for i in range(len(graph)):
        for j in graph[i]:
            G.add_edge(i,j)
    return G

def visualize(G, name = ""):
    '''G: networkx graph'''
    nx.draw_networkx(G)
    if name != "":
        plt.savefig(name)
    else:
        plt.show()
        
model = sys.argv[1]
SAVE = True
if model == "star":
    G = newgraph(stargraph)
elif model == "ring":
    G = newgraph(ringgraph)
else:
    G = newgraph(wellmixed)
if SAVE:
    visualize(G, name=f"{model}graphvisual.jpg")
else:
    visualize(G)



