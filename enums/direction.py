from enum import Enum

import numpy as np


class Direction(Enum):
    UP = 1,
    RIGHT = 2,
    DOWN = 3,
    LEFT = 4

    def get_left(self):
        if self == Direction.UP:
            return Direction.LEFT
        elif self == Direction.RIGHT:
            return Direction.UP
        elif self == Direction.DOWN:
            return Direction.RIGHT
        else:
            return Direction.DOWN

    def get_right(self):
        if self == Direction.UP:
            return Direction.RIGHT
        elif self == Direction.RIGHT:
            return Direction.DOWN
        elif self == Direction.DOWN:
            return Direction.LEFT
        else:
            return Direction.UP

    def get_vector(self):
        if self == Direction.UP:
            return np.array([-1, 0])
        elif self == Direction.RIGHT:
            return np.array([0, 1])
        elif self == Direction.DOWN:
            return np.array([1, 0])
        else:
            return np.array([0, -1])
