from RL_brain import QLearningTable
from env2 import stock
from random import *
import matplotlib.pyplot as plt
import numpy as np

def update():
    #fig1 = plt.figure()  
    #plt.ion() 
        

    for episode in range(1000):
        if episode%200==0:
            step = 0    
        #plt.cla()
        # initial observation
        state = env.reset()

        for i in range(500):
            
            # RL choose action based on observation
            action = RL.choose_action(str(state))

            # RL take action and get next observation and reward
            state, reward,_state= env.step(action)
            #print(action)

            # RL learn from this transition
            RL.learn(str(state), action, reward, str(_state))

            # swap observation
            env.s=_state

            # break while loop when end of this episode
            
        if episode%10==0:
            print("episode = ",episode)
            print("performance: ",env.user.profitfactor)
            try:
                RL.q_table.to_csv("ql_brain.csv")
            except:
                print("output failed")
        env.performance=[]

        
    #plt.ioff()
    #plt.show()

if __name__ == "__main__":
    env = stock()
    RL = QLearningTable(actions=list(range(-1,env.n_actions)))

    update()
    RL.q_table.to_csv("ql_brain.csv")
    #print(RL.memory.tolist())
    
    """    
    while(not done):
        print("close:",env.db.data[4])
        observation_, reward, done=env.step(randint(0,3))
        print("observation_")
        i+=1
    print ("performance: ",env.performance)
    """
