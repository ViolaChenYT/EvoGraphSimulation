import sys
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_pydot import *
from networkx.generators.random_graphs import *


# g = nx.generators.random_graphs.erdos_renyi_graph(n, p)
g = random_regular_graph(3, 100)
nx.draw(g,with_labels=True, font_weight='bold')
plt.show()

'''networkx.generators.random_graphs.powerlaw_cluster_graph
powerlaw_cluster_graph(n, m, p, seed=None)[source]
Holme and Kim algorithm for growing graphs with powerlaw degree distribution and approximate average clustering.

Parameters
nint
the number of nodes
mint
the number of random edges to add for each new node
pfloat,
Probability of adding a triangle after adding a random edge
seedinteger, random_state, or None (default)
Indicator of random number generation state. See Randomness.
'''