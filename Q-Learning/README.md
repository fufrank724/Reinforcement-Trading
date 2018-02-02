# Q-Learning Trading

This is an experiment of trading by Q-Learning algorithm.
The Agent model reference from [Morvan's github](https://github.com/MorvanZhou/Reinforcement-learning-with-tensorflow/tree/master/contents/2_Q_Learning_maze).

## Algorithms：
To build a reinforcement learning models,we often need 2 classes.
1. Enviroment
2. Agent

The enviroment will return states and rewards to the agent, and the agent will make decisions according to the states and rewards.
To finish this program, we will need class "Account" to save the performance of the model,so you can find the following classes in this program.
1. stock(env2.py)
2. Account(account.py)
3. QLearningTable(RL-brain.py)

Stock is the enviroment, and the QLearningTable is the agent reference from [Morvans's Q-Learning example](https://github.com/MorvanZhou/Reinforcement-learning-with-tensorflow/tree/master/contents/2_Q_Learning_maze).

To distinguish this project from [DQN project](https://github.com/fufrank724/Reinforcement-Trading/tree/master/DQN),the Agent in this project use table to save states and Q-values instead of neural network.

## Reference
1. [使用增強式學習法建立臺灣股價指數期貨當沖交易策略](https://www.csie.ntu.edu.tw/~lyuu/theses/thesis_r96922117.pdf)
2. [Morvans's Q-Learning example](https://github.com/MorvanZhou/Reinforcement-learning-with-tensorflow/tree/master/contents/2_Q_Learning_maze)


## Dependencies
1. Python 3.5
2. numpy
3. pandas
4. matplotlib
