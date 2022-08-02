import sys
import networkx as nx

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

def gen_tree_like():
  output_dir = sys.argv[1]
  for i in range(n):
    g = nx.Graph()
  
    nx.write_edgelist(g,f"./{output}/{i}.txt")
  print("Done!")

if __name__ == '__main__':
  # gen_myisland()
  gen_tree_like()