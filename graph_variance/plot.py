import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def plot_window():
  data = pd.read_csv('./results/window1.txt',sep='\t',header=None)
  # binomdata = pd.read_csv('./results/binom_window.txt',sep='\t',header=None)
  plt.plot(data.iloc[:,0], data.iloc[:,2],label = 'uniform continuous')
  # plt.plot(binomdata.iloc[:,0],binomdata.iloc[:,2],label='discrete binomial')
  plt.xlabel('fitness mean')
  plt.ylabel('probability of fixation')
  # plt.title('p-fix with uniform +/- 1 noise on mutant, 20000 runs')
  plt.savefig('pfix-window-uniform.jpg')
  
def plot_poi():
  data = pd.read_csv('./results/poisson.txt',sep='\t',header=None)
  plt.plot(data.iloc[:,0], data.iloc[:,2],label = 'Poisson')
  data = pd.read_csv('./results/window1.txt',sep='\t',header=None)
  plt.plot(data.iloc[:50,0], data.iloc[:50,2],label = 'uniform continuous')
  plt.xlabel('lambda')
  plt.ylabel('probability of fixation')
  plt.ylim(0,0.01)
  plt.legend()
  plt.title('p-fix Poisson, 100000 runs')
  plt.savefig('pfix-poisson.jpg')

if __name__ == '__main__':
  plot_poi()