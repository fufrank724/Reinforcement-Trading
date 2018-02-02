from keras import initializers
from keras.initializers import normal, identity
from keras.models import model_from_json
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.layers.convolutional import Convolution2D, MaxPooling2D
from keras.optimizers import SGD , Adam
import tensorflow as tf
import numpy as np
import random
from collections import deque
import json

class Agent():
    def __init__(self,actions=2,initialepsilons=0.1,finalEpsilon=0.0001,batch=32,memory=50000,learningRate=1e-4,ifRun=False):
        self.im_h = self.im_w =80
        self.img_channels = 4
        self.ACTIONS = actions # number of valid actions
        self.GAMMA = 0.99 # decay rate of past observations
        self.OBSERVATION = 3200. # timesteps to observe before training
        self.EXPLORE = 3000000. # frames over which to anneal epsilon
        self.FINAL_EPSILON = finalEpsilon # final value of epsilon
        self.INITIAL_EPSILON = initialepsilons # starting value of epsilon
        self.REPLAY_MEMORY = memory # number of previous transitions to remember
        self.BATCH = batch # size of minibatch
        self.FRAME_PER_ACTION = 1
        self.LEARNING_RATE = learningRate
        
        self.buildmodel()
        if (ifRun):
            self.load()
            self.epsilon=self.INITIAL_EPSILON=FINAL_EPSILON
        else:
            self.epsilon=self.INITIAL_EPSILON
        self.state=np.zeros((1,80,80,4))#1,80,80,4
        self.loss=0
        
        self.D = deque()        
        
    def buildmodel(self):
        for i in range(10):
            print()
        print("Now we build the model")
        self.model = Sequential()
        self.model.add(Convolution2D(32, 8, 8, subsample=(4, 4), border_mode='same',input_shape=(self.im_h , self.im_w,self.img_channels)))  #80*80*4
        self.model.add(Activation('relu'))
        self.model.add(Convolution2D(64, 4, 4, subsample=(2, 2), border_mode='same'))
        self.model.add(Activation('relu'))
        self.model.add(Convolution2D(64, 3, 3, subsample=(1, 1), border_mode='same'))
        self.model.add(Activation('relu'))
        self.model.add(Flatten())
        self.model.add(Dense(512))
        self.model.add(Activation('relu'))
        self.model.add(Dense(self.ACTIONS))
       
        adam = Adam(lr=self.LEARNING_RATE)
        self.model.compile(loss='mse',optimizer=adam)
        print("We finish building the model")
        
    def choose_action(self,s_t,_isobserve=False):    #1*80*80*4

            #choose an action epsilon greedy
        if random.random() <= self.epsilon:
            #print("----------Random Action----------")
            action_index = random.randrange(self.ACTIONS)
            max_Q=action_index
        else:
            q = self.model.predict(s_t)       #input a stack of 4 images, get the prediction
            max_Q = np.argmax(q)    #action index
                
        if self.epsilon > self.FINAL_EPSILON and _isobserve:
            self.epsilon -= (self.INITIAL_EPSILON - self.FINAL_EPSILON) / self.EXPLORE   
        return max_Q
        
    def store_transition(self,s_t,action,reward,s_t1,terminal):
        self.D.append((s_t, action, reward, s_t1,terminal))
        self.state=s_t
        if len(self.D) > self.REPLAY_MEMORY:
            self.D.popleft()
            
    def train(self):

        #sample a minibatch to train on
        minibatch = random.sample(self.D, self.BATCH)

        inputs = np.zeros((self.BATCH, self.state.shape[1], self.state.shape[2], self.state.shape[3]))   #32, 80, 80, 4
        #print (inputs.shape)
        targets = np.zeros((inputs.shape[0], self.ACTIONS))                                              #32, 2

        #Now we do the experience replay
        for i in range(0, len(minibatch)):
            state_t = minibatch[i][0]
            action_t = minibatch[i][1]   #This is action index
            reward_t = minibatch[i][2]
            state_t1 = minibatch[i][3]
            terminal = minibatch[i][4]
            # if terminated, only equals reward

            inputs[i:i + 1] = state_t    #I saved down s_t

            targets[i] = self.model.predict(state_t)  # Hitting each buttom probability
            Q_sa = self.model.predict(state_t1)

            if terminal:
                targets[i, action_t] = reward_t
            else:
                targets[i, action_t] = reward_t + self.GAMMA * np.max(Q_sa)

        # targets2 = normalize(targets)
        self.loss += self.model.train_on_batch(inputs, targets)


    def save(self):
        self.model.save_weights("E:/Python/Python/jupyter/futures/TXF/model.h5", overwrite=True)
        with open("model.json", "w") as outfile:
                json.dump(self.model.to_json(), outfile)
    def load(self):
        try:
            print("\n\nloading...")
            self.model.load_weights("E:/Python/Python/jupyter/futures/TXF/model.h5")
            adam = Adam(lr=self.LEARNING_RATE)
            self.model.compile(loss='mse',optimizer=adam)
            print("load success!")
        except:
            print("load failed")