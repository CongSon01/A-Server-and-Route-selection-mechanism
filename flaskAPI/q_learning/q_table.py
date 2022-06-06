import sys, random
import numpy as np
sys.path.append('/home/onos/Downloads/flaskSDN/flaskAPI/q_learning')
sys.path.append('/home/onos/Downloads/flaskSDN/flaskAPI/handledata/models')

import custom_env

class Q_table(object):
    def __init__(self):
        self.env = custom_env.Custom_env()
        action_size = self.env.action_space.n
        state_size = self.env.observation_space
        # khoi tao q ban dau full 0
        self.qtable = np.zeros((state_size, action_size))

        self.learning_rate = 0.08           # Learning rate
        self.iteration = 100               # Max steps per episode
        self.gamma = 0.95                  # Discounting rate

        # Exploration parameters
        self.epsilon = 1.0                 # Exploration rate

        # max_epsilon = min_epsilon ( du lieu khai pha )
        self.max_epsilon = 0.5             # Exploration probability at start
        self.min_epsilon = 0.5             # Minimum exploration probability 
        self.decay_rate = 0.001             # Exponential decay rate for exploration prob

        # List of rewards
        self.rewards = []

    # 2 For life or until learning is stopped
    def get_q_table(self, RD, WD, V_staleness, episode):
        print(RD, WD, V_staleness, episode)
        # Reset the environment
        state = self.env.reset(RD, WD)
        done = False
        total_rewards = 0
        
        for step in range(self.iteration):
            # 3. Choose an action a in the current world state (s)
            ## First we randomize a number
            exp_exp_tradeoff = random.uniform(0, 1)
            
            ## If this number > greater than epsilon --> exploitation (taking the biggest Q value for this state)
            if exp_exp_tradeoff > self.epsilon:
                if state <= 10000:
                    action = np.argmax(self.qtable[state,:])

            # Else doing a random choice --> exploration
            else:
                action= self.env.action_space.sample()

            # Take the action (a) and observe the outcome state(s') and reward (r)
            new_state, reward, done = self.env.step(RD, WD, V_staleness)

            # Update Q(s,a):= Q(s,a) + lr [R(s,a) + gamma * max Q(s',a') - Q(s,a)]
            # qtable[new_state,:] : all the actions we can take from new state
            # print(f(action, R, W))
            # R, W = f(action, R, W)
            if ( new_state <= 10000 ):
                self.qtable[state, action] = self.qtable[state, action] + self.learning_rate * (reward + self.gamma * np.max(self.qtable[new_state, :]) - self.qtable[state, action])
            
            total_rewards =total_rewards + reward
            
            # Our new state is state
            state = new_state
            
            # If done (if we're dead) : finish episode
            if done == True: 
                break

        # Reduce epsilon (because we need less and less exploration)
        self.epsilon = self.min_epsilon + (self.max_epsilon - self.min_epsilon)*np.exp(-self.decay_rate*episode) 
        self.rewards.append(total_rewards)