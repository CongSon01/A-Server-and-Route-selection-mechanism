
import random
import sys
import numpy as np
sys.path.append('/home/onos/Downloads/flaskSDN/flaskAPI/q_learning')
import q_table
RD = random.sample(range(0, 5), 5)
WD = random.sample(range(0, 5), 5)
V_staleness = random.sample(range(5, 15), 5)

q_table = q_table.Q_table()

for i in range(5):
    # q_table.env.reset()
    q_table.get_q_table(RD[i], WD[i], V_staleness[i], i)

print(q_table.qtable)
np.save('qtable.npy',np.array(q_table.qtable))