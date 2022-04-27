import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

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
  plt.plot(data.iloc[:,0], data.iloc[:,3],label = 'Poisson')
  data = pd.read_csv('./results/cmp_poisson.txt',sep='\t',header=None)
  plt.plot(data.iloc[:,1], data.iloc[:,4],label = 'uniform continuous')
  plt.xlabel('variance')
  plt.ylabel('probability of fixation')
  plt.title('selection: s = 0.05')
  plt.legend()
  plt.savefig('poisson-uniform.png')
  
def plot_wellmixed():
  d0 = pd.read_csv('./results/wellmixed_diffs_var0.txt',sep='\t',header=None)
  plt.plot(d0.iloc[:,2], d0.iloc[:,3], label = 'variance = 0')
  d1 = pd.read_csv('./results/wellmixed_diffs_var.05.txt',sep='\t',header=None)
  plt.plot(d0.iloc[:,2], d1.iloc[:,3], label = 'variance = 0.05')
  d2 = pd.read_csv('./results/wellmixed_diffs_var.1.txt',sep='\t',header=None)
  plt.plot(d0.iloc[:,2], d2.iloc[:,3], label = 'variance = 0.1')
  d3 = pd.read_csv('./results/wellmixed_diffs_var.15.txt',sep='\t',header=None)
  plt.plot(d0.iloc[:,2], d3.iloc[:,3], label = 'variance = 0.15')
  plt.xlabel('selection s')
  plt.legend()
  plt.savefig('welmixed_diff_s_diff_Var.png')

def uniform_binom_var():
  uni = pd.read_csv("./results/uniform_variance.txt",sep="\t",header=None)
  binom = pd.read_csv("./results/binom_variance.txt",sep="\t",header=None)
  print(uni)
  plt.plot(uni.iloc[:,2],uni.iloc[:,4],label="uniform")
  plt.plot(binom.iloc[:,2],binom.iloc[:,4],label="binomial")
  plt.xlabel("window: +/-")
  plt.legend()
  plt.show()

def aggregate(dirname):
  count = np.zeros((500,))
  matrix_list = []
  for i in range(1,501):
    filename = dirname + f'{i}.txt'
    data = pd.read_csv(filename, sep='\t', header=None)
    data.index = data.iloc[:,2]
    matrix_list.append(data)
    # print(data)
  cmb = pd.concat(matrix_list).groupby(level=0).sum()
  # print(cmb.iloc[:,0].to_string())
  # print(cmb)
  ans = pd.DataFrame()
  ans.index = cmb.index
  freq = cmb.iloc[:,0] // 5
  ans['pfix'] = cmb.iloc[:,3] / freq
  print(ans)
  return ans

def filter():
  dirname = "star_uni_s0"
  for filename in os.listdir(dirname):
    f = os.path.join(dirname, filename)
    print(f)
    data = pd.read_csv(f, sep='\t', header=None)
    if data.iloc[0,0] != 'uniform' or data.iloc[0,3] != 0:
      os.rename(f, dirname+'wrong'+filename)
    
def cmp():
  df = aggregate('star_uni_s0/')
  plt.plot(df.index, df.iloc[:,0], label='uniform, s=0')
  df1 = aggregate('star_binom_s0/')
  plt.plot(df1.index, df1.iloc[:,0], label='binom, s=0')
  df = aggregate('star_uni_s005/')
  plt.plot(df.index, df.iloc[:,0], label='uniform, s=0.05')
  df1 = aggregate('star_binom_s005/')
  plt.plot(df1.index, df1.iloc[:,0], label='binom, s=0.05')
  df = aggregate('star_uni_s01/')
  plt.plot(df.index, df.iloc[:,0], label='uniform, s=0.1')
  df1 = aggregate('star_binom_s01/')
  plt.plot(df1.index, df1.iloc[:,0], label='binom, s=0.1')
  plt.legend()
  plt.show()

if __name__ == '__main__':
  # plot_wellmixed()
  # uniform_binom_var()
  # plot_poi()
  # cmp()
  filter()