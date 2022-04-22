import sys
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random

n = 100
s = 20

def sim_1d():
  population = [0,0]
  loc = dict()
  for i in range(n):
    loc[i] = random.randint(0,n)
    if loc[i] < s:
      population[0] += 1
    elif loc[i] == n:
      population[1] += 1
  # print(loc)
  while population[0] + population[1] < n:
    for i in range(n):
      if loc[i] < s or loc[i] == n:
        continue
      if random.random() < 0.5:
        loc[i] -= 1
        if loc[i] < s:
          population[0] += 1
      else:
        loc[i] += 1
        if loc[i] == n:
          population[1] += 1
  return population[0] / n

def get1dvar():
  data = np.load('./1dsimresult.npy')
  mean = np.mean(data)
  zeromean = data - mean
  n = data.shape[0]
  sample_var = np.sum(np.square(zeromean)) / (n-1)
  print(np.sqrt(sample_var))
  return sample_var

def get1d_dist():
  nruns = 10000
  ''' data = np.zeros((nruns,))
  for i in range(nruns):
    data[i] = sim_1d()
    if i % 50 == 0:
      print(".",end='',flush=True)
  np.save('1dsimresult',data) '''
  data = np.load('./1dsimresult.npy')
  count,bins_count = np.histogram(data, bins = 20)
  pdf = count / sum(count)
  plt.plot(bins_count[1:],pdf,label='PDF')
  plt.xlabel('chance of fixing to correct loci')
  plt.ylabel('frequency')
  plt.legend()
  plt.savefig('1dmarkov_pdf.png')
  
def sim_2d():
  pass

def get2d_dist():
  pass

if __name__ == '__main__':
  if len(sys.argv) < 2:
    raise Exception('Error: Please enter arguments')
  if sys.argv[1] == '1d':
    get1dvar()
  elif sys.argv[1] == '2d':
    sim_2d()
  else:
    print("please enter 1d or 2d")