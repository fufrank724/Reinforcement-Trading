#tkinter
import tkinter as tk
from tkinter import *
from PIL import Image, ImageDraw

#others
import urllib,json
import pandas as pd
import numpy as np
import warnings,time,sys
from datetime import date,datetime


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

c_h = c_w =400
im_h = im_w = 400

im = Image.new('L', (im_h, im_w)) 
im_draw = ImageDraw.Draw(im)

#root = tk.Tk()
#canvas = tk.Canvas(root,width=c_w,height=c_h)
#canvas.pack()
class env():
    def __init__(self,data):
        self.intput_data=data        
        self.c_h = self.c_w =400
        self.im_h = self.im_w = 400
        self.im_buffer=[]
        self.root = tk.Tk()
        self.canvas = tk.Canvas(self.root,width=self.c_w,height=self.c_h)
        self.canvas.pack()

    def drawCanvas(self,input_data,len=61):
        i=60
        x=1
        buypoint=0        
        while (i<len):
            self.canvas.delete('all')
            h= input_data['TXF'].iloc[i-59:i].max()- input_data['TXF'].iloc[i-59:i].min()
            down = input_data['TXF'].iloc[i-59:i].min()
            high = input_data['TXF'].iloc[i-59:i].max()
            
            for k in range(i-59,i):
                p1= (high-input_data['TXF'][k-1])*(self.c_h/h)
                p2= (high-input_data['TXF'][k])*(self.c_h/h)
                self.r_w = self.c_w/60
                self.canvas.create_line((x-1)*self.r_w, p1 ,x*self.r_w , p2, fill="black")
                if (k>=30):
                    if(k==30):
                        buypoint=(high-input_data['TXF'][k])*(self.c_h/h)
                        input_data=input_data.set_value(k,'long',input_data['TXF'][k])
                    self.canvas.create_line((x-1)*self.r_w, buypoint ,x*self.r_w , buypoint, fill="red")
                    im_draw.line(((x-1)*imr_w, buypoint ,(x)*imr_w , buypoint), fill=125)
                            
                im_p1= (high-input_data['TXF'][k-1])*(self.im_h/h)
                im_p2= (high-input_data['TXF'][k])*(self.im_h/h)
                
                imr_w = self.im_w/60
                im_draw.line(((x-1)*imr_w, im_p1 ,(x)*imr_w , im_p2), fill=255)
                x+=1
            time.sleep(0.25)
            x=1
            i+=1
            print(i)
            self.im_buffer.append(np.array(im))
            self.canvas.update()
        print("done")

        #root.destroy()
        #im.show()
    def drawImage(self):
        pass
        
    def step(self):
        pass
    

Env=env(input_data)        
Env.root.after(100,Env.drawCanvas(input_data))
Env.root.mainloop()