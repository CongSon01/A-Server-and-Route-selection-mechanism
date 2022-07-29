import sys, random
import numpy as np
sys.path.append('/home/onos/Downloads/A-Server-and-Route-selection-mechanism/flaskAPI/q_learning')
sys.path.append('/home/onos/Downloads/A-Server-and-Route-selection-mechanism/flaskAPI/handledata/models')

import custom_env
def get_x(x):
    if (x >= 4):
        return 4
    elif (x <= 0):
        return 1
    else:
        return x

def f(x, r, w):
    # print(r, w)
    return {
        0: (get_x(r - 1), get_x(w - 1)),
        1: (get_x(r - 1), get_x(w)),
        2: (get_x(r - 1), get_x(w + 1)),
        3: (get_x(r), get_x(w - 1)),
        4: (get_x(r), get_x(w)),
        5: (get_x(r), get_x(w + 1)),
        6: (get_x(r + 1), get_x(w - 1)),
        7: (get_x(r + 1), get_x(w)),
        8: (get_x(r + 1), get_x(w + 1)),
    }[x]

env = custom_env.Custom_env()
R = 2
W = 2
RD = random.sample(range(0, 5), 5)
WD = random.sample(range(0, 5), 5)
V_staleness = random.sample(range(5, 15), 5)

qtable_new = np.load('qtable.npy')
for i in range(5):
    state = env.reset()
    # print("STATE", state)
    step = 0
    done = False
    # print(qtable_new[state, :])

    env.render()
    # Take the action (index) that have the maximum expected future reward given that state
    if sum(qtable_new[state, :]) == 0:
        action = random.randint(0, 8)
    else:
        action = np.argmax(qtable_new[state,:])

    R, W = f(action, R, W)
    print('R : ',R, 'W :', W)
    new_state, reward, done = env.step(RD[i], WD[i], V_staleness[i])
        
    if done:
        break
    state = new_state