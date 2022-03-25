import random, math,time
import numpy as np
import matplotlib.pyplot as plt
from networkx.drawing.nx_pydot import *
from network import *

'''
landscape for S1 S2 R1 R2
evo allowing both mutations
'''
N_ITER = 5000 # per trial
n_keep = N_ITER
MUTATION_RATE = 0.02

N_TRIALS = 20

MAPSIZE = 400
# agent states
NOIDEA = 0
POLLING = 1
COMMITTED = 2
# agent param
AGENT_STEPSIZE = 4
AGENT_RADIUS = 10
NROBOT = 15
COMM_RANGE = 60
# sites param
NSITE = 2
SITE_RAD = 60

WELLMIXED = 0
RING = 1
STAR = 2
d = {0:"wellmixed",1:"ring",2:"star"}

class Channel():
    def __init__(self, sd): # sd = standard deviation: int / float
        if not (isinstance(sd, int) or isinstance(sd, float)):
            raise "standard deviation should be numerical"
        self.sd = sd
    
    def __eq__(self,other):
        return self.sd == other.sd
    
    def send(self, val):
        (x,y) = val
        x_noise = np.random.normal(0, self.sd)
        y_noise = np.random.normal(0, self.sd)
        return (x+x_noise, y+y_noise)

# comm channels
S1 = Channel(SITE_RAD )
S2 = Channel(SITE_RAD / 3)

def inrange(a,b,r):
  '''check if 2 centers of circle (a,b) are in range r, inrage -> True
  @params a, b: tuples, coordinate on a plane;
  @param r: allowed distance between a and b
  @ensures True if dist(a,b) <= r, False otherwise'''
  (x1,y1) = a
  (x2,y2) = b
  return (x1 - x2)**2 + (y1 - y2)**2 <= r**2

class Agent():
  def __init__(self, id, server, param = (1,0)):
    '''initialize agent'''
    self.id = id
    self.x = (np.random.normal(MAPSIZE/2, MAPSIZE/2))%MAPSIZE
    self.y = (np.random.normal(MAPSIZE/2, MAPSIZE/2))%MAPSIZE# random.random() * MAPSIZE
    self.r = AGENT_RADIUS
    self.state = NOIDEA
    self.speculation = (-1, -1) # for cross inhib model
    self.opinion = (-1, -1) # should be location of commited site
    self.site = 0 # id of the committed site?
    self.quality = 0 # have not seen any
    self.broadcasting = None
    self.server = server
    self.schannel = S1 #s1r1 s1r2 s2r1 s2r2
    self.rchannel = S1
  def __eq__(self, other):
    return self.id == other.id

  def move(self):
    '''if self.state == NOIDEA / COMMITTED: simulate a brownian motion in 2D
       otherwise: move towards speculation with noise of 0.1 standard normal,
       stepsize also follows a normal distribution'''
    
    if self.state in [NOIDEA, COMMITTED]:
      '''simulating  Brownian motion'''
      stepsize = np.random.normal(AGENT_STEPSIZE, AGENT_STEPSIZE)
      direction = random.random() * math.pi * 2 # all directions
      dx = stepsize * math.cos(direction)
      dy = stepsize * math.sin(direction)
    
    # in polling state, it will move in the general direction of the potential target, 
    # with variation of a standard normal in radian
    elif self.state == POLLING: # move towards target with some noise
      if inrange((self.x,self.y),self.speculation, AGENT_STEPSIZE*2):
        self.state = NOIDEA
        dx, dy = np.random.normal(AGENT_STEPSIZE, AGENT_STEPSIZE),np.random.normal(AGENT_STEPSIZE, AGENT_STEPSIZE)
      else:
        stepsize = np.random.normal(AGENT_STEPSIZE / 2, AGENT_STEPSIZE)
        tmp = np.random.standard_normal()
        xdiff, ydiff = self.speculation[0] - self.x, self.speculation[1] - self.y
        theta = math.atan2(ydiff, xdiff) + tmp/2
        dx = stepsize * math.cos(theta)
        dy = stepsize * math.sin(theta)
      
    self.x = (self.x + dx) % self.server.width
    self.y = (self.y + dy) % self.server.height
  
  def advertise(self):
    '''committed cells broadcast their opinion with probability of the quality sampled'''
    if self.state == COMMITTED and np.random.uniform() < self.quality:
        self.broadcasting = self.schannel.send(self.opinion)
    else: self.broadcasting = None

  
  def receiveOpinion(self):
    '''randomly select a message among all robots in range that are broadcasting
    in that iteration'''
    friendlist = []
    for friend in self.server.robots:
      if self == friend: continue
      if inrange((self.x,self.y), (friend.x, friend.y), COMM_RANGE):
        if friend.broadcasting != None and \
            (friend.schannel == self.rchannel):
          friendlist.append(friend)
    if len(friendlist) == 0: 
      return
    message = random.choice(friendlist)
    '''estimate of the true quality of the site heard'''
    # total_qual = self.quality + quality

    # if robot in commited state, 
    # it retains its state with probability of the quality it sampled
    rand_n = np.random.uniform()
    if self.state == COMMITTED and self.site != message.site:
      if rand_n > self.quality:
        self.state = NOIDEA
        self.site = 0
        self.quality = 0
    elif self.state == COMMITTED:
      return  
    else: 
      if self.state == POLLING:
        if rand_n > 0.5:
          self.speculation = message.broadcasting
      else: # should be noidea here
        self.state = POLLING
        self.speculation = message.broadcasting
        self.quality = 0
        
        
  def sample(self):
    '''at every iteration, if an agent is in range of a target, 
    it will sample the site quality with some random noise'''
    for site in self.server.sites:
      if inrange((self.x,self.y),site.loc, SITE_RAD):
        if self.state == COMMITTED:
          if not inrange(self.opinion, site.loc, SITE_RAD):
            # if it's not my site
            quality = max(np.random.normal(0,0.1) + site.quality, 1)
            if quality > self.quality or np.random.uniform() > self.quality:
              self.opinion = (self.x, self.y)
              self.site = site.id
              self.quality = quality
          else:
              self.quality = max(np.random.normal(0,0.1) + site.quality, 1)
        else:
          self.state = COMMITTED
          self.opinion = (self.x, self.y)
          self.site = site.id
          self.quality = max(np.random.normal(0,0.1) + site.quality, 1)
          return

class Target():
  def __init__(self, id):
    self.radius = SITE_RAD
    if id == 0:
      self.loc = (100, 100)
    else:
      self.loc = (300, 300)
    # self.loc = (int(np.random.normal(MAPSIZE/2, MAPSIZE/2)) % MAPSIZE, \
    #            int(np.random.normal(MAPSIZE/2, MAPSIZE/2)) % MAPSIZE)
    self.id = id + 1
    if self.id == 1: self.quality = 0.9
    else: self.quality = 0.1

class MyGame():
  def __init__(self, model, graph, width = 600, height = 600, fps = 60, title = "simulation"):
    self.width = width
    self.height = height
    self.fps = fps
    self.title = title
    self.robots = []
    self.sites = []
    self.free = []
    self.polling = []
    self.right = []
    self.wrong = []
    self.s1r1 = []
    self.s2r1 = []
    self.s1r2 = []
    self.s2r2 = []
    self.best = 0 # id of the best site
    self.model = model
    self.graph = graph
    self.initRobots()
    self.initSites()
    self.mutant = 0

  # initialize robots, assign each a unique ID
  def initRobots(self):
    for i in range(NROBOT):
      robot = Agent(i, self)
      self.robots.append(robot)

  # right now assign the site with a deterministic quality
  def initSites(self):
    best_site = 0
    best_quality = -1
    for i in range(NSITE):
      site = Target(i)
      # make sure no overlap in site
      # while i > 0 and inrange(site.loc, self.sites[i-1].loc, SITE_RAD * 3):
        # site = Target(i)
      if site.quality > best_quality:
        best_quality = site.quality
        best_site = i
      self.sites.append(site)
    self.best = best_site + 1
    
  def next_gen(self, scores):
    ''' take parameters and scores from the previous generation and produce the 
        parameters for the next generation
        @param: model
    '''
    model = self.model
    prob = softmax(scores)
    # print(scores, prob)
    indices = [i for i in range(GRAPH_SIZE)]
    if model == WELLMIXED:
        for _ in range(GRAPH_SIZE):
            tobirth = np.random.choice(indices, p=prob)
            togo = np.random.randint(0, GRAPH_SIZE)
            while togo == tobirth: # make sure it's not same node
              togo = np.random.randint(0, GRAPH_SIZE)
    elif model == STAR:
        for _ in range(GRAPH_SIZE):
            tobirth = np.random.choice(indices, p=prob)
            togo = np.random.choice(stargraph[tobirth])
    elif model == RING:
        for _ in range(GRAPH_SIZE):
            tobirth = np.random.choice(indices, p=prob)
            togo = np.random.choice(ringgraph[tobirth])
    else: 
        print("PANIC! No evolution model selected")
        raise Exception
    self.robots[togo].schannel = self.robots[tobirth].schannel
    self.robots[togo].rchannel = self.robots[tobirth].rchannel
    if np.random.uniform() < MUTATION_RATE:
        if np.random.uniform() > 0.5:
          self.robots[togo].schannel = S2
        else:
          self.robots[togo].rchannel = S2

  # things done at each iteration
  def timerFired(self, plot_state = True):
    '''
    plot_state = True <-> plot state,
    else will plot strains ie. channels
    - each robot first sample, if they are committed, then they advertise, 
    and all robots check what they have received
     '''
    for robot in self.robots:
      robot.sample()
      robot.advertise()
    for robot in self.robots:
      robot.receiveOpinion()
    for robot in self.robots:
      robot.move()
      
    ###############################################
    #####           for plots                 #####
    if plot_state:
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
    else:
      n_s1, n_s1r1, n_r1 = 0,0,0
      for robot in self.robots:
        both = 0
        if robot.schannel == S1:
          n_s1 += 1
          both += 1
        if robot.rchannel == S1:
          n_r1 += 1
          both += 1
        if both == 2:
          n_s1r1 += 1
      n_s2 = NROBOT - n_s1
      n_r2 = NROBOT - n_r1
      n_s1r2 = n_s1 - n_s1r1
      n_s2r2 = n_r2 - n_s1r2
      n_s2r1 = n_s2 - n_s2r2
      assert(n_s1r1 + n_s1r2 + n_s2r1 + n_s2r2 == NROBOT)
      self.s1r1.append(n_s1r1 / NROBOT)
      self.s1r2.append(n_s1r2 / NROBOT)
      self.s2r1.append(n_s2r1 / NROBOT)
      self.s2r2.append(n_s2r2 / NROBOT)
        
    #####            end plots                #####
    ###############################################
    
    # add some mutation and evolution code here
    qual = [bot.quality for bot in self.robots]
    if not plot_state: self.next_gen(qual)
    
    
  def run(self, plot_state = True):
    self.cnt = 0
    while self.cnt < N_ITER:
      self.cnt += 1
      # invoke everything that are supposed to happen in one time step
      self.timerFired(plot_state) 
    print(".",end="",flush=True)
  
  def reshape(self, arr):
    return np.array(arr).reshape((n_keep,1))
  
  def run_trials(self):
    f, p, r, w = np.zeros((n_keep, 1)),np.zeros((n_keep, 1)),\
                np.zeros((n_keep, 1)),np.zeros((n_keep, 1))  
    for i in range(N_TRIALS):
      self.__init__(model=self.model, graph = self.graph)
      self.run()
      f = np.add(f, self.reshape(self.free))
      p = np.add(p, self.reshape(self.polling))
      r = np.add(r, self.reshape(self.right) )
      w = np.add(w, self.reshape(self.wrong))
    f = np.divide(f, N_TRIALS)
    p = np.divide(p, N_TRIALS)
    r = np.divide(r, N_TRIALS)
    w = np.divide(w, N_TRIALS)
    plt.clf()
    plt.plot(f, label = 'no idea')
    plt.plot(p, label = 'polling')
    plt.plot(r, label = 'correct site')
    plt.plot(w, label = 'incorrect site')
    plt.ylabel("proportion of agents in each state")
    plt.ylim(0,1)
    plt.legend()
    if self.robots[0].schannel == S1:
      str1 = 's1'
    else: str1 = 's2'
    if self.robots[0].rchannel == S1:
      str2 = 'r1'
    else: str2 = 'r2'
    plt.savefig(f"landscape{str1}{str2}.jpg")
    
  def run_evo(self):
    s1r1, s1r2, s2r1, s2r2 = np.zeros((n_keep, 1)),np.zeros((n_keep, 1)),\
                np.zeros((n_keep, 1)),np.zeros((n_keep, 1))  
    for i in range(N_TRIALS):
      self.__init__(model=self.model, graph = self.graph)
      self.run(plot_state = False)
      s1r1 = np.add(s1r1, self.reshape(self.s1r1))
      s1r2 = np.add(s1r2, self.reshape(self.s1r2))
      s2r1 = np.add(s2r1, self.reshape(self.s2r1) )
      s2r2 = np.add(s2r2, self.reshape(self.s2r2))
    s1r1 = np.divide(s1r1, N_TRIALS)
    s1r2 = np.divide(s1r2, N_TRIALS)
    s2r1 = np.divide(s2r1, N_TRIALS)
    s2r2 = np.divide(s2r2, N_TRIALS)
    plt.clf()
    plt.plot(s1r1, label = 'S1R1')
    plt.plot(s1r2, label = 'S1R2')
    plt.plot(s2r1, label = 'S2R1')
    plt.plot(s2r2, label = 'S2R2')
    plt.ylabel("proportion of agents in each state")
    plt.ylim(0,1)
    plt.legend()
    plt.savefig(f"evo_{d[self.model]}_{N_ITER}timesteps_{N_TRIALS}runs.jpg")

def softmax(scores,temp=5.0):
    ''' transforms scores to probabilites '''
    '''exp = np.exp(np.array(scores)/temp)
    return exp/exp.sum()'''
    if sum(scores) == 0:
        return [1 / len(scores) for _ in range(len(scores))]
    else:
        return np.array(scores) / sum(scores)

if __name__ == '__main__':
    if (len(sys.argv)) > 1:
      model = sys.argv[1]
      if model == "star":
          G = stargraph
          model = STAR
      elif model == "ring":
          G = (ringgraph)
          model = RING
      else:
          G = (wellmixed)
          model = WELLMIXED
    else:
      model=0
      G=wellmixed
    game = MyGame(model, G)
    if (len(sys.argv)) > 1:
      game.run_evo()
    else: game.run_trials()
    