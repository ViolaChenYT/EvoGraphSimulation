import random, math
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_pydot import *

N_CHEATER = 5
N_ITER = 6000 # per trial

MAPSIZE = 400
# agent states
NOIDEA = 0
POLLING = 1
COMMITTED = 2
# agent param
AGENT_STEPSIZE = 4
AGENT_RADIUS = 10
NROBOT = 15
COMM_RANGE = 80
# sites param
NSITE = 2
SITE_RAD = 60

def softmax(scores,temp=5.0):
    ''' transforms scores to probabilites '''
    exp = np.exp(np.array(scores)/temp)
    return exp/exp.sum()
  
def inrange(a,b,r):
  '''check if 2 centers of circle (a,b) are in range r, inrage -> True
  @params a, b: tuples, coordinate on a plane;
  @param r: allowed distance between a and b
  @ensures True if dist(a,b) <= r, False otherwise'''
  (x1,y1) = a
  (x2,y2) = b
  return (x1 - x2)**2 + (y1 - y2)**2 <= r**2

class Agent():
  def __init__(self, id, server, param = (1,0), faulty = False):
    '''initialize agent'''
    self.id = id
    self.x = (np.random.normal(MAPSIZE/2, MAPSIZE/2))%MAPSIZE
    self.y = (np.random.normal(MAPSIZE/2, MAPSIZE/2))%MAPSIZE# random.random() * MAPSIZE
    self.r = AGENT_RADIUS
    self.state = NOIDEA
    self.speculation = (-1, -1) # for cross inhib model
    self.opinion = (-1, -1) # should be location of commited site
    self.site = 0 # id of the committed site?
    self.quality = -1 # have not seen any
    self.broadcasting = None
    self.server = server
    self.faulty = faulty
    (c1,c2) = param
    self.c1 = c1
    self.c2 = c2

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
    if self.faulty:
      quality = 1 - self.quality
    else:
      quality = self.quality
    if self.state == COMMITTED and random.random() < self.quality:
        self.broadcasting = (self.opinion, quality)
    else: self.broadcasting = None

  
  def receiveOpinion(self):
    '''randomly select a message among all robots in range that are broadcasting
    in that iteration'''
    friendlist = []
    for friend in self.server.robots:
      if self == friend: continue
      if inrange((self.x,self.y), (friend.x, friend.y), COMM_RANGE):
        if friend.broadcasting != None:
          friendlist.append(friend)
    if len(friendlist) == 0: 
      return
    message = random.choice(friendlist)
    quality = self.c1 * message.broadcasting[1] + self.c2
    '''estimate of the true quality of the site heard'''
    # total_qual = self.quality + quality

    # if robot in commited state, 
    # it retains its state with probability of the quality it sampled
    rand_n = random.random()
    if self.state == COMMITTED and self.site != message.site:
      if quality > self.quality and rand_n < 0.1:
        self.state = NOIDEA
        self.site = 0
    elif self.state == COMMITTED:
      return  
    else: # else enter polling state 
      if self.state == POLLING:
        if quality > self.quality:
          self.speculation = message.broadcasting[0]
          self.quality = quality
      else: # should be noidea here
        self.state = POLLING
        self.speculation = message.broadcasting[0]
        self.quality = quality
        
        
  def sample(self):
    '''at every iteration, if an agent is in range of a target, 
    it will sample the site quality with some random noise'''
    for site in self.server.sites:
      if inrange((self.x,self.y),site.loc, SITE_RAD):
        if self.state == COMMITTED:
          if not inrange(self.opinion, site.loc, SITE_RAD):
            # if it's not my site
            quality = max(np.random.normal(0,0.1) + site.quality, 1)
            if quality > self.quality or random.random() > 0.999999:
              self.opinion = (self.x, self.y)
              self.site = site.id
              self.quality = quality
        else: #elif random.random() < site.quality:
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
    if self.id == 1: self.quality = 0.8
    else: self.quality = 0.2 # random.random()

class MyGame():
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
      # while i > 0 and inrange(site.loc, self.sites[i-1].loc, SITE_RAD * 3):
        # site = Target(i)
      if site.quality > best_quality:
        best_quality = site.quality
        best_site = i
      self.sites.append(site)
    self.best = best_site + 1
    print(".", end="",flush=True)

  # things done at each iteration
  def timerFired(self):
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

  def run(self):
    cnt = 0
    while cnt < N_ITER:
      cnt += 1
      # invoke everything that are supposed to happen in one time step
      self.timerFired() 
