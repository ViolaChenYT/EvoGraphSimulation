import numpy as np
import sys
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import scipy

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
  count = np.zeros((100,))
  matrix_list = []
  for i in range(1,101):
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
  # print(ans)
  return ans - ans['pfix'][0]

def filter():
  dirname = "star_uni_s0"
  for filename in os.listdir(dirname):
    f = os.path.join(dirname, filename)
    print(f)
    data = pd.read_csv(f, sep='\t', header=None)
    if data.iloc[0,0] != 'uniform' or data.iloc[0,3] != 0:
      os.rename(f, dirname+'wrong'+filename)
      
def aggr(dirname):
  matrix_list = []
  cnt = 0
  for filename in os.listdir(dirname):
    f = os.path.join(dirname, filename)
    data = pd.read_csv(f, sep='\t', header=None)
    data.index = data.iloc[:,2]
    matrix_list.append(data)
    cnt = cnt + 1
  cmb = pd.concat(matrix_list).groupby(level=0).sum()
  # print(cmb.iloc[:,0].to_string())
  # print(cmb)
  ans = pd.DataFrame()
  ans.index = cmb.index
  ans['pfix'] = cmb.iloc[:,3] / cnt
  return ans - ans['pfix'][0]
    
def uni():
  df = aggregate('wellmixed_uni_s0/')
  plt.plot(df.index, df.iloc[:,0], label='uniform, s=0')
  df1 = aggregate('wellmixed_binom_s0/')
  plt.plot(df1.index, df1.iloc[:,0], label='binom, s=0')
  df = aggregate('wellmixed_uni_s005/')
  plt.plot(df.index, df.iloc[:,0], label='uniform, s=0.05')
  df1 = aggregate('wellmixed_binom_s005/')
  plt.plot(df1.index, df1.iloc[:,0], label='binom, s=0.05')
  df = aggregate('wellmixed_uni_s01/')
  plt.plot(df.index, df.iloc[:,0], label='uniform, s=0.1')
  df1 = aggregate('wellmixed_binom_s01/')
  plt.plot(df1.index, df1.iloc[:,0], label='binom, s=0.1')
  plt.legend()
  plt.show()

def star():
  df = aggr('star_uni_s0/')
  plt.plot(df.index, df.iloc[:,0], label='uniform, s=0')
  df1 = aggr('star_binom_s0/')
  plt.plot(df1.index, df1.iloc[:,0], label='binom, s=0')
  df = aggr('star_uni_s005/')
  plt.plot(df.index, df.iloc[:,0], label='uniform, s=0.05')
  df1 = aggr('star_binom_s005/')
  plt.plot(df1.index, df1.iloc[:,0], label='binom, s=0.05')
  df = aggr('star_uni_s01/')
  plt.plot(df.index, df.iloc[:,0], label='uniform, s=0.1')
  df1 = aggr('star_binom_s01/')
  plt.plot(df1.index, df1.iloc[:,0], label='binom, s=0.1')
  plt.legend()
  plt.show()
  
def cmp():
  ''' df = aggregate('wellmixed_binom_s0/')
  df1 = aggr('star_binom_s0/')
  plt.plot(df.index ** 2, df.iloc[:,0],  label='wellmixed, binom, s=0')
  plt.plot(df1.index ** 2, df1.iloc[:,0], label='star, binom, s=0')  '''
  ''' plt.plot(df.index ** 2, df.iloc[:,0], 'b-', label='wellmixed, binom, s=0')
  plt.plot(df1.index ** 2, df1.iloc[:,0] ,color='red', label='star, binom, s=0')  '''
  
  ''' df = aggregate('wellmixed_binom_s005/')
  df1 = aggr('star_binom_s005/')
  plt.plot(df.index ** 2, df.iloc[:,0],  label='wellmixed, binom, s=0.05')
  plt.plot(df1.index ** 2, df1.iloc[:,0], label='star, binom, s=0.05') '''
  ''' plt.plot(df.index**2, df.iloc[:,0], 'b--', label='wellmixed, binom, s=0.05')
  plt.plot(df1.index **2, df1.iloc[:,0],color='red', linestyle='dashed', label='star, binom, s=0.05') '''
  
  df = aggregate('wellmixed_binom_s01/')
  df1 = aggr('star_binom_s01/')
  plt.plot(df.index**2, df.iloc[:,0], label='wellmixed, binom, s=0.1')
  plt.plot(df1.index**2, df1.iloc[:,0] , label='star, binom, s=0.1')
  ''' plt.plot(df.index**2, df.iloc[:,0], 'b:', label='wellmixed, binom, s=0.1')
  plt.plot(df1.index**2, df1.iloc[:,0] ,color='red', linestyle=':', label='star, binom, s=0.1') '''
  plt.legend()
  plt.xlabel('variance')
  plt.ylabel('Probability of fixation - prob. fix with var = 0')
  plt.show()
  
