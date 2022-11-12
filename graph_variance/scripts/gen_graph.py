import sys, os
import networkx as nx
import numpy as np
import random
import matplotlib.pyplot as plt
from queue import *
import copy

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

def gen_diff_size_same_deg(e_inter=1):
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
  cnt = 0
  
def gen_diff_deg():
  output_dir = sys.argv[1]
  cnt=0
  for degree in range(3, 49):
    g = nx.random_regular_graph(degree,50)
    el = np.array(nx.random_regular_graph(50-degree, 50).edges) + 50
    g.add_edges_from(el)
    g.add_edges_from([(j, 50 + j) for j in range(2)])
    nx.write_edgelist(g,f"./{output_dir}/{cnt}.txt",data=False)
    cnt += 1

def gen_alt_detour():
  output_dir = sys.argv[1]
  cnt = 0
  base = nx.random_regular_graph(3, 50)
  for interval in range(2, 49):
    g = copy.deepcopy(base)
    g.add_edges_from([(i, i+1) for i in range(50,99)])
    g.add_edge(0,50)
    g.add_edge(1,99)
    g.add_edges_from([(50+i, 50 + ((i+interval)%50) ) for i in range(49)])
    # print(interval)
    # print(nx.transitivity(g))
    nx.draw_networkx(g)
    # plt.show()
    nx.write_edgelist(g,f"./{output_dir}/{cnt}.txt",data=False)
    cnt += 1
    
def gen_very_regular():
  output_dir = sys.argv[1]
  cnt = 0
  for i in range(100):
    g = nx.complete_graph(50)
    el = np.array(nx.random_regular_graph(3, 50).edges) + 50
    g.add_edges_from(el)
    g.add_edges_from([(j, 50 + j) for j in range(2)])
    nx.write_edgelist(g,f"./{output_dir}/{cnt}.txt",data=False)
    cnt += 1
    
def gen_many_bridges(): # Sept 14 2022
  output_dir = sys.argv[1]
  cnt=0
  el = np.array(nx.random_regular_graph(3, 50).edges) + 50
  for i in range(1,50):
    g = nx.complete_graph(50)
    g.add_edges_from(el)
    g.add_edges_from([(0, 50 + j) for j in range(i)]) 
    # the way bridges are added can be further modified
    nx.write_edgelist(g,f"./{output_dir}/{cnt}.txt",data=False)
    cnt += 1
  for i in range(1,50):
    g = nx.complete_graph(50)
    g.add_edges_from(el)
    g.add_edges_from([(j, 50) for j in range(i)]) 
    # the way bridges are added can be further modified
    nx.write_edgelist(g,f"./{output_dir}/{cnt}.txt",data=False)
    cnt += 1

def gen_star_regular():
  output_dir = sys.argv[1]
  cnt=0
  satellites = [i for i in range(1,50)]
  el = np.array(nx.random_regular_graph(43, 50).edges) + 50
  # add up to 100 random edges to satellites
  # randomly (?) add i edges into the graph
  # perhaps not random to control for the no. of triangles? 
  # need to do something about # triangles

  # make g the star graph
  g = nx.Graph()
  star_list = [(0, satellite) for satellite in range(1,50)]
  g.add_edges_from(star_list)
  g.add_edges_from(el)
  g.add_edges_from([(j, 50 + j) for j in range(1)])  # link with satellite
  links = 0
  existing_links = set()
  while links < 500:
    a, b = random.sample(satellites,2)
    a, b = min(a,b), max(a,b)
    if (a,b) not in existing_links:
      g.add_edge(a,b)
      existing_links.add((a,b))
      links += 1
      # the way bridges are added can be further modified
      nx.write_edgelist(g,f"./{output_dir}/{cnt}.txt",data=False)
      # nx.draw_networkx(g)
      # plt.show()
      cnt += 1
  # repeat for bridge to center of star
  pass

def gen_star_wheel():
  output_dir = sys.argv[1]
  cnt=0
  satellites = [i for i in range(1,50)]
  
  # make wheel
  el = [(50+i, 50+(i+1)%25) for i in range(25)] + [(75+i, 75+(i+1)%25) for i in range(25)] + [(i, i+25) for i in range(50,75)]
  
  # make g the star graph
  g = nx.Graph()
  star_list = [(0, satellite) for satellite in range(1,50)]
  g.add_edges_from(star_list)
  g.add_edges_from(el)
  g.add_edges_from([(j, 50 + j) for j in range(1)])  # link with satellite
  links = 0
  existing_links = set()
  while links < 500:
    a, b = random.sample(satellites,2)
    a, b = min(a,b), max(a,b)
    if (a,b) not in existing_links:
      g.add_edge(a,b)
      existing_links.add((a,b))
      links += 1
      # the way bridges are added can be further modified
      nx.write_edgelist(g,f"./{output_dir}/{cnt}.txt",data=False)
      # nx.draw_networkx(g)
      # plt.show()
      cnt += 1
# repeat for bridge to center of star
  pass

