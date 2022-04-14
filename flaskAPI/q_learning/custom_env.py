from gym import Env
from gym.spaces import Discrete, Box
import numpy as np
import random

class Custom_env(Env):
    def __init__(self):
        # Actions we can take: w+1, r+1, w-1, r-1, w+0
        self.action_space = Discrete(9)
        # Do thay doi min va max.
        # it nhat 1 may va nhieu nhat 4 may
        self.observation_space = 500
        # Set times
        self.times = 1

        # set state
        # self.state = 300 + random.randint(-3, 3)

        # tham so dau vao
        self.writeThreshold = 20
        self.readThreshold = 20
        self.V_stalenessThreshold = 5
        
    def step(self, RD, WD, V_staleness):
        # Apply action
        # W: w+1, r+1, w-1, r-1, w+0
        state = RD * 2 + WD

        # print('state: ', state)
        
        # Reduce 1 second
        self.times -= 1 
        
        # Calculate reward
        if WD<self.writeThreshold and RD<self.readThreshold: 
            reward = self.V_stalenessThreshold - V_staleness
        else: 
            reward = -100 
        
        # Check is done
        if self.times <= 0: 
            done = True
        else:
            done = False
        
        # Return step information
        return state, reward, done

    def render(self):
        # Implement viz
        pass
    
    def reset(self):
        self.times = 60 
        state = 300 + random.randint(-3, 3)
        return state