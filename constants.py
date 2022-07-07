
# Drikus Roor
# drikusroor@gmail.com

"""
constants.py
~~~~~~~~~~
A module which contains all constants for the snake game, it is useful to improve performance
which is very important for the genetic algorithm
"""

RENDER_MODE = 'rgb_array'
FPS = 24
BLOCK_SIZE = 30
ROWS_AMOUNT = int(18)
COLS_AMOUNT = int(18)
observation_shape = 12
predict = True
SHOULD_TRAIN = True
SHOULD_PLOT = True

ENV = "DeepSnake-v1"
TRAIN_MODEL = "model.v11.h5"
RANDOM_SEED = 1
N_EPISODES = 250
MAX_TURNS = 500
