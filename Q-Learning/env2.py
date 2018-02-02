import math,datetime
import numpy as np
import pandas as pd
from account import Account

class stock():
    def __init__(self,start="2000-01-01",end="2010-07-01"):
        self.action_space = ['Buy', 'Sell', 'hold']
        self.n_actions = (len(self.action_space))
        self.n_features = 6# quote ,H_L , H_C ,C_L ,avg_c10 ,avg_vol10
        
        self.data=pd.read_csv("E:/Python/Python/jupyter/futures/QL/TXF_60min_filted.CSV")   
        self.data.drop('quote', axis=1, inplace=True)
        self.current_step=4
        
        self.reward=0
        self.state=[0,0,0,0]
        self.user=Account()
        
        self.s=[]
        self._s=[]
    
    def reset(self):

        self.current_step=4
        self.user.reset()
        self.state=[0,0,0,0]
        self.s=self.make_state()
        self._s=[]
        return self.s
        
    def _ifLastDay(self,date):
        year, month, day=int(date.strftime("%Y")),int(date.strftime("%m")),int(date.strftime("%d"))
        end = int(datetime.datetime(year, month, day).strftime("%W"))
        begin = int(datetime.datetime(year, month, 1).strftime("%W"))
        
        if(end-begin+1)>2 and day>14 and  datetime.date(year, month, day).weekday()==2:
            return True
        else:
            return False
    def make_state(self):
        s=[]
        self.current_step+=1
        for i in range(self.current_step-5,self.current_step):
            s.append([self.data['H_L'][self.current_step],
                      self.data['H_C'][self.current_step],
                      self.data['C_L'][self.current_step],
                      str(self.data['avg_c10_filt'][self.current_step]),
                      str(self.data['avg_vol10_filt'][self.current_step])])
        return s
        
    def step(self,action):
        #if not holding
        self._s=self.make_state()
        if action==1:
            action=(-1)
        elif action==0:
            action=(1)
        else:
            action=(0)
        if (self.state[0]==0):
            if (action==1):
                self.state[1]=1
                self.state[0]=1
                self.state[2] = self.data['close'][self.current_step]
                self.state[3]=self.current_step
                #print("buy")
            elif(action==-1):
                self.state[1]=-1
                self.state[0]=1
                self.state[2] = self.data['close'][self.current_step]
                self.state[3]=self.current_step
                #print("sell")
            elif(action==0):
                #print("do nothing")
                pass
            else:
                #print("action>2")
                pass
        
        #if holding
        elif (self.state[0]==1):
                
            if(action== self.state[1]*(-1)):                
                if(self.state[1]==-1):      #long
                    self.reward = self.state[2] - self.data['close'][self.current_step]-5                    
                    self.state[0] = 0
                    self.state[1] =0
                    self.state[2]=0
                    self.state[3]=0
                    self.user.getReward(self.reward)
                else:                       #short
                    self.reward = self.data['close'][self.current_step]- self.state[2]-5                    
                    self.state[0] = 0
                    self.state[1] =0
                    self.state[2]=0
                    self.state[3]=0
                    self.user.getReward(self.reward)
                
            elif(action==0):
                #print("hold!")
                self.reward=0
            elif(action==self.state[1]):
                #print("action same to holding type")
                self.reward=0
                pass
            else:
                #print("WTF?!")
                pass
        return self.s,self.user.profitfactor,self._s