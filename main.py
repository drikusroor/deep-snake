import numpy as np
import sys
import tensorflow as tf
from sklearn import neural_network

# local imports
from constants import *
from game import *
from neural_network import NeuralNetwork
from envs.deep_snake_env import DeepSnakeEnv

args = sys.argv

should_train = SHOULD_TRAIN
should_plot = SHOULD_PLOT

# random seed (reproduciblity)
np.random.seed(RANDOM_SEED)
tf.random.set_seed(RANDOM_SEED)

# set the env
env = DeepSnakeEnv()  # env to import
env.seed(RANDOM_SEED)

env.reset()  # reset to env

model_name = f'trained_models/{TRAIN_MODEL}'

neural_network = NeuralNetwork(env, model_name)  # import model

neural_network.train(episodes=N_EPISODES)  # train model
if should_train:
    neural_network.save_model(model_name)  # save model

if should_plot:
    neural_network.plot() # plot model

env.close()
