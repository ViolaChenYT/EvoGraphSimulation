import random, math, pygame
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_pydot import *

'''PARAMETERS'''

n_iter = 6000 
'''duration of simulation'''

MAPSIZE = 400
# agent states
NOIDEA = 0
POLLING = 1
COMMITTED = 2
# agent param
AGENT_STEPSIZE = 3.5
AGENT_RADIUS = 10
NROBOT = 20
COMM_RANGE = 60
# sites param
NSITE = 2
SITE_RAD = 60
# colors
RED = pygame.Color('#ff1744')
PINK = pygame.Color('#E30B5C')
YELLOW = pygame.Color('#FFEA00')
PURPLE = pygame.Color('#ea80fc')
GREEN = pygame.Color('#4caf50')
BLUE = pygame.Color('#42a5f5')
DARKBLUE = pygame.Color('#00008B')

SITE_PALETTE = [RED, DARKBLUE]
BOT_PALETTE = [PINK, BLUE]


def inrange(a,b,r):
  '''check if 2 centers of circle (a,b) are in range r, inrage -> True
  @params a, b: tuples, coordinate on a plane;
  @param r: allowed distance between a and b
  @ensures True if dist(a,b) <= r, False otherwise'''
  (x1,y1) = a
  (x2,y2) = b
  return (x1 - x2)**2 + (y1 - y2)**2 <= r**2

class Agent():
  def __init__(self, id, server, faulty = False):
    '''initialize agent'''
    self.id = id
    self.x = random.random() * MAPSIZE
    self.y = random.random() * MAPSIZE
    self.r = AGENT_RADIUS
    self.state = NOIDEA
    self.speculation = (-1, -1) # for cross inhib model
    self.opinion = (-1, -1) # should be location of commited site
    self.site = 0 # id of the committed site?
    self.quality = -1 # have not seen any
    self.broadcasting = None
    self.server = server
    self.faulty = faulty

  def __eq__(self, other):
    return self.id == other.id

  def move(self):
    '''if no idea, will move in a random directions for a fixed distance'''
    
    if self.state in [NOIDEA, COMMITTED]:
      stepsize = np.random.normal(1, AGENT_STEPSIZE)
      direction = random.random() * math.pi * 2 # all directions
      dx = stepsize * math.cos(direction)
      dy = stepsize * math.sin(direction)
    
    # in polling state, it will move in the general direction of the potential target, 
    # with variation of a standard normal in radian
    elif self.state == POLLING: # move towards target with some noise
      stepsize = np.random.normal(1, AGENT_STEPSIZE)
      tmp = np.random.standard_normal()
      xdiff, ydiff = self.speculation[0] - self.x, self.speculation[1] - self.y
      theta = math.atan2(ydiff, xdiff) + tmp
      dx = stepsize * math.cos(theta)
      dy = stepsize * math.sin(theta)
      
    self.x = (self.x + dx) % self.server.width
    self.y = (self.y + dy) % self.server.height
  
  def advertise(self):
    '''committed cells broadcast their opinion with probability of the quality sampled'''
    if self.state == COMMITTED and random.random() < self.quality:
        self.broadcasting = (self.opinion, self.quality)
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
    total_qual = self.quality + message.broadcasting[1]

    # if robot in commited state, 
    # it retains its state with probability of the quality it sampled
    if self.state == COMMITTED and self.site != message.site:
      if random.random() >= self.quality / total_qual:
        self.state = NOIDEA
        self.site = 0
    elif self.state == COMMITTED:
      return  
    else: # else enter polling state 
      if self.state == POLLING:
        if random.random() >= self.quality / total_qual:
          self.speculation = message.broadcasting[0]
          self.quality = message.broadcasting[1]
      else:
        assert(self.state != COMMITTED)
        self.state = POLLING
        self.speculation = message.broadcasting[0]
        self.quality = message.broadcasting[1]

  def sample(self):
    '''at every iteration, if an agent is in range of a target, 
    it will sample the site quality with some random noise'''
    for site in self.server.sites:
      if inrange((self.x,self.y),site.loc, SITE_RAD):
        if random.random() < site.quality:
          self.state = COMMITTED
          self.opinion = (self.x, self.y)
          self.site = site.id
          self.quality = max(np.random.normal(0,0.1) + site.quality, 0.99999)
          return

class Target():
  def __init__(self, id):
    self.radius = SITE_RAD
    self.loc = (int(random.random() * MAPSIZE), int(random.random() * MAPSIZE))
    self.id = id + 1
    if id == 0: self.quality = 0.7
    else: self.quality = 0.3 # random.random()

class PygameGame(object):
  def __init__(self, free, polling, right, wrong, width = 600, height = 600, fps = 60, title = "simulation"):
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
    self.initRobots()
    self.initSites()
    pygame.init()

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
      q = random.random()
      site = Target(i)
      # make sure no overlap in site
      while i > 0 and inrange(site.loc, self.sites[i-1].loc, SITE_RAD * 2):
        site = Target(i)
      if q > best_quality:
        best_quality = q
        best_site = i
      self.sites.append(site)
    self.best = best_site + 1

  # things done at each iteration
  def timerFired(self, dt):
    # each robot first sample, then those committed advertise, 
    # and all robots check what they have received
    for robot in self.robots:
      robot.sample()
      robot.advertise()
    for robot in self.robots:
      robot.receiveOpinion()
    # lastly, each makes their own move based on the information and 
    # updates in the latest iteration
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
      pygame.draw.circle(screen, color, (int(robot.x), int(robot.y)), robot.r)
      pygame.draw.circle(screen, (0,0,0), (int(robot.x), int(robot.y)), robot.r, True)

  def run(self):
    print("running")
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((self.width, self.height))
    pygame.display.set_caption(self.title)
    screen.fill((255,255,255))

    cnt = 0
    while cnt < n_iter:
      time = clock.tick(self.fps)
      cnt += 1
      # invoke everything that are supposed to happen in one time step
      self.timerFired(time) 
      # draw things
      screen.fill((255,255,255))
      self.drawAll(screen)
      pygame.display.flip()
    pygame.quit()



def run_trial():
  frac_free = []
  frac_polling = []
  frac_correct = []
  frac_wrong = []
  game = PygameGame(frac_free, frac_polling, frac_correct, frac_wrong)
  print("Red:", game.sites[0].quality)
  print("Blue:", game.sites[1].quality)
  print(game.best)
  game.run()

  plt.plot(frac_free, label = 'no idea')
  plt.plot( frac_polling, label = 'polling')
  plt.plot( frac_correct, label = 'correct site')
  plt.plot(frac_wrong, label = 'incorrect site')
  plt.ylabel("proportion of agents with each state")
  plt.ylim(0,1)
  plt.legend()
  # Display a figure.
  plt.savefig("./figures/2dnoadversary.jpg")

if __name__ == '__main__':
    run_trial()