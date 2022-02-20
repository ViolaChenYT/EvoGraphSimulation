"""
source: https://github.com/wfleshman/Evolving_To_Walk
@author: bill
"""
import gym
import numpy as np
from copy import deepcopy
import matplotlib.pyplot as plt
import math
from togif import*

VERBOSE = True
frames = []

def glorot_uniform(n_inputs,n_outputs,multiplier=1.0):
    ''' Glorot uniform initialization '''
    glorot = multiplier*np.sqrt(6.0/(n_inputs+n_outputs))
    return np.random.uniform(-glorot,glorot,size=(n_inputs,n_outputs))

def softmax(scores,temp=5.0):
    ''' transforms scores to probabilites '''
    exp = np.exp(np.array(scores)/temp)
    return exp/exp.sum()

class Agent(object):
    ''' each agent is still a neural network
        - it controls 4 motors, each take range (0,1)
        - maybe, try learning each of these individually?
    '''
    
    def __init__(self, n_inputs, n_hidden, n_outputs, mutate_rate=.05, init_multiplier=1.0):
        ''' Create agent's brain '''
        self.n_inputs = n_inputs
        self.n_hidden = n_hidden
        self.n_outputs = n_outputs
        self.mutate_rate = mutate_rate
        self.init_multiplier = init_multiplier
        ''' assume the network to have 2 layers '''
        self.network = {'Layer 1' : glorot_uniform(n_inputs, n_hidden,init_multiplier),
                        'Bias 1'  : np.zeros((1,n_hidden)),
                        'Layer 2' : glorot_uniform(n_hidden, n_outputs,init_multiplier),
                        'Bias 2'  : np.zeros((1,n_outputs))}
                        
    def act(self, state):
        ''' Use the network to decide on an action '''        
        if(state.shape[0] != 1):
            state = state.reshape(1,-1)
        net = self.network
        layer_one = np.tanh(np.matmul(state,net['Layer 1']) + net['Bias 1'])
        layer_two = np.tanh(np.matmul(layer_one, net['Layer 2']) + net['Bias 2'])
        return layer_two[0]
    
    def __add__(self, another):
        ''' overloads the + operator for breeding'''
        # copying parent
        child = Agent(self.n_inputs, self.n_hidden, self.n_outputs, self.mutate_rate, self.init_multiplier)
        for key in child.network: # what is key
            n_inputs,n_outputs = child.network[key].shape
            mask = np.random.choice([0,1],size=child.network[key].shape,p=[.5,.5])
            random = glorot_uniform(mask.shape[0],mask.shape[1])
            child.network[key] = np.where(mask==1,self.network[key],another.network[key])
            mask = np.random.choice([0,1],size=child.network[key].shape,p=[1-self.mutate_rate,self.mutate_rate])
            # children's network is some random modification of parent's network
            child.network[key] = np.where(mask==1,child.network[key]+random,child.network[key])
        return child
    
def run_trial(env,agent,verbose=VERBOSE):
    ''' an agent performs 3 episodes of the env '''
    totals = []
    n_run = 3
    for _ in range(n_run):
        state = env.reset()
        if verbose: frames.append(env.render())
        total = 0
        done = False
        cnt = 0
        while not done:
            state, reward, done, _ = env.step(agent.act(state))
            if verbose and (cnt % 10 == 0): frames.append(env.render())
            total += reward
            cnt += 1
        totals.append(total)
    return sum(totals)/n_run

def next_generation(env,population,scores,temperature):
    ''' breeds a new generation of agents '''
    scores, population =  zip(*sorted(zip(scores,population),reverse=True))
    upper = math.ceil(len(population)/4)
    children = list(population[:upper]) # next gen is the best quarter + random choice from last gen
    parents = list(np.random.choice(population,size=2*(len(population)-len(children)),p=softmax(scores,temperature)))
    children = children + [parents[i]+parents[i+1] for i in range(0,len(parents)-1,2)]
    scores = [run_trial(env,agent) for agent in children]

    return children,scores

def main():
    ''' main function '''
    # Setup environment
    env = gym.make('BipedalWalker-v3')
    env.seed(0)
    np.random.seed(0)
    
    # network params
    n_inputs = env.observation_space.shape[0]
    n_actions = env.action_space.shape[0]
    n_hidden = 512
    multiplier = 5
    
    # Population params
    pop_size = 50
    mutate_rate = .3
    softmax_temp = 5.0
    
    # Training
    n_generations = 2
    population = [Agent(n_inputs,n_hidden,n_actions,mutate_rate,multiplier) for i in list(range(pop_size))]
    scores = [run_trial(env,agent) for agent in population]
    best = [deepcopy(population[np.argmax(scores)])]
    for generation in list(range(n_generations)):
        score_arr = []
        population,scores = next_generation(env,population, scores,softmax_temp)
        best.append(deepcopy(population[np.argmax(scores)]))
        score = np.max(scores)
        print ("Generation:",generation,"Score:",score)
        score_arr.append(score)
    
    fig = plt.figure()
    plt.plot(score_arr)
    plt.ylabel('Score')
    plt.xlabel('Episode #')
    plt.show()

    # Record every agent
    '''env = gym.wrappers.Monitor(env,'/tmp/walker',force=True,video_callable=lambda episode_id: episode_id%3==0)   
    for agent in best:
        run_trial(env,agent)
    env.close()'''
    save_frames_as_gif(frames)
    
if __name__ == '__main__':
    main()
    