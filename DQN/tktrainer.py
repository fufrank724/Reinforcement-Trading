#Q_Brain
from Qagent import Agent
#env
from env import SampleApp
#others
import pandas as pd
import numpy as np
import warnings,time,sys
from datetime import date,datetime
import random


def run(ifLoad=False):

    """ 
    for i in range(1000):        
        action=random.randint(0,1)
        env.step(action)
    """
    print("\nstart observing")
    
    if(ifLoad):
        agent.load()
    if(not ifLoad):
        for k in range(50):
            env.reset()
            for i in range(365):
                action=random.randint(0,1)
                s_t,reward,s_t1=env.step(action)
                terminal=(i==364)
                if((i*k)%100==0):
                    agent.store_transition(s_t, action, reward, s_t1, terminal)
                
                env.s_t=s_t1
    else:
        for k in range(50):
            s_t=env.reset()
            for i in range(365):
                action=agent.choose_action(s_t)
                s_t,reward,s_t1=env.step(action)
                terminal=(i==364)
                if((i*k)%100==0):
                    agent.store_transition(s_t, action, reward, s_t1, terminal)
                
                env.s_t=s_t1
    
    print("\nstart train")
    for episode in range(30000):
        s_t=env.reset()
        
        for i in range(365):
        
            action=agent.choose_action(s_t)
            s_t,reward,s_t1=env.step(action)
            terminal=(i==364)
            agent.store_transition(s_t, action, reward, s_t1,terminal)
            
            env.s_t=s_t1
            if terminal:
                s_t,reward,s_t1=env.step(env.state[1]*-1)
        if episode %4==0:
            agent.train()
            
        if episode %100==0:
            print("saving...")
            agent.save()
            print("save successfully!")
            print("Now episode is at ",episode)
        
    
        

if __name__    ==  "__main__":

    path="E:/Python/Python/jupyter/futures/TXF/TXF_day.CSV"

    input_data=pd.read_csv(path)
    i=datetime.strptime(input_data['date'][0], "%Y/%m/%d").strftime("%Y-%m-%d")
    for i in range(len(input_data['date'])):
        t=datetime.strptime(input_data['date'][i], "%Y/%m/%d").strftime("%Y-%m-%d")
        input_data=input_data.set_value(i,'date',t)

    #input_data=input_data.set_index(['date'])    
    #input_data.drop('date', axis=1, inplace=True)

    input_data.drop('open', axis=1, inplace=True)
    input_data.drop('high',axis=1, inplace=True)
    input_data.drop('low', axis=1, inplace=True)
    input_data.drop('quote', axis=1, inplace=True)
    input_data.drop('quote_b(3)', axis=1, inplace=True)
    input_data.drop('quote_a(3)', axis=1, inplace=True)
    input_data.drop('BIAS(5)', axis=1, inplace=True)

    input_data=input_data.rename(columns={'close': 'TXF'})
    input_data['long']=np.nan
    input_data['short']=np.nan
    print("build agent!")
    agent=Agent(actions=3)
    print("build complete!")
    
    env = SampleApp(input_data)
    env.after(100,lambda: run())
    env.mainloop()