def one_model(model='wellmixed',dist='uniform'):
  dist1 = dist
  if dist == 'uniform':
    dist = 'uni'
  def get_var(df1):
    if dist == 'uni':
      return (df1.index * 2) ** 2 / 12
    elif dist == 'binom':
      return df1.index ** 2
  def get_data(f):
    if model == 'wellmixed':
      return aggregate(f)
    elif model == 'star':
      return aggr(f)
  df1 = get_data(f'{model}_{dist}_s0/')
  #print(df1)
  var = get_var(df1)
  #print(var)
  plt.plot(var, df1.iloc[:,0], label=f'{model},{dist1}, s=0')
  df1 = get_data(f'{model}_{dist}_s005/')
  var = get_var(df1)
  plt.plot(var, df1.iloc[:,0], label=f'{model},{dist1}, s=0.05')
  df1 = get_data(f'{model}_{dist}_s01/')
  var = get_var(df1)
  plt.plot(var, df1.iloc[:,0], label=f'{model},{dist1}, s=0.1')
  plt.legend()
  plt.xlabel('variance')
  plt.ylabel('Probability of fixation')
  plt.show()

def collect(dirname):
  s0_list = []
  s005_list = []
  s01_list = []
  s02_list = []
  cnt = 0
  for filename in os.listdir(dirname):
    # print(filename, flush=True)
    f = os.path.join(dirname, filename)
    data = pd.read_csv(f, sep='\t', header=None)
    index = data.iloc[:10,2]
    mat_s0 = data.iloc[:10,4]
    mat_s0.index = index
    s0_list.append(mat_s0)
    mat_s005 = data.iloc[10:20,4]
    mat_s005.index = index
    s005_list.append(mat_s005)
    mat_s01 = data.iloc[20:30,4]
    mat_s01.index = index
    s01_list.append(mat_s01)
    mat_s02 = data.iloc[30:40,4]
    mat_s02.index = index
    s02_list.append(mat_s02)
    cnt = cnt + 1
  cmb1 = pd.concat(s0_list).groupby(level=0).sum()/cnt
  cmb2 = pd.concat(s005_list).groupby(level=0).sum()/cnt
  cmb3 = pd.concat(s01_list).groupby(level=0).sum()/cnt
  cmb4 = pd.concat(s02_list).groupby(level=0).sum()/cnt
  return cmb1,cmb2,cmb3,cmb4

def scollect(dirname):
  s0_list = []
  s005_list = []
  s01_list = []
  s02_list = []
  cnt = 0
  for filename in os.listdir(dirname):
    f = os.path.join(dirname, filename)
    data = pd.read_csv(f, sep='\t', header=None)
    index = data.iloc[:11,2]
    mat_s0 = data.iloc[:11,4]
    mat_s0.index = index
    s0_list.append(mat_s0)
    mat_s005 = data.iloc[11:22,4]
    mat_s005.index = index
    s005_list.append(mat_s005)
    mat_s01 = data.iloc[22:33,4]
    mat_s01.index = index
    s01_list.append(mat_s01)
    mat_s02 = data.iloc[33:44,4]
    mat_s02.index = index
    s02_list.append(mat_s02)
    cnt = cnt + 1
  cmb1 = pd.concat(s0_list).groupby(level=0).sum()/cnt
  cmb2 = pd.concat(s005_list).groupby(level=0).sum()/cnt
  cmb3 = pd.concat(s01_list).groupby(level=0).sum()/cnt
  cmb4 = pd.concat(s02_list).groupby(level=0).sum()/cnt
  return cmb1,cmb2,cmb3,cmb4

def plot_mean1(dirname):
  m1,m2,m3,m4 = collect(dirname)
  s1,s2,s3,s4 = scollect('std_' + dirname)
  plt.scatter(m1.index**2, m1, label='s=0')
  plt.scatter(m2.index**2, m2, label='s=0.05')
  plt.scatter(m3.index**2, m3, label='s=0.1')
  plt.scatter(m4.index**2, m4, label='s=0.2')
  plt.scatter(s1.index**2, s1, label='standard s=0')
  plt.scatter(s2.index**2, s2, label='standard s=0.05')
  plt.scatter(s3.index**2, s3, label='standard s=0.1')
  plt.scatter(s4.index**2, s4, label='standard s=0.2')
  plt.legend()
  plt.xlabel('variance')
  plt.ylabel('Probability of fixation')
  plt.show()

def cmp_mean1():
  # m1,m2,m3,m4 = collect('star')
  s1,s2,s3,s4 = scollect('std_' + 'star')
  plt.plot(s1.index**2, s1, label='star s=0')
  plt.plot(s2.index**2, s2, label='star s=0.05')
  plt.plot(s3.index**2, s3, label='star s=0.1')
  plt.plot(s4.index**2, s4, label='star s=0.2')
  s1,s2,s3,s4 = scollect('std_' + 'wellmixed')
  plt.plot(s1.index**2, s1, label='wellmixed s=0')
  plt.plot(s2.index**2, s2, label='wellmixed s=0.05')
  plt.plot(s3.index**2, s3, label='wellmixed s=0.1')
  plt.plot(s4.index**2, s4, label='wellmixed s=0.2')
  plt.legend()
  plt.xlabel('variance')
  plt.ylabel('Probability of fixation')
  plt.show()

def get_param_graph_label(i):
  if i < 0:
    print("error in index")
    return
  if i < 100:
    return "ER p = 0.03"
  # elif i < 200:
  #   return "PA m = 3"
  # elif i < 300:
  #   return "PA m = 5"
  # elif i < 400:
  #   return "PA m = 7"
  elif i < 400:
    return "PA"
  elif i < 450:
    return "Bi"
  elif i < 510:
    return "SW m = 4"
  elif i < 600:
    return "detour"
  elif i < 700:
    return "star"
  else:
    return "rgg"
  # elif i < 750:
  #   return "rgg r= 0.3"
  # else: return "rgg r= 0.5"
  
def fx(x, pfix):
  '''return pfix - (1-(1+S_eff)^{-1}) / (1-(1+S_eff)^{-N})
     solving for x = S_eff
  '''
  term = (1 - 1/(1 + x)) / (1 - 1 / ((1 + x) ** 100))
  return pfix-term
  

def plot_effective():
  '''plot the effective fitness S_eff instead of pfix'''
  start = np.array([1.1])
  xs, ys = np.load("pfix0.npy"), np.load("pfixmax.npy")
  n = len(xs)
  seff0 = np.zeros((n,))
  seffmax = np.zeros((n,))
  for i in range(n):
    seff0[i] = scipy.optimize.fsolve(fx, x0=start, args=(xs[i]))
    seffmax[i] = scipy.optimize.fsolve(fx, x0=start, args=(ys[i]))
    
  fig, ax = plt.subplots()
  for g in np.unique(groups):
      ix = np.where(groups == g)
      ax.scatter(seff0[ix], seffmax[ix], label = g,s=3)
  m,b = np.polyfit(seff0,seffmax,1)
  plt.plot(xs, m*xs + b)
  # plt.plot(xs, 0.632 * xs)
  plt.text(xs[0],ys[0], f"y = {m:.3f}x + {b:.3f}")
  print(m,b)
  ax.legend()
  plt.show()
  # lst = ["20_3","assort","complex","fam","isl0","isl1","mv","pa","regx4"]

