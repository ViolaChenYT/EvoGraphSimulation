import networkx as nx
import numpy as np
import sys, os
import pandas as pd
import matplotlib.pyplot as plt

class Graph:
  def __init__(self, filename):
    self.G = nx.Graph()
    with open(filename,'r') as f:
      edges = f.readlines()
    for line in edges:
      (a,b) = line.split()
      self.G.add_edge(a,b)
      self.G.add_edge(b,a)
    f.close()
  
  def compute_amplification(self):
    '''compute the amplification factor in a Moran birth-death model
    '''
    degrees = np.array(nx.degree(self.G)).astype(int)
    degrees = pd.DataFrame(degrees,columns=["index", "degree"],dtype=int)
    degrees.sort_values(by="index",inplace=True)
    degrees.index = degrees["index"]
    print(degrees)
    max_d = np.max(degrees["degree"])
    print(max_d)
    p_i = np.array([len(degrees[degrees["degree"]==i]["degree"]) for i in range(max_d + 1)]) / len(self.G.nodes)
    print(p_i)
    return alpha
  
  def compute_mixing_pattern(self):
    '''compute the assortativity coefficient of a grpah
    '''
    return nx.degree_assortativity_coefficient(self.G)
  
  def get_n_triangles(self):
    return nx.triangles(self.G)
  
  def show(self):
    nx.draw_networkx(self.G)
    plt.show()
   
def plot_density(dirname):
  densities = []
  if dirname == "../param_graphs/":
    for i in range(510,600):
      graphfile = f"{dirname}{i}.txt"
      g = Graph(graphfile)
      densities.append(nx.density(g.G))
  else:
    for i in range(800):
      graphfile = f"{dirname}{i}.txt"
      g = Graph(graphfile)
      densities.append(nx.density(g.G))
  plt.plot(densities)
  plt.show()
    
    
def detour():
  pfix0 = np.load("pfix0.npy")
  pfixmax = np.load("pfixmax.npy")
  ratio = pfixmax / pfix0
  # detourlen = [610 - i for i in range(510,600)]
  # plt.plot(detourlen, ratio[510:600])
  # plt.gca().set(title="", xlabel="detour length",ylabel="ratio of pfix_max_variance / pfix_0_variance")
  # plt.show()
  return ratio[510:600]

def plot_detour():
  dirname = "../param_graphs/"
  degs = []
  for i in range(510, 600):
    graphfile = f"{dirname}{i}.txt"
    g = Graph(graphfile)
    degrees = np.array(nx.degree(g.G)).astype(int)
    degs.append(np.std(degrees[:,1]))
  degs = np.array(degs)
  plt.scatter(degs, detour())
  plt.gca().set(title="", xlabel="degree standard deviation",ylabel="ratio of pfix_max_variance / pfix_0_variance")
  plt.show()

def get_amp_factor(filename):
  g = Graph(filename)
  return g.compute_amplification()

def get_mix_pat(filename):
  g = Graph(filename)
  return g.compute_mixing_pattern()

def plot_island(f=2):
  if f < 0 or f > 3:
    raise Exception("Invalid graph family")
  dirname = f"../graphs/isl{f}_graphs/"
  degs = []
  
  
  result_dirname = "../graphall_result/"
  graphtype = f"isl{f}"
  name = os.path.join(result_dirname,graphtype)
  n = len(os.listdir(name))
  xs = []
  ys = []
  for filename in os.listdir(name):
    f = os.path.join(name,filename)
    id = int(filename.split(".")[0])
    if os.stat(f).st_size == 0:
      continue
    graphfile = f"{dirname}{id}.txt"
    g = Graph(graphfile)
    degrees = np.array(nx.degree(g.G)).astype(int)
    degs.append(np.std(degrees[:,1]))
    data = pd.read_csv(f, sep='\t', header=None)
    xs.append(data.iloc[0,4])
    ys.append(data.iloc[1,4])
  # print(graphtype)
  # ax.scatter(xs,ys,label=graphtype,s=5)
  degs = np.array(degs)
  ratio = np.array(ys) / np.array(xs)
  
  plt.scatter(degs, ratio)
  plt.gca().set(title="", xlabel="degree standard deviation",ylabel="ratio of pfix_max_variance / pfix_0_variance")
  plt.show()
  

if __name__ == "__main__":
  
  # plot_detour()
  # plot_island(2)
  # plot_density("../graphs/isl1_graphs/")
  g = Graph('..//wheel.txt')
  g.compute_amplification()
  # g.show()