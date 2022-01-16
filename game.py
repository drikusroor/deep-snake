import pygame
import numpy as np
import sys
from enums.direction import Direction

from models.candy import *
from models.snake import Snake


class Game:

    screen = None
    running = False
    state = []
    turns = 0
    score = 0
    snake = None
    candy = None
    black = 0, 0, 0
    size = width, height = COLS_AMOUNT * BLOCK_SIZE, ROWS_AMOUNT * BLOCK_SIZE
    clock = pygame.time.Clock()
    font = None

    def __init__(self) -> None:
        pygame.init()
        self.snake = Snake(self)
        self.candy = Candy(self)
        self.reset_state()

    def generate_empty_state(self):
        state = np.array([[0] * COLS_AMOUNT for i in range(ROWS_AMOUNT)])
        return state

    def reset_state(self):
        if RENDER_MODE == 'human':
            self.screen = pygame.display.set_mode(self.size)
        self.state = self.generate_empty_state()

    def start(self):
        pass

    def step(self, action):
        move_possible = True
        reward = 0
        done = False
        head = self.snake.state[0]
        predicted_direction = action

        if predicted_direction == 0:
            self.snake.direction_state = Direction.UP
        elif predicted_direction == 1:
            self.snake.direction_state = Direction.RIGHT
        elif predicted_direction == 2:
            self.snake.direction_state = Direction.DOWN
        else:
            self.snake.direction_state = Direction.LEFT

        if self.snake.direction_state == Direction.UP:
            next_move = (head[0] - 1, head[1])
        elif self.snake.direction_state == Direction.RIGHT:
            next_move = (head[0], head[1] + 1)
        elif self.snake.direction_state == Direction.DOWN:
            next_move = (head[0] + 1, head[1])
        else:
            next_move = (head[0], head[1] - 1)

        for segment in self.snake.state:
            if segment[0] == next_move[0] and segment[1] == next_move[1]:
                move_possible = False
            elif (
                next_move[0] < 0
                or next_move[0] > ROWS_AMOUNT - 1
                or next_move[1] < 0
                or next_move[1] > COLS_AMOUNT - 1
            ):
                move_possible = False

        if move_possible:
            self.snake.state.insert(0, next_move)

            if self.snake.state[0] == self.candy.state:
                self.candy.reset()
                reward = 10
            else:
                reward = .1
                self.snake.state.pop()
        else:
            done = True
            reward = -1

        self.state = self.generate_state()
        state = self.state  # self.flatten_state()
        info = {"state": state, "reward": reward, "done": done,
                "turns": self.turns, "score": self.score}

        return state, reward, done, info

    def reset(self):
        self.reset_state()
        self.snake.reset()
        self.candy.reset()
        self.state = self.generate_state()
        return self.state

    def render(self):
        for r_index, row in enumerate(self.state):
            for c_index, col in enumerate(row):
                color = (0, 0, 0)

                if col == 1:
                    color = (255, 0, 0)  # red
                elif col == 2:
                    color = (0, 255, 0)  # green
                elif col == 3:
                    color = (0, 0, 255)  # candy

                rect = pygame.Rect(
                    c_index * BLOCK_SIZE, r_index * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE
                )
                pygame.draw.rect(self.screen, color, rect)

        pygame.display.flip()
        
        if RENDER_MODE == 'human':
            self.clock.tick(FPS)

    def generate_state(self):
        state = self.generate_empty_state()

        for s, segment in enumerate(self.snake.state):
            if s == 0:
                state[segment[1]][segment[0]] = 2
            else:
                state[segment[1]][segment[0]] = 1

        candy_y = self.candy.state[1]
        candy_x = self.candy.state[0]

        state[candy_y][candy_x] = 3

        return state

    def flatten_state(self):
        np_state = np.array(self.state)
        return np.array([np_state.flatten()])

    def close(self):
        pygame.quit()
        sys.exit()
