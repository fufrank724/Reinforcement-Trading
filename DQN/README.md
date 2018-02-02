# Nature Deep Q-Trading Model

This is an experiment of trading by Nature Depp Q-Learning algorithm. <br /> 
The Agent model is referenced from [Playing Flappy Bird](https://github.com/yanpanlau/Keras-FlappyBird).

## Introduction:
In Q-Learning responsity, I found that it is hard to build a good trading bot by Q-table, after reading [Playing Atari with Deep Reinforcement Learning](https://arxiv.org/pdf/1312.5602.pdf), 
I write a new program to build a deep Q-Trading bot, but it still have bad performance.<br /> 

In this responsity, the input of convolutional neural network is the line chart of close price instead of price array.<br />

## Reference
1. [使用增強式學習法建立臺灣股價指數期貨當沖交易策略](https://www.csie.ntu.edu.tw/~lyuu/theses/thesis_r96922117.pdf)
2. [Playing Atari with Deep Reinforcement Learning](https://arxiv.org/pdf/1312.5602.pdf)
3. [Keras-FlappyBird](https://github.com/yanpanlau/Keras-FlappyBird)

## Dependencies
1. Python 3.5
2. Tensorflow 1.0.0
3. Keras
4. numpy
5. pandas
6. matplot
7. tkinter
8. PIL
9. h5py

