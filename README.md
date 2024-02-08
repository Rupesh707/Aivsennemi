## @Author : Rupesh Kumar
Date : 07/02/2023
Licensed Under the [MIT License](LICENSE.md)

# Deep Reinforcement Learning
## Project: Train AI Vs Ennemi

## Introduction
The goal of this project is to develop an AI able to learn how to capture its emmemi. In order to do it, I implemented a Deep Reinforcement Learning algorithm. This approach consists in giving the system parameters related to its state, and a positive or negative reward based on its actions. No rules about the game are given, and initially the AI agent has no information on what it needs to do. The goal for the system is to figure it out and elaborate a strategy to maximize the score - or the reward.

We are going to see how a Deep Q-Learning algorithm learns how to capture ennemi.

## Install
This project requires Python 3.8.5 with the pygame library installed, as well as Pytorch. 

The full list of requirements is in `requirements.txt`. 

## Run
To run and show the game, executes in the snake-ga folder:

```python
python agent.py
```
Arguments description:

- --display - Type bool, default True, display or not game view
- --speed - Type integer, default 50, game speed


To train the agent, set in the file agent.py:
- `params['train'] = True`
The parameters of the Deep neural network can be changed in *snakeClass.py* by modifying the dictionary `params` in the function `define_parameters()`


### **ARCHITECTURE OF APPLICATION**

<p align="center">
  <img src="Images/Archi.png">
</p>
