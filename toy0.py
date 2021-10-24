import random, math, pygame
import numpy as np

## PARAMETERS

# duration of simulation
n_iter = 1500
# some global variables
MAPSIZE = 600
# agent states
NOIDEA = 0
POLLING = 1
COMMITTED = 2
# agent param
STEPSIZE = 3
RADIUS = 10
NROBOT = 20
COMM_RANGE = 20
# sites param
NSITE = 1
SITE_RAD = 75
# colors
red = pygame.Color('#ff1744')
yellow = pygame.Color('#FFEA00')
purple = pygame.Color('#ea80fc')
green = pygame.Color('#4caf50')
blue = pygame.Color('#42a5f5')

# check if 2 centers of circle (a,b) are in range r, inrage => True
def inrange(a,b,r):
  (x1,y1) = a
  (x2,y2) = b
  return (x1 - x2)**2 + (y1 - y2)**2 <= r**2

# class for agent / robot
class Agent():
  # initialization
  def __init__(self, id, server):
    self.id = id
    self.x = random.random() * MAPSIZE
    self.y = random.random() * MAPSIZE
    self.r = 10
    self.state = NOIDEA
    self.speculation = (-1, -1) # for cross inhib model
    self.opinion = (-1, -1) # should be location of commited site
    self.quality = -1 # have not seen any
    self.broadcasting = None
    self.server = server

  def __eq__(self, other):
    return self.id == other.id

  def move(self):
    # if no idea, will move in a random directions for a fixed distance
    if self.state in [NOIDEA, COMMITTED]:
      direction = random.random() * math.pi * 2 # all directions
      dx = STEPSIZE * math.cos(direction)
      dy = STEPSIZE * math.sin(direction)
    
    # in polling state, it will move in the general direction of the potential target, with variation of a standard normal in radian
    elif self.state == POLLING: # move towards target with some noise
      tmp = np.random.standard_normal()
      xdiff, ydiff = max(0.001, self.speculation[0] - self.x), self.speculation[1] - self.y
      theta = math.tanh(ydiff / xdiff) + tmp
      dx = STEPSIZE * math.cos(theta)
      dy = STEPSIZE * math.sin(theta)
    self.x = (self.x + dx) % self.server.width
    self.y = (self.y + dy) % self.server.height
  
  # committed cells broadcast their opinion with probability of the quality sampled
  def advertise(self):
    if self.state == COMMITTED:
      if random.random() < self.quality:
        self.broadcasting = self.opinion
      else: self.broadcasting = None

  # randomly select a message among all robots in range that are broadcasting in that iteration
  def receiveOpinion(self):
    friendlist = []
    for friend in self.server.robots:
      if self == friend: continue
      if inrange((self.x,self.y), (friend.x, friend.y), COMM_RANGE):
        if friend.broadcasting != None:
          friendlist.append(friend)
    if len(friendlist) == 0: 
      return
    message = random.choice(friendlist)
    # if robot in commited state, it retains its state with probability of the quality it sampled
    if self.state == COMMITTED:
      if random.random() < self.quality:
        return
      # if it's the same site, ignore the message
      elif inrange(self.opinion, message.broadcasting, SITE_RAD):
        return
      # else change to no-idea state
      else:
        self.state = NOIDEA
    else: # else enter polling state 
      self.state = POLLING
      self.speculation = message.broadcasting

  # at every iteration, if an agent is in range of a target, it will sample the site quality with some probability of error
  def sample(self):
    for site in self.server.sites:
      if inrange((self.x,self.y),(site.x,site.y), site.radius + self.r):
        if random.random() < site.quality:
          self.state = COMMITTED
          self.opinion = (self.x, self.y)
          self.quality = max(0.2 * np.random.standard_normal() + site.quality, 0,99999)
          return

class Target():
  def __init__(self, id, quality):
    self.radius = SITE_RAD
    self.x = random.random() * MAPSIZE
    self.y = random.random() * MAPSIZE
    self.id = id + 1
    self.quality = quality

class PygameGame(object):
  def __init__(self, width = 600, height = 600, fps = 30, title = "simple simulation"):
    self.width = width
    self.height = height
    self.fps = fps
    self.title = title
    self.robots = []
    self.sites = []
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
    for i in range(NSITE):
      site = Target(i, 0.8)
      self.sites.append(site)

  # things done at each iteration
  def timerFired(self, dt):
    # each robot first sample, then those committed advertise, and all robots check what they have received
    for robot in self.robots:
      robot.sample()
      robot.advertise()
    for robot in self.robots:
      robot.receiveOpinion()
    # lastly, each makes their own move based on the information and updates in the latest iteration
    for robot in self.robots:
      robot.move()

  def drawAll(self, screen): ## visualization
    for site in self.sites:
      pygame.draw.circle(screen, red, (int(site.x), int(site.y)), site.radius)

    for robot in self.robots:
      if robot.state == NOIDEA: color = green
      elif robot.state == POLLING: color = yellow
      else: color = blue
      pygame.draw.circle(screen, color, (int(robot.x), int(robot.y)), robot.r)
      pygame.draw.circle(screen, (0,0,0), (int(robot.x), int(robot.y)), robot.r, True)

  def run(self):
    print("running")
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((self.width, self.height))
    pygame.display.set_caption(self.title)
    screen.fill((255,255,255))

    cnt = 0
    while cnt <= n_iter:
      time = clock.tick(self.fps)
      cnt += 1
      self.timerFired(time) # invoke everything that are supposed to happen in one time step
      screen.fill((255,255,255))
      self.drawAll(screen)
      pygame.display.flip()
    pygame.quit()

game = PygameGame()
print("ready?")
game.run()
