#tkinter
import tkinter as tk
from tkinter import *
from PIL import Image, ImageDraw,ImageTk
#Q_Brain
#from Qagent import Agent
#others
import urllib,json
import pandas as pd
import numpy as np
import warnings,time,sys
from datetime import date,datetime
import random

class SampleApp(tk.Tk):
    def __init__(self,data):
        tk.Tk.__init__(self)
        self.c_h = self.c_w =400
        self.im_h = self.im_w =80
        self.current_step=60
        #self.im = Image.new('L', (self.im_h, self.im_w)) 
        #self.im_draw = ImageDraw.Draw(self.im)
        self.im_buffer=[]
        
        self.input_data=data
        """         tk variables            """
        self.canvas1 = PeeredCanvas(self, width=self.c_w, height=self.c_h, border=1, relief="sunken")
        self.canvas2 = PeeredCanvas(self, width=self.c_w, height=self.c_h, border=1, relief="sunken")
        #self.canvas3 = PeeredCanvas(self, width=self.c_w, height=self.c_h, border=1, relief="sunken")
        #self.canvas1.add_peer(self.canvas2)
        #self.canvas1.add_peer(self.canvas3)
        #self.frame1=tk.Frame(self)
        toolbar = tk.Frame(self)
        clear_button = tk.Button(self, text="start", command=self.reset)
        clear_button.pack(in_=toolbar, side="left")
        clear_button = tk.Button(self, text="buy", command=lambda: self.step(0))
        clear_button.pack(in_=toolbar, side="left")
        clear_button = tk.Button(self, text="sell", command=lambda: self.step(1))
        clear_button.pack(in_=toolbar, side="left")
        clear_button = tk.Button(self, text="next", command=lambda: self.step(2))
        clear_button.pack(in_=toolbar, side="left")
        toolbar.pack(side="top", fill="x")
        
        self.canvas1.pack(side="left", fill="both", expand=True)
        self.canvas2.pack(side="right", fill="both", expand=True)
        self.canvas2.pack(side="right", fill="both", expand=True)
        #self.animate(10)
        #self.agent=Agent()
        self.s_t=[]        

        """         user parameters         """
        self.reward=0
        self.performance=[]
        #user[0]:profit         user[1]:max draw down
        self.user=[0,0]  
        
        #state[0] =0 means not holding , state[0] = 1 means holding;     
        #state[1] = holding type;   state[1]: 1 = buy ,   state[1]: -1 =sell
        #state[2] = holding price   state[3]: holding step
        self.state=[0,0,0,0]
        
        
    def reset(self):
        '''Move all items down at a random rate'''
        i=60
        self.current_step=60
        self.im_buffer=[]        
        self.reward=0
        self.performance=[]
        #user[0]:profit         user[1]:max draw down
        self.user=[0,0]  
        
        #state[0] =0 means not holding , state[0] = 1 means holding;     
        #state[1] = holding type;   state[1]: 1 = buy ,   state[1]: -1 =sell
        #state[2] = holding price   state[3]: holding step
        self.state=[0,0,0,0]
        while (self.current_step<64):
            self.drawCanvas1()
            self.current_step += 1
            self.im_buffer.append(np.array(self.im))
            
        print("buffer len = ",len(self.im_buffer))
        print("done")
        self.canvas2.delete('all')
        self.canvas2.create_text(50,50,text=t,fill='blue')
        self.canvas2.create_text(50,70,text='reward= '+str(self.reward),fill='blue')
        self.canvas2.create_text(50,90,text='profit= '+str(self.user[0]),fill='blue')
        #s_t =  np.stack((np.array(self.im_buffer[0]),np.array(self.im_buffer[1]),np.array(self.im_buffer[2]),np.array(self.im_buffer[3])),axis=2)
        self.s_t =  np.stack((self.im_buffer[0],self.im_buffer[1],self.im_buffer[2],self.im_buffer[3]),axis=2)
        self.s_t = self.s_t.reshape(1,self.s_t.shape[0],self.s_t.shape[1],self.s_t.shape[2]) #1x80*80*4
        #photo=ImageTk.PhotoImage(image=self.im)
        
        #self.im.show()
        #self.canvas1.create_image(self.c_h,self.c_w,image=photo)
        #self.canvas1.update()
        #self.im.show()        
        

    def step(self,action):
        

        #action = 0 : long       action = 1 short
        if action==1:
            self.trade(-1)
        elif action==0:
            self.trade(1)
        else:
            self.trade(0)
        self.current_step += 1        
        #initialize canvas and data
        self.canvas1.delete('all')

        color=['',0]
        x=0
        imr_w = self.im_w/60
        
        #action=0: hold     action=1 :buy       action = -1 :sell    action=2: clear
        if (self.state[1]==1):
            color=['red',35]
        elif(self.state[1]==-1):
            color=['green',70]
        else:
            buypoint=0
        t="holding type: "+str(self.state[1])
        self.canvas2.delete('all')
        self.canvas2.create_text(50,50,text=t,fill='blue')
        self.canvas2.create_text(50,70,text='reward= '+str(self.reward),fill='blue')
        self.canvas2.create_text(50,90,text='profit= '+str(self.user[0]),fill='blue')

        h= self.input_data['TXF'].iloc[self.current_step-59:self.current_step].max()- self.input_data['TXF'].iloc[self.current_step-59:self.current_step].min()
        down = self.input_data['TXF'].iloc[self.current_step-59:self.current_step].min()
        high = self.input_data['TXF'].iloc[self.current_step-59:self.current_step].max()
        self.im = Image.new('L', (self.im_h, self.im_w)) 
        self.im_draw = ImageDraw.Draw(self.im)        
        for k in range(self.current_step-59,self.current_step):
            p1= (high-self.input_data['TXF'][k-1])*(self.c_h/h)
            p2= (high-self.input_data['TXF'][k])*(self.c_h/h)
            r_w = self.c_w/60
            
            im_p1= (high-self.input_data['TXF'][k-1])*(self.im_h/h)
            im_p2= (high-self.input_data['TXF'][k])*(self.im_h/h)
            #draw stock line
            self.canvas1.create_line((x-1)*r_w, p1 ,x*r_w , p2, fill="black")
            self.im_draw.line(((x-1)*imr_w, im_p1 ,(x)*imr_w , im_p2), fill=255)
            self.canvas1.update()
            
            """         action          """
            #draw holding price
                
            if(self.state[2]>high)and(self.state[2] != 0):
                c_point=int(self.c_h*0.01)
                im_point=(self.im_h*0.01)

            elif(self.state[2]<down)and(self.state[2] != 0):
                c_point=(self.c_h*0.99)
                im_point=(self.im_h*0.99)
            else:               
                c_point=(high-self.state[2])*(self.c_h/h)
                im_point=(high-self.state[2])*(self.im_h/h)
            len_x=self.current_step-self.state[3]
            if (self.current_step-self.state[3]>0):                
                self.canvas1.create_line((x-1)*r_w, c_point ,x*r_w , c_point, fill=color[0])
                self.im_draw.line(((x-1)*imr_w, im_point ,(x)*imr_w , im_point), fill=color[1])
            
                
            """                          """
           
            #self.input_data=self.input_data.set_value(k,'long',self.input_data['TXF'][k])              
            x+=1

        self.canvas1.update()
        arr=np.array(self.im)
        x_t1=(arr.reshape(1, arr.shape[0], arr.shape[1], 1))    #1x80x80x1
        
        s_t1 = np.append(x_t1, self.s_t[:, :, :, :3], axis=3)
        
        self.s_t =  np.stack((self.im_buffer[0],self.im_buffer[1],self.im_buffer[2],self.im_buffer[3]),axis=2)
        self.s_t = self.s_t.reshape(1,self.s_t.shape[0],self.s_t.shape[1],self.s_t.shape[2]) #1x80*80*4
             
        #self.s_t1 = np.append(self.im_buffer[step], s_t[:, :, :, :3], axis=3)
        

    def trade(self,action):
        #if not holding
        if (self.state[0]==0):            
            if (action==1):
                self.state[1]=1
                self.state[0]=1
                self.state[2] = self.input_data['TXF'][self.current_step]
                self.state[3]=self.current_step
                print("buy")
            elif(action==-1):
                self.state[1]=-1
                self.state[0]=1
                self.state[2] = self.input_data['TXF'][self.current_step]
                self.state[3]=self.current_step
                print("sell")
            elif(action==0):
                print("do nothing")
                pass
            else:
                #print("action>2")
                pass
        
        #if holding
        elif (self.state[0]==1):
                
            if(action== self.state[1]*(-1)):                
                if(self.state[1]==-1):      #long
                    self.reward = self.state[2] - self.input_data['TXF'][self.current_step]-5                    
                    self.state[0] = 0
                    self.state[1] =0
                    self.state[2]=0
                    self.state[3]=0
                    self.user[0]+=self.reward
                    self.performance.append(self.user[0])
                else:                       #short
                    self.reward = self.input_data['TXF'][self.current_step]- self.state[2]-5                    
                    self.state[0] = 0
                    self.state[1] =0
                    self.state[2]=0
                    self.state[3]=0
                    self.user[0]+=self.reward
                    self.performance.append(self.user[0])           
                
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
    
    def drawCanvas1(self):
        self.canvas1.delete('all')
        h= self.input_data['TXF'].iloc[self.current_step-59:self.current_step].max()- self.input_data['TXF'].iloc[self.current_step-59:self.current_step].min()
        down = self.input_data['TXF'].iloc[self.current_step-59:self.current_step].min()
        high = self.input_data['TXF'].iloc[self.current_step-59:self.current_step].max()
        self.im = Image.new('L', (self.im_h, self.im_w)) 
        self.im_draw = ImageDraw.Draw(self.im)
        x=1
        for k in range(self.current_step-59,self.current_step):
            p1= (high-self.input_data['TXF'][k-1])*(self.c_h/h)
            p2= (high-self.input_data['TXF'][k])*(self.c_h/h)
            r_w = self.c_w/60

            self.canvas1.create_line((x-1)*r_w, p1 ,x*r_w , p2, fill="black")
            self.canvas1.update()
            
            im_p1= (high-self.input_data['TXF'][k-1])*(self.im_h/h)
            im_p2= (high-self.input_data['TXF'][k])*(self.im_h/h)
            
            imr_w = self.im_w/60
            self.im_draw.line(((x-1)*imr_w, im_p1 ,(x)*imr_w , im_p2), fill=255)
            x+=1

            
        time.sleep(0.25)
    
class PeeredCanvas(tk.Canvas):
    '''A class that duplicates all objects on one or more peer canvases'''
    def __init__(self, *args, **kwargs):
        self.peers = []
        tk.Canvas.__init__(self, *args, **kwargs)

    def add_peer(self, peer):
        if self.peers is None:
            self.peers = []
        self.peers.append(peer)

    def move(self, *args, **kwargs):
        tk.Canvas.move(self, *args, **kwargs)
        for peer in self.peers:
            peer.move(*args, **kwargs)

    def itemconfigure(self, *args, **kwargs):
        tk.Canvas.itemconfigure(self, *args, **kwargs)
        for peer in self.peers:
            peer.itemconfigure(*args, **kwargs)

    def delete(self, *args, **kwargs):
        tk.Canvas.delete(self, *args)
        for peer in self.peers:
            peer.delete(*args)

    def create_oval(self, *args, **kwargs):
        tk.Canvas.create_oval(self, *args, **kwargs)
        for peer in self.peers:
            peer.create_oval(*args, **kwargs)

if __name__    ==  "__main__":

    #change your own path
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

    app = SampleApp(input_data)
    app.mainloop()
