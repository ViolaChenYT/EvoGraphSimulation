'''
@author: Viola Chen


@TODO: 2/21
randomness seems to really play a part here, any way to get over that?
like it is really supposed to converge etc intuitively, but many times it is not
- try different cases of initial condition
- squares? 
- more adversary?

@isses: 2/25
- slower convergence
- still susceptable to drift
- this just reminds me to population genetics, is there anything i can do to uh minimize
  drift?
- use some sort of coverage algorithm?
- it may not be optimal in this case
  (randomize the x-y coordinate too)
- resource utilization?

@TODO: 2/25
- every time there is a mutation, re-run simulation
- have to normalize everyhting

@TODO: 2/28
- ask for cluster access
- increase params
  - graph_size: 5 -> 10
  - repeats: 7 -> 10? 20?
  - n_gen: 5 -> 50? 100?
- confidence interval for the plots
- plot some sort of fitness landscape (fitness against param)
- use jupyter notebook 0. 0
- make sure u don't select yourself in birthdeat
- ring / star graph
- when mutation happen, think about whether to mutate parent or child
'''
import random, math, pygame,time
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_pydot import *
from no_visual import*

VISUAL = False
PLOT = True
'''PARAMETERS'''
N_TRIALS = 5 # per run
n_keep = N_ITER # no. of frames to record

# Evolution parameters
GRAPH_SIZE = 10
N_GEN = 10 # for evolution
MUTATION_RATE = 0.1
WELLMIXED = 0
RING = 1
STAR = 2
MODEL = STAR

# generate simple graphs
ringgraph = [[(i-1)%GRAPH_SIZE, (i+1)%GRAPH_SIZE] for i in range(GRAPH_SIZE)]
stargraph = [[i for i in range(1,GRAPH_SIZE)]] + [[0] for _ in range(GRAPH_SIZE-1)]

MAPSIZE = 400
NSITE = 2

RED = pygame.Color('#ff1744')
PINK = pygame.Color('#E30B5C')
YELLOW = pygame.Color('#FFEA00')
PURPLE = pygame.Color('#ea80fc')
GREEN = pygame.Color('#4caf50')
BLUE = pygame.Color('#42a5f5')
DARKBLUE = pygame.Color('#00008B')            

SITE_PALETTE = [RED, DARKBLUE]
BOT_PALETTE = [PINK, BLUE]

class PygameGame(object):
  def __init__(self, params, free, polling, right, wrong, width = 600, height = 600, fps = 60, title = "simulation"):
    self.width = width
    self.height = height
    self.fps = fps
    self.title = title
    self.robots = []
    self.sites = []
    self.best = 0 # id of the best site
    self.free = free
    self.polling = polling
    self.right = right
    self.wrong = wrong
    self.params = params
    self.initRobots()
    self.initSites()
    pygame.init()

  # initialize robots, assign each a unique ID
  def initRobots(self):
    for i in range(NROBOT):
      if i < N_CHEATER:
        robot = Agent(i, self, param = (self.params[i]),faulty = True)
      else:
        robot = Agent(i, self, param = (self.params[i]))
      self.robots.append(robot)

  # right now assign the site with a deterministic quality
  def initSites(self):
    best_site = 0
    best_quality = -1
    for i in range(NSITE):
      site = Target(i)
      # make sure no overlap in site
      while i > 0 and inrange(site.loc, self.sites[i-1].loc, SITE_RAD * 3):
        site = Target(i)
      if site.quality > best_quality:
        best_quality = site.quality
        best_site = i
      self.sites.append(site)
    self.best = best_site + 1

  # things done at each iteration
  def timerFired(self, dt):
    '''each robot first sample, if they are committed, then they advertise, 
     and all robots check what they have received
     '''
    for robot in self.robots:
      robot.sample()
      robot.advertise()
    for robot in self.robots:
      robot.receiveOpinion()
    for robot in self.robots:
      robot.move()
    n_poll, n_commit, n_correct = 0,0,0
    for robot in self.robots:
      if robot.state == 1:
        n_poll += 1
      if robot.state == 2:
        n_commit += 1
        if robot.site == self.best:
          n_correct += 1
    fp = n_poll / NROBOT
    fc = n_commit / NROBOT
    fright = n_correct / NROBOT
    n_wrong = n_commit - n_correct
    fwrong = n_wrong / NROBOT
    ff = 1 - fp - fc
    self.polling.append(fp)
    self.right.append(fright)
    self.wrong.append(fwrong)
    self.free.append(ff)

  def drawAll(self, screen): ## visualization
    for i in range(len(self.sites)):
      site = self.sites[i]
      clr = SITE_PALETTE[i]
      pygame.draw.circle(screen, clr, site.loc, site.radius, width=2)

    for robot in self.robots:
      if robot.state == NOIDEA: color = GREEN
      elif robot.state == POLLING: color = YELLOW
      else: color = BOT_PALETTE[robot.site - 1]
      if robot.faulty: edge_color = PURPLE
      else: edge_color = (0,0,0)
      pygame.draw.circle(screen, color, (int(robot.x), int(robot.y)), robot.r)
      pygame.draw.circle(screen, edge_color, (int(robot.x), int(robot.y)), robot.r, width = 1)

  def run(self):
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((self.width, self.height))
    pygame.display.set_caption(self.title)
    screen.fill((255,255,255))
    cnt = 0
    while cnt < N_ITER:
      time = clock.tick(self.fps)
      cnt += 1
      # invoke everything that are supposed to happen in one time step
      self.timerFired(time) 
      # draw things
      screen.fill((255,255,255))
      self.drawAll(screen)
      pygame.display.flip()
    pygame.quit()

def run_trial(i, params):
  frac_free = []
  frac_polling = []
  frac_correct = []
  frac_wrong = []
  if VISUAL:
    game = PygameGame(params, frac_free, frac_polling, frac_correct, frac_wrong)
  else:
    game = MyGame(params, frac_free, frac_polling, frac_correct, frac_wrong)
  game.run()
  
  corrects = np.array(frac_correct[-n_keep:]).reshape((n_keep,1))
  pollings = np.array(frac_polling[-n_keep:]).reshape((n_keep,1))
  wrongs = np.array(frac_wrong[-n_keep:]).reshape((n_keep,1))
  frees = np.array(frac_free[-n_keep:]).reshape((n_keep,1))
  return (frees, pollings, corrects, wrongs)

def next_gen(population, scores, model = MODEL):
  ''' take parameters and scores from the previous generation and produce the 
      parameters for the next generation
      @param: model: 
  '''
  prob = softmax(scores)
  indices = [i for i in range(GRAPH_SIZE)]
  if model == WELLMIXED:
    for _ in range(GRAPH_SIZE):
      tobirth = np.random.choice(indices, p=prob)
      togo = np.random.randint(0, GRAPH_SIZE)
      if np.random.uniform(0,1) < MUTATION_RATE:
        (c1,c2) = population[tobirth]
        c1 = c1 + np.random.normal(-0.1, 0.1)
        c2 = 1 - c1
        population[togo] = (c1,c2)
      else:
        population[togo] = population[tobirth]
  elif model == STAR:
    for _ in range(GRAPH_SIZE):
      tobirth = np.random.choice(indices, p=prob)
      togo = np.random.choice(stargraph[tobirth])
      population[togo] = population[tobirth]
      if np.random.uniform(0,1) < MUTATION_RATE:
        (c1,c2) = population[tobirth]
        c1 = c1 + np.random.normal(-0.1, 0.1)
        c2 = 1 - c1
        population[tobirth] = (c1,c2)
  elif model == RING:
    for _ in range(GRAPH_SIZE):
      tobirth = np.random.choice(indices, p=prob)
      togo = np.random.choice(ringgraph[tobirth])
      population[togo] = population[tobirth]
      if np.random.uniform(0,1) < MUTATION_RATE:
        (c1,c2) = population[tobirth]
        c1 = c1 + np.random.normal(-0.1, 0.1)
        c2 = 1 - c1
        population[tobirth] = (c1,c2)
  else: 
    print("PANIC! No evolution model selected")
    raise Exception
  return population

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
  score = r[n_keep-1, 0]

  if PLOT and score > 0.3:
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
    else: plt.savefig(f"./figures/{MODEL}_noadversary_average_{param[0]}.jpg")
    return score

if __name__ == '__main__':
  tic = time.perf_counter()
  '''initialize n = graph_size sets of parameters'''
  all_scores = np.zeros((N_GEN,1))
  rand = [np.random.uniform(0, 0.05) for _ in range(GRAPH_SIZE)]
  params = [(1-r, r) for r in rand]
  params = np.array(params,dtype="f,f")
  print("param:", params)
  # add some noise
  for gen in range(N_GEN):
    scores = np.zeros((GRAPH_SIZE, ))
    for i in range(GRAPH_SIZE):
      param = params[i]
      score = run_one_sim(param)
      scores[i] = score
    '''maybe print the avg score of each generation'''
    print(np.mean(scores))
    all_scores[gen] = np.mean(scores)
    params = next_gen(params, scores)
  plt.clf()
  plt.plot(all_scores)
  plt.ylabel("best proportion of correct agents in each generation")
  plt.ylim(0,1)
  plt.savefig(f"./figures/{MODEL}_{N_CHEATER}_adv_over_{N_GEN}generations.jpg")
  toc = time.perf_counter()
  print(f"Duration: {toc - tic:0.4f} seconds")
