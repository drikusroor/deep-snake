import pygame
import tensorflow as tf
import numpy as np
from tensorflow.keras import datasets, layers, losses, models, optimizers, Sequential
import matplotlib.pyplot as plt
import random
import pygad

# local imports
from game import *
from models.snake import *
from models.candy import *
from neural_network import *
from constants import *

# Game
game = Game()
neural_network = NeuralNetwork(game)

session_samples = np.array([])

game.start()
