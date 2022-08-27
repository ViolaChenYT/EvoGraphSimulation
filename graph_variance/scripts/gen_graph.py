import sys
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from queue import *

N = 100

def gen_basics():
  if len(sys.argv) < 4:
    print("please key in name, n_nodes, graph_type")
    raise Exception("InvalidInput")
  else:
    name = sys.argv[1]
    n_nodes = int(sys.argv[2])
    graph_type = sys.argv[3]
    g = nx.Graph()
    if graph_type == 'star':
      for i in range(1, n_nodes):
        g.add_edge(0, i)
    elif graph_type == "ring":
      for i in range(n_nodes):
        g.add_edge(i, (i+1)%n_nodes)
    elif graph_type in ["complete", "wellmixed"]:
      for i in range(n_nodes):
        for j in range(i+1, n_nodes):
          g.add_edge(i,j)
    elif graph_type == 'reg':
      g = nx.random_regular_graph(3, n_nodes)
    else:
      # gen random graph
      g = nx.generators.random_graphs.erdos_renyi_graph(n_nodes, 0.1)
    nx.write_edgelist(g, f"./graphs/{name}.txt", data=False)
    
def gen_wheel_reg(n=100):
  output_dir = sys.argv[1]
  for i in range(n):
    g = nx.Graph()
  
    nx.write_edgelist(g,f"./{output}/{i}.txt")
  print("Done!")

def gen_tree_like(d = 4, branch = 2, link = 2):
  output_dir = sys.argv[1]
  idx = 0
  for size in range(5, 11):
    for i in range(10, 60): # root cluster
      cnt = i + 1
      queue = SimpleQueue()
      G = nx.random_regular_graph(d, cnt)
      queue.put(cnt-1)
      while cnt + size <= N:
        prev_head = queue.get()
        for j in range(branch):
          new_clique = nx.random_regular_graph(d, size)
          mapping = dict(zip(new_clique, range(cnt, cnt+size)))
          new_clique = nx.relabel_nodes(new_clique, mapping)
          G = nx.compose(G, new_clique)
          for k in range(link):
            G.add_edge(prev_head-j-k, cnt+k) # the bridges
          cnt += size
          queue.put(cnt-1)
      for node in range(cnt, N):
        G.add_edge(cnt-1, node)
      nx.write_edgelist(G,f"./{output_dir}/{idx}.txt",data=False)
      # nx.draw_networkx(G)
      # plt.show()
      idx += 1
  print("Done!")

def gen_identical(e_inter=1):
  output_dir = sys.argv[1]
  # for degree in range(3, 49):
  #   g = nx.random_regular_graph(degree,50)
  #   el = np.array(g.edges) + 50
  #   g.add_edges_from(el)
  #   g.add_edges_from([(j, 50 + j) for j in range(e_inter)])
  #   nx.write_edgelist(g,f"./{output_dir}/{degree}.txt",data=False)
  cnt = 0
  for degree in range(3,8):
    for i in range(10,90,2): # every 40
      g = nx.random_regular_graph(degree,i)
      el = np.array(nx.random_regular_graph(degree,100-i).edges) + i
      g.add_edges_from(el)
      g.add_edges_from([(j, 50 + j) for j in range(e_inter)])
      
      nx.write_edgelist(g,f"./{output_dir}/{cnt}.txt",data=False)
      cnt += 1

def gen_alt_detour():
  output_dir = sys.argv[1]
  cnt = 0
  for interval in range(2, 49):
    g = nx.complete_graph(50)
    g.add_edges_from([(i, i+1) for i in range(50,99)])
    g.add_edge(0,50)
    g.add_edge(1,99)
    g.add_edges_from([(50+i, 50 + (i+interval)%50 ) for i in range(49)])
    print(nx.transitivity(g))
    nx.write_edgelist(g,f"./{output_dir}/{cnt}.txt",data=False)
    cnt += 1
    

if __name__ == '__main__':
  # gen_myisland()
  # gen_tree_like()
  # gen_identical()
  gen_alt_detour()