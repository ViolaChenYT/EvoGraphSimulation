import sys
import networkx as nx

if __name__ == '__main__':
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