def plot_graphs():
  # dirname = "graph_result"
  groups = np.vectorize(get_param_graph_label)(np.arange(0,800))
  # count = np.full((800, ), 0, dtype=int)
  # pfix0 = np.zeros((800,))
  # pfixmax = np.zeros((800,))
  # for filename in os.listdir(dirname):
  #   id = int(filename.split(".")[0]) % 800
  #   f = os.path.join(dirname, filename)
  #   if os.stat(f).st_size == 0:
  #     continue
  #   data = pd.read_csv(f, sep='\t', header=None)
  #   pfix0[id] += data.iloc[0,4]
  #   pfixmax[id] += data.iloc[1,4]
  #   count[id] += 1
  # dirname = dirname+"1"
  # for filename in os.listdir(dirname):
  #   id = int(filename.split(".")[0]) % 800
  #   f = os.path.join(dirname, filename)
  #   if os.stat(f).st_size == 0:
  #     continue
  #   data = pd.read_csv(f, sep='\t', header=None)
  #   pfix0[id] += data.iloc[0,4]
  #   pfixmax[id] += data.iloc[1,4]
  #   count[id] += 1
  # xs = np.divide(pfix0, count)
  # ys = np.divide(pfixmax, count)
  # np.save("pfix0.npy",xs)
  # np.save("pfixmax.npy",ys)
  xs, ys = np.load("pfix0.npy"), np.load("pfixmax.npy")
  fig, ax = plt.subplots()
  for g in np.unique(groups):
      ix = np.where(groups == g)
      ax.scatter(xs[ix], ys[ix], label = g,s=3)
  lst = ["20_3","assort","complex","fam","isl0","isl1","mv","pa","regx4"]
  dirname = "graphall_result"
  for graphtype in lst:
    name = os.path.join(dirname,graphtype)
    n = len(os.listdir(name))
    xs1 = []
    ys1 = []
    for filename in os.listdir(name):
      f = os.path.join(name,filename)
      id = int(filename.split(".")[0])
      if os.stat(f).st_size == 0:
        continue
      data = pd.read_csv(f, sep='\t', header=None)
      xs1.append(data.iloc[0,4])
      ys1.append(data.iloc[1,4])
    print(graphtype)
    ax.scatter(xs1,ys1,label=graphtype,s=3)
    xs = np.concatenate((xs, np.array(xs1)))
    ys = np.concatenate((ys, np.array(ys1)))
  # dirname="wheel_result"
  # pfix0 = np.zeros((100,))
  # pfixmax = np.zeros((100,))
  # for filename in os.listdir(dirname):
  #   id = int(filename)
  #   f = os.path.join(dirname, filename)
  #   if os.stat(f).st_size == 0:
  #     continue
  #   data = pd.read_csv(f, sep='\t', header=None)
  #   pfix0[id] = data.iloc[0,4]
  #   pfixmax[id] = data.iloc[1,4]
  # plt.scatter(pfix0,pfixmax,label="wheel",s=3)
  # np.save("xs.npy",xs)
  # np.save("ys.npy",ys)
  m,b = np.polyfit(xs,ys,1)
  plt.plot(xs, m*xs + b)
  plt.plot(xs, 0.632 * xs)
  plt.text(xs[0],ys[0], f"y = {m:.3f}x + {b:.3f}")
  print(m,b)
  ax.legend()
  plt.show()

def plot_wheel():
  dirname="../wheel_result"
  pfix0 = np.zeros((100,))
  pfixmax = np.zeros((100,))
  for filename in os.listdir(dirname):
    id = int(filename)
    f = os.path.join(dirname, filename)
    if os.stat(f).st_size == 0:
      continue
    data = pd.read_csv(f, sep='\t', header=None)
    pfix0[id] = data.iloc[0,4]
    pfixmax[id] = data.iloc[1,4]
  plt.scatter(pfix0,pfixmax,label="wheel",s=3)
  plt.legend()
  plt.show()
  
def plot_some_graphs():
  dirname = "../graph_result"
  groups = np.vectorize(get_param_graph_label)(np.arange(0,800))
  count = np.full((800, ), 0, dtype=int)
  pfix0 = np.zeros((800,))
  pfixmax = np.zeros((800,))
  for filename in os.listdir(dirname):
    id = int(filename.split(".")[0]) % 800
    f = os.path.join(dirname, filename)
    if os.stat(f).st_size == 0:
      continue
    data = pd.read_csv(f, sep='\t', header=None)
    pfix0[id] += data.iloc[0,4]
    pfixmax[id] += data.iloc[1,4]
    count[id] += 1
  dirname = dirname+"1"
  for filename in os.listdir(dirname):
    id = int(filename.split(".")[0]) % 800
    f = os.path.join(dirname, filename)
    if os.stat(f).st_size == 0:
      continue
    data = pd.read_csv(f, sep='\t', header=None)
    pfix0[id] += data.iloc[0,4]
    pfixmax[id] += data.iloc[1,4]
    count[id] += 1
  xs = np.divide(pfix0, count)
  ys = np.divide(pfixmax, count)
  np.save("pfix0.npy",xs)
  np.save("pfixmax.npy",ys)
  fig, ax = plt.subplots()
  for g in np.unique(groups):
      ix = np.where(groups == g)
      ax.scatter(xs[ix], ys[ix], label = g,s=5)
  lst = ["isl0","isl1","isl2","isl3"]
  dirname = "../graphall_result/"
  for graphtype in lst:
    name = os.path.join(dirname,graphtype)
    n = len(os.listdir(name))
    xs = []
    ys = []
    for filename in os.listdir(name):
      f = os.path.join(name,filename)
      id = int(filename.split(".")[0])
      if os.stat(f).st_size == 0:
        continue
      data = pd.read_csv(f, sep='\t', header=None)
      xs.append(data.iloc[0,4])
      ys.append(data.iloc[1,4])
    print(graphtype)
    plt.scatter(xs,ys,label=graphtype,s=5)
  # dirname="../wheel_result/"
  # pfix0 = np.zeros((100,))
  # pfixmax = np.zeros((100,))
  # for filename in os.listdir(dirname):
  #   id = int(filename)
  #   f = os.path.join(dirname, filename)
  #   if os.stat(f).st_size == 0:
  #     continue
  #   data = pd.read_csv(f, sep='\t', header=None)
  #   pfix0[id] = data.iloc[0,4]
  #   pfixmax[id] = data.iloc[1,4]
  # plt.scatter(pfix0,pfixmax,label="wheel",s=5)
  ax.legend()
  plt.show()
  
