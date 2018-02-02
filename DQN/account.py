import numpy as np
class Account():
    def __init__(self):
        self.grossloss=0
        self.grossprofit=0
        self.totaltrade=0
        self.maxDrawdown=0
        self.drawdown=0
        self.profit=0
        self.maxprofit=0
        self.profitfactor=0
        self.sharpe=0
        self.performance=[]
        self.history=[]
        
    def getReward(self,reward):
        if reward>0:    self.grossprofit+=reward
        elif reward<0:  self.grossloss+=reward
        
        _profit=self.profit
        self.profit+=reward
        
        if self.profit>_profit:
            self.maxprofit=self.profit
        
        elif self.profit<self.maxprofit:
            self.drawdown = self.maxprofit-self.profit
            if self.drawdown>=self.maxDrawdown:
                self.maxDrawdown=self.drawdown
                
        self.performance.append(self.profit)
        self.history.append(reward)
        
        if len(self.performance)>1:
            perform=np.array(self.history)        
            self.sharpe=np.sqrt(30) * np.mean(perform) / np.std(perform)
        
        if self.maxDrawdown>0:
            self.profitfactor=self.profit/self.maxDrawdown
        else:
            self.profitfactor=self.profit/len(self.performance)/5
        
        
    def reset(self):
        self.grossloss=0
        self.grossprofit=0
        self.totaltrade=0
        self.maxDrawdown=0
        self.drawdown=0
        self.profit=0
        self.maxprofit=0
        self.performance=[]
        self.history=[]