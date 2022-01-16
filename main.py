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
# should_train = args[0] == "should_train"

should_train = True
should_display = True

# random seed (reproduciblity)
np.random.seed(RANDOM_SEED)
tf.random.set_seed(RANDOM_SEED)

# set the env
env = DeepSnakeEnv()  # env to import
env.seed(RANDOM_SEED)

env.reset()  # reset to env

model_name = 'trained_models/model.v3.h5'

neural_network = NeuralNetwork(env)  # import model

neural_network.train(episodes=N_EPISODES)  # train model
if should_train:
    neural_network.save_model(model_name)  # save model
    neural_network.plot()

env.close()
