import sys
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_pydot import *

A = 10
n = 2

def run1simulation(G, T, s):
    N = len(G) # no. of vertices
    mutation_w = 0.12

    # randomly initialized population
    pop = np.random.randn(N, n) / 4 + 5 * np.ones((N, n))
    # random normal, mean 5

    prob = np.zeros(N) 
    
    traj = np.zeros((T, n))
    var = np.zeros((T, n))
    
    best_array = np.zeros(T)
    mean_array = np.zeros(T)
    
    for t in range(T): # each run
        rugged = np.cos(2 * np.pi * pop)
        fit = (pop**2 + A * (1 - rugged)).sum(1)

        # print(t, fit.mean(), fit.min()) # the population fitness

        prob[fit.argsort()] = (1 + np.linspace(-s, s, N))[::-1]
        prob = np.maximum(prob, 1/N)

        traj[t, :] = pop.mean(0)
        var[t,:] = pop.std(0)
        
        best_array[t] = fit.min()
        mean_array[t] = fit.mean()
        
        for _ in range(N): # each vertex
            prob /= prob.sum()

            birth = np.random.choice(range(N), p = prob)
            death = np.random.choice(list(G.neighbors(birth)) )
            pop[death,:] = pop[birth,:]
            prob[death] = prob[birth]
            
            if np.random.rand() > 0.5:
                pop[death,:] += mutation_w * np.random.randn(n) / np.sqrt(n)
            else:
                pop[birth,:] += mutation_w * np.random.randn(n) / np.sqrt(n)
        pop[np.random.choice(range(N), N // 2),:] += mutation_w * np.random.randn(n)
    
    #print(best_array.shape, mean_array.shape, traj.shape, var.shape)
    plt.plot(mean_array)
    plt.xlabel("time")
    plt.ylabel("fitness")
    plt.show()
    return np.hstack([best_array[:,None], mean_array[:,None], traj, var])#best_array, mean_array, traj, var


def make_graph(adjlist):
  '''takes in a graph in the form of adjacency list where each entry is an edge,
   returns a networkx graph G'''
  N = np.max(adjlist) + 1
  G = nx.Graph()
  G.add_nodes_from(range(N))
  G.add_edges_from(adjlist)
  return G


if __name__ == "__main__":

    # Training time
    T_train = int(sys.argv[1])

    # Number of runs
    runs = int(sys.argv[2])
    
    # input graph - adj list, each row -> edge?
    el = np.loadtxt(sys.argv[3]).astype(int)
    
    # output files
    out_path = sys.argv[4]
    
    
    results = np.zeros((runs + 1, T_train, 6)) 
    
    G = make_graph(el)
    #G = nx.generators.random_graphs.random_regular_graph(3,100)
    nx.draw(G,with_labels=True, font_weight='bold')
    plt.show()
    
    for i in range(runs):
        results[i] = run1simulation(G, T_train, 1)
    
    # last run on a complete graph
    N = np.max(el) + 1
    G = nx.complete_graph(N)
    results[runs] = run1simulation(G, T_train, 1)
    # print(results)
    #subax1 = plt.subplot(121)
    # pos = nx.spring_layout(G)
    #subax2 = plt.subplot(122)
    #plt.plot(results[:,:,])

    np.save(out_path, results)
    
    
    
