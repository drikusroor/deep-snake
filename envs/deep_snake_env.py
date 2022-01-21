from gym import Env, spaces
from constants import *
from game import *


class DeepSnakeEnv(Env):

    def __init__(self):
        self.action_space = spaces.Discrete(4)
        self.observation_space = spaces.Box(
            low=-1, high=2, shape=(ROWS_AMOUNT, COLS_AMOUNT), dtype=np.uint8)
        self.game = DeepSnakeGame()

    def step(self, action):
        return self.game.step(action)

    def reset(self):
        return self.game.reset()

    def render(self, mode='human'):
        if mode == 'rgb_array':
            pass
        elif mode == 'human':
            self.game.render()
        else:
            pass

    def seed(self, seed=None):
        return RANDOM_SEED

    def close(self):
        return self.game.close()