def plot_some_dirs(dirlist):
  count = np.full((800, ), 0, dtype=int)
  pfix0 = np.zeros((800,))
  pfixmax = np.zeros((800,))
  fig, ax = plt.subplots()
  for name in dirlist:
    n = len(os.listdir(name))
    xs = []
    ys = []
    for filename in os.listdir(name):
      f = os.path.join(name,filename)
      id = int(filename.split(".")[0])
      if os.stat(f).st_size == 0:
        continue
      print(id)
      data = pd.read_csv(f, sep='\t', header=None)
      xs.append(data.iloc[0,4])
      ys.append(data.iloc[1,4])
    ax.scatter(xs,ys,label=name)
  ax.legend()
  plt.xlabel("pfix 0")
  plt.ylabel("pfix max")
  plt.show()
  
def plot_skew_concept():
  x = [0.1, 0.6, 1.1, 1.6, 2.1]
  left = [0.25, 0, 0.25, 0.5,0]
  plt.bar(x,left, width = 0.3, tick_label=x)
  plt.gca().set(title="left skew, wildtype fitness 1", xlabel="mutant fitness",ylabel="probability")
  plt.savefig("left skew")
  plt.clf()
  right = [0, 0.5, 0.25, 0, 0.25]
  plt.bar(x,right, width=0.3,tick_label=x)
  plt.gca().set(title="right skew, wildtype fitness 1", xlabel="mutant fitness",ylabel="probability")
  plt.savefig("right skew")
  plt.clf()
  mid = [0, 0.5, 0, 0.5, 0]
  plt.bar(x,mid, width=0.3,tick_label=x)
  plt.gca().set(title="no skew, wildtype fitness 1", xlabel="mutant fitness",ylabel="probability")
  plt.savefig("no skew")
  
def plot_skew():
  dirname = "skew_result"
  left = [[],[],[]]
  mid = [[],[],[]]
  right = [[],[],[]]
  count = [0,0,0]
  for filename in os.listdir(dirname):
    f = os.path.join(dirname, filename)
    id = int(filename.split(".")[0])
    if os.stat(f).st_size == 0:
      continue
    data = pd.read_csv(f, sep='\t', header=None)
    # print(data)
    if id < 100:
      right[0].append(data.iloc[0,4])
      mid[0].append(data.iloc[1,4])
      left[0].append(data.iloc[2,4])
      count[0]+=1
    elif id < 200:
      right[1].append(data.iloc[0,4])
      mid[1].append(data.iloc[1,4])
      left[1].append(data.iloc[2,4])
      count[1]+=1
    else:
      right[2].append(data.iloc[0,4])
      mid[2].append(data.iloc[1,4])
      left[2].append(data.iloc[2,4])
      count[2]+=1
  left = np.array(left) / count
  mid = np.array(mid) / count
  right = np.array(right) / count

  mean_l, mean_m, mean_r = np.mean(left), np.mean(mid),np.mean(right)
  print(mean_l, mean_m, mean_r)
  std_l,std_m,std_r = np.std(left), np.std(mid),np.std(right)
  
  fig, ax = plt.subplots()
  ax.bar(np.arange(3), [mean_l, mean_m, mean_r], yerr=[std_l,std_m,std_r], align='center', alpha=0.5, ecolor='black', capsize=10)
  ax.set_xticks(np.arange(3))
  ax.set_xticklabels(["left skew", "no skew", "right skew"])
  ax.set_title('pfix of different skew, mean 1, sigma2 = 0.25, s=0.1')
  
  plt.show()
  
if __name__ == '__main__':
  # plot_wellmixed()
  # uniform_binom_var()
  # plot_poi()
  # cmp()
  # aggr('star_uni_s0')
  # star()
  # cmp()
  # one_model('star','uni')
  # plot_mean1(sys.argv[1])
  # cmp_mean1()
  plot_graphs()
  # plot_some_dirs(["./graphall_result/isl3", "./graphall_result/assort","./reg_identical_res"])
  # plot_wheel()
  # plot_skew_concept()
  # plot_skew()
  