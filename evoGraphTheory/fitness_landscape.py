'''
@author: Viola Chen

@description:
- map the fitness given param ranges from 0 to 1
'''


import time, sys
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_pydot import *
from no_visual import*

VISUAL = False
PLOT = True
'''PARAMETERS'''
N_TRIALS = 5 # per run
n_keep = 50 # no. of frames to record

# Evolution parameters
GRAPH_SIZE = 10
N_GEN = 10 # for evolution
MUTATION_RATE = 0.1
WELLMIXED = 0
RING = 1
STAR = 2
MODEL = 0 # default wellmixed

# generate simple graphs
ringgraph = [[(i-1)%GRAPH_SIZE, (i+1)%GRAPH_SIZE] for i in range(GRAPH_SIZE)]
stargraph = [[i for i in range(1,GRAPH_SIZE)]] + [[0] for _ in range(GRAPH_SIZE-1)]

MAPSIZE = 400
NSITE = 2

def run_trial(i, params):
  frac_free = []
  frac_polling = []
  frac_correct = []
  frac_wrong = []
  
  game = MyGame(params, frac_free, frac_polling, frac_correct, frac_wrong)
  game.run()
  
  corrects = np.array(frac_correct[-n_keep:]).reshape((n_keep,1))
  pollings = np.array(frac_polling[-n_keep:]).reshape((n_keep,1))
  wrongs = np.array(frac_wrong[-n_keep:]).reshape((n_keep,1))
  frees = np.array(frac_free[-n_keep:]).reshape((n_keep,1))
  return (frees, pollings, corrects, wrongs)


def run_one_sim(param):
  f, p, r, w = np.zeros((n_keep, 1)),np.zeros((n_keep, 1)),\
                np.zeros((n_keep, 1)),np.zeros((n_keep, 1))  
  params = [param for _ in range(NROBOT)]
  for i in range(N_TRIALS):
    (free, poll, right, wrong) = run_trial(i, params)
    f = np.add(f, free)
    p = np.add(p, poll)
    r = np.add(r, right) 
    w = np.add(w, wrong)
  f = np.divide(f, N_TRIALS)
  p = np.divide(p, N_TRIALS)
  r = np.divide(r, N_TRIALS)
  w = np.divide(w, N_TRIALS)
  score = np.mean(r)
  print(param, score)
  '''if PLOT and score > 0.2:
    plt.clf()
    plt.plot(f, label = 'no idea')
    plt.plot( p, label = 'polling')
    plt.plot( r, label = 'correct site')
    plt.plot(w, label = 'incorrect site')
    plt.ylabel("proportion of agents in each state")
    plt.ylim(0,1)
    plt.legend()
    # Display a figure.
    if N_CHEATER > 0:
      plt.savefig(f"./figures/{MODEL}_{N_CHEATER}_adversary_{param[0]}_average.jpg")
    else: plt.savefig(f"./figures/{MODEL}_noadversary_average_{param[0]}.jpg")'''
    
  return score

if __name__ == '__main__':
  idx = sys.argv[1]
  tic = time.perf_counter()
  '''initialize n = graph_size sets of parameters'''
  n = 101
  all_scores = np.zeros((n,1))
  rand = [0.02 * i - 1 for i in range(n)] # so it's  in [-1, 1]
  def f(r):
    return -r / 2 + 0.5
  params = [(r, f(r)) for r in rand]
  params = np.array(params,dtype="f,f")
  # add some noise
  for i in range(n):
    p = params[i]
    score = run_one_sim(p)
    all_scores[i] = score
  plt.clf()
  plt.plot(rand, all_scores)
  plt.ylabel("best proportion of correct agents in each generation")
  plt.ylim(0,1)
  plt.xlabel("parameter for quality perception, take it as c q_received + (1-c)")
  plt.xlim(-1,1)
  plt.savefig(f"{idx}landscape.jpg")
  toc = time.perf_counter()
  print(f"Duration: {toc - tic:0.4f} seconds")
