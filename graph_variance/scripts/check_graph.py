import networkx as nx
import numpy as np
import sys, os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
##############################################################################
# Util functions
def get_first_inverse(pi):
  '''
  @param: d is a vector / list of degree densities, where index are degree, values are p_i
  @returns: the first inverse moment of the degree distribution
  '''
  res = 0.0
  for d in range(len(pi)):
    if pi[d] == 0:
      continue
    res += pi[d] * (1/d)
  return res

np.set_printoptions(precision=3)

##############################################################################
# graph class
class Graph:
  def __init__(self, filename):
    self.G = nx.read_edgelist(filename,nodetype=int)
    self.list = [list(nbrdict.keys()) for _, nbrdict in self.G.adjacency()]
    arr = ((np.array(nx.degree(self.G)).astype(int)))
    arr = arr[arr[:, 0].argsort()]
    self.degree = list(arr[:,1])
    
  
  def get_p_i(self):
    ''' 
    @return the degree density distribution as a vector
    where index are degree and values are frequency
    '''
    arr = [self.degree.count(d) for d in range(max(self.degree)+1)] 
    return np.array(arr) / len(self.G.nodes)
    
  def get_p_ij(self):  
    ''' 
    @return the transition probability between nodes of degree i and nodes of degree j
    for all possible i, j between 0 and max degree
    '''
    max_d = max(self.degree)
    degree = np.array(self.degree)
    p_ij = np.zeros((max_d+1,max_d+1))
    for i in range(max_d+1):
      # get all nodes with degree i
      di = np.where(degree==i)[0]
      if len(di) == 0:
        continue
      neighbors = []
      for node in di:
        neighbors += self.list[node]
      neighbors = (list(set(neighbors)))
      degrees_of_neighbors = degree[neighbors]
      unique, counts = np.unique(degrees_of_neighbors, return_counts=True)
      # print(i,"uniq",unique, "cnt",counts)
      for pos in range(len(unique)):
        d = unique[pos]
        p_ij[i,d] = counts[pos] / len(neighbors)
    # print(p_ij)
    return p_ij
  
  def compute_amplification(self):
    '''compute the amplification factor in a Moran birth-death model
    '''
    p_i = self.get_p_i() # is a vector
    # print(p_i)
    p_ij = self.get_p_ij() # is a numpy matrix
    term1, term2 = 0.0, 0.0
    for i in range(len(p_i)):
      for j in range(len(p_i)):
        if p_i[i] * p_ij[i,j] == 0:
          continue
        term1 += p_i[i] * p_ij[i,j] * (1/j)
        term2 += p_i[i] * p_ij[i,j] / (j**2)
    alpha = get_first_inverse(p_i) * term1 * (1/term2)
    # print(alpha)
    return alpha
  
  def compute_mixing_pattern(self):
    '''compute the assortativity coefficient of a grpah
    '''
    return nx.degree_assortativity_coefficient(self.G)
  
  def get_n_triangles(self):
    triangle_list = list(nx.triangles(self.G).values())
    return sum(triangle_list) / 3
  
  def get_property(self, xfunc, yfunc):
    x, y = None, None
    def map(string):
      if string.startswith("amp"):
        return self.compute_amplification()
      elif string.startswith("mix"):
        return self.compute_mixing_pattern()
      elif string.startswith("deg"):
        return np.std(self.degree)
  
  def show(self):
    nx.draw_networkx(self.G)
    plt.show()
  
  def remove_a_bridge(self):
    # print(nx.degree(self.G))
    degrees = self.degree
    max_d = max(degrees)
    min_d = min(degrees)
    for (u,v) in self.G.edges():
      u,v = int(u),int(v)
      if (degrees[u] == min_d+1 and degrees[v] > min_d) or \
          (degrees[v] == min_d+1 and degrees[u] > min_d):
        self.G.remove_edge(str(u), str(v))
        degrees = list((np.array(nx.degree(self.G)).astype(int))[:,1])
        # print(degrees)
        return
    print("Failed to remove edge")
    return
   
  def writetofile(self, output):
    nx.write_edgelist(self.G, output, data=False)


##############################################################################
# plotting functions
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

def get_size(n):
  if n < 24: return 4 + 2 * n
  elif n < 50: 
    if n-24 < 20: return 5 + (n-24)
    else: return 25 + 5 * (n-44)
  elif n < 74: return 4 + 2 *(n - 50)
  else: 
    if n-74 < 20: return 5 + (n-74)
    else: return 25 + 5 * (n-94)

def plot_dir(dirname, result_dirname):
  n = len(os.listdir(f"{result_dirname}1"))
  xs = np.zeros((n,))
  ys = np.zeros((n,))
  degs = np.zeros((n,))
  color = np.zeros((n,)) # amplification factor or whatever it is
  for rep in range(1,6):
    result_dir = f"{result_dirname}{rep}"
    for filename in os.listdir(result_dir):
      f = (os.path.join(result_dir,filename))
      # print(f)
      id = int(filename.split(".")[0])
      if os.stat(f).st_size == 0:
        print(id, "file is empty")
        continue
      data = pd.read_csv(f, sep='\t', header=None)
      graphfile = f"{dirname}{id}.txt"
      xs[id%n] += (data.iloc[0,4])
      ys[id%n] += (data.iloc[1,4])
      
      g = Graph(graphfile)
      degrees = g.degree
      # print(degrees)
      degs[id%n] = abs(degrees[98] - degrees[2]) # np.std(degrees) # abs(degrees[98] - degrees[2]) #
      
      color[id%n] = sum(nx.triangles(g.G).values()) / 3# get_size(id%n) # nx.transitivity(g.G) # g.compute_amplification()
      # g.show()
  ratio = np.divide(np.array(ys),np.array(xs))
  mask = np.isfinite(ratio)
  x_axis = degs
  colors = None
  df = pd.DataFrame({f"{sys.argv[1]}":x_axis,"pfix_max_variance / pfix_0_variance":ratio})
  print(df)
  g = sns.lmplot(x=sys.argv[1], y="pfix_max_variance / pfix_0_variance", data=df)
  # plt.scatter(color,ratio)
  # plt.gca().set(title="", xlabel=sys.argv[1],ylabel="ratio of pfix_max_variance / pfix_0_variance")
  # plt.colorbar()
  g.show()
  

if __name__ == "__main__":
  
  # plot_detour()
  f = 2
  name = sys.argv[2]
  dirname = f"./graphs/{name}/"
  result_dirname = f"./graphs/res_{name}"
  graphtype = f"isl{f}"
  name = os.path.join(result_dirname,graphtype)
  ratio = plot_dir(dirname, result_dirname)
  # plot_density("../graphs/isl1_graphs/")
  # for i in range(200):
  #   # print(i)
  #   # g = Graph("./graphs/wellmixed.txt") # sanity check
  #   g = Graph(f'./graphs/isl3_graphs/{i}.txt')
  #   print(i, sum(nx.triangles(g.G).values()) / 3, ratio[i])
  #   # g.remove_a_bridge()
  #   # g.writetofile(f'./alt_island3/{i}.txt')
  #   # g.compute_amplification()
  #   g.show()