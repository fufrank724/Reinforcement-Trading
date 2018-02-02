# Q-Learning Trading

This is an experiment of trading by Q-Learning algorithm. <br /> 
The Agent model reference from [Morvan's github](https://github.com/MorvanZhou/Reinforcement-learning-with-tensorflow/tree/master/contents/2_Q_Learning_maze).

## Introduction:
To build a reinforcement learning models,we often need 2 classes.
1. Enviroment
2. Agent

The enviroment will return states and rewards to the agent, and the agent will make decisions according to the states and rewards. <br /> 
To finish this program, we will need class "Account" to save the performance of the model,so you can find the following classes in this program.
1. stock(env2.py)
2. Account(account.py)
3. QLearningTable(RL-brain.py)

Stock is the enviroment, and the QLearningTable is the agent reference from [Morvans's Q-Learning example](https://github.com/MorvanZhou/Reinforcement-learning-with-tensorflow/tree/master/contents/2_Q_Learning_maze). <br /> 

To distinguish this project from [DQN project](https://github.com/fufrank724/Reinforcement-Trading/tree/master/DQN), the Agent in this project use table to save states and Q-values instead of neural network.

## Start:
1. change the path in every files.
2. create your jupyter notebook and run "QL_test.ipynb" or just run "run.py"

## Reference
1. [使用增強式學習法建立臺灣股價指數期貨當沖交易策略(Using Reinforcement Learning algorithm to build a future day trade strategy)](https://www.csie.ntu.edu.tw/~lyuu/theses/thesis_r96922117.pdf)
2. [Morvans's Q-Learning example](https://github.com/MorvanZhou/Reinforcement-learning-with-tensorflow/tree/master/contents/2_Q_Learning_maze)


## Dependencies
1. Python 3.5
2. numpy
3. pandas
4. matplotlib
