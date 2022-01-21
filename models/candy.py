import random

import numpy as np

from constants import *


class Candy:

    state = None
    game = None

    def __init__(self, game) -> None:
        self.game = game

    def reset(self):

        if self.state != None:
            self.game.state[self.state[0]][self.state[1]] = 0

        candy_row = random.randint(1, ROWS_AMOUNT - 2)
        candy_col = random.randint(1, COLS_AMOUNT - 2)

        valid_pos = True

        for segment in self.game.snake.state:
            if candy_col == segment[0] and candy_row == segment[1]:
                valid_pos = False

        if self.state is not None and self.state[0] == candy_col and self.state[1] == candy_row:
            valid_pos = False

        if valid_pos:
            self.state = (candy_col, candy_row)
        else:
            self.reset()