def gen_diff_fraction_triangles():
  output_dir = sys.argv[1]
  cnt=0
  satellites = [i for i in range(1,50)]
  for degree in range (3, 50, 5): # degree of the regular graph
    el = np.array(nx.random_regular_graph(degree, 50).edges) + 50
    star_list = [(0, satellite) for satellite in range(1,50)]
    for satellite_set in range(11,40):
      g = nx.Graph()
      g.add_edges_from(star_list)
      g.add_edges_from(el)
      g.add_edges_from([(j+1, 50 + j) for j in range(1)])  # link with satellite
      
      partial_link = [(i, i+1) for i in range(1, satellite_set)]
      
      g.add_edges_from(partial_link)
      p1,p2 = 1, satellite_set+1
      offset = 2
      edge_cnt = 0
      while p1 + offset <= p2 and offset <= satellite_set and edge_cnt <= 49 - satellite_set:
        g.add_edge(p1, p1+offset)
        p1 += 1
        edge_cnt += 1
        if p1 + offset == p2:
          p1 = 1
          offset += 1
        # print(offset, satellite_set)
      
      # the way bridges are added can be further modified
      nx.write_edgelist(g,f"./{output_dir}/{cnt}.txt",data=False)
      # nx.draw_networkx(g)
      # plt.show()
      cnt += 1
      if cnt%10 == 0: print(".",end="",flush=True)
  # repeat for bridge to center of star
  print()
  pass

def gen_90_10():
  output_dir = sys.argv[1]
  cnt=0
  el_small = np.array(nx.random_regular_graph(3, 10).edges)
  for degree in range(3, 75): # 75 because otherwise it takes forever..haiz
    el = np.array(nx.random_regular_graph(degree, 90).edges) + 10
    g = nx.Graph()
    g.add_edges_from(el_small)
    g.add_edges_from(el)
    g.add_edges_from([(j, 90 + j) for j in range(1)])
    nx.write_edgelist(g,f"./{output_dir}/{cnt}.txt",data=False)
    cnt += 1
    
def gen_critical_node():
  output_dir = sys.argv[1]
  cnt = 0
  n = 52
  el_small = np.array(nx.random_regular_graph(4, 100-n+1).edges)+n-1
  for degree in range(3,48):
    g = nx.random_regular_graph(degree, n)
    g.add_edges_from(el_small)
    nx.write_edgelist(g,f"./{output_dir}/{cnt}.txt",data=False)
    cnt += 1
  
def gen_critical_node_dense():
  output_dir = sys.argv[1]
  cnt = 0
  n = 52
  el_small = np.array(nx.complete_graph(100-n+1).edges)+n-1
  for degree in range(3,n):
    g = nx.random_regular_graph(degree, n)
    g.add_edges_from(el_small)
    nx.write_edgelist(g,f"./{output_dir}/{cnt}.txt",data=False)
    cnt += 1
 
def gen_90_10_node():
    output_dir = sys.argv[1]
    cnt=0
    el_small = np.array(nx.random_regular_graph(4, 11).edges) + 89
    for degree in range(4, 75): # 75 because otherwise it takes forever..haiz
      g = nx.random_regular_graph(degree,90)
      g.add_edges_from(el_small)
      nx.write_edgelist(g,f"./{output_dir}/{cnt}.txt",data=False)
      cnt += 1
  
def gen_larger_size():
  repeats = 100
  kind = sys.argv[1]
  cnt = 0
  if kind.startswith("well"):
    output_dir = "graphs/largeN_wellmixed"
    if not os.path.exists(output_dir):
      os.makedirs(output_dir)
    for _ in range(repeats):
      for N in range(50, 1000, 50):
        g = nx.complete_graph(N)
        nx.write_edgelist(g,f"./{output_dir}/{cnt}.txt",data=False)
        cnt += 1
  elif kind.startswith("reg"):
    output_dir = "graphs/largeN_regular"
    if not os.path.exists(output_dir):
      os.makedirs(output_dir)
    for _ in range(repeats):
      for N in range(50, 1000, 50):
        g = nx.random_regular_graph(3,N)
        nx.write_edgelist(g,f"./{output_dir}/{cnt}.txt",data=False)
        cnt += 1
  elif kind.startswith("star"):
    output_dir = "graphs/largeN_star"
    if not os.path.exists(output_dir):
      os.makedirs(output_dir)
    for _ in range(repeats):
      for N in range(50, 1000, 50): # 19
        g = nx.star_graph(N)
        nx.write_edgelist(g,f"./{output_dir}/{cnt}.txt",data=False)
        cnt += 1
  
if __name__ == '__main__':
  # gen_myisland()
  # gen_tree_like()
  # gen_identical()
  # gen_alt_detour()
  # gen_diff_deg()
  # gen_very_regular()
  # gen_many_bridges()
  # gen_star_regular()
  # gen_star_wheel()
  # gen_diff_fraction_triangles()
  # gen_90_10_node()
  # gen_critical_node()
  gen_larger_size()