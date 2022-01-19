import pygame
import numpy as np
import sys
from enums.direction import Direction
from enums.game_entity import GameEntity

from models.candy import *
from models.snake import Snake


class DeepSnakeGame:

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
        state[0] = np.array([-1] * COLS_AMOUNT)
        state[ROWS_AMOUNT - 1] = np.array([-1] * COLS_AMOUNT)

        for i in range(ROWS_AMOUNT):
            state[i][0] = -1
            state[i][COLS_AMOUNT - 1] = -1

        return state

    def reset_state(self):
        self.state = self.generate_empty_state()

    def start(self):
        pass

    def step(self, action):
        move_possible = True
        reward = 0
        done = False
        head = self.snake.state[0]
        predicted_direction = action

        self.snake.prev_direction_state = self.snake.direction_state

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

        if (
            self.state[next_move[0]][next_move[1]] == -1
            or next_move[0] < 0
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
                reward = 0
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
        if RENDER_MODE == 'human':
            self.screen = pygame.display.set_mode(self.size)
        return self.state

    def render(self):
        for r_index, row in enumerate(self.state):
            for c_index, col in enumerate(row):
                color = (0, 0, 0)

                if col == -1:
                    color = (127, 0, 0)  # border / tail red
                elif col == 1:
                    color = (0, 0, 127)  # head / green
                elif col == 2:
                    color = (0, 127, 0)  # candy / green

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
                state[segment[1]][segment[0]] = GameEntity.SNAKE_HEAD.value
            else:
                state[segment[1]][segment[0]] = GameEntity.FORBIDDEN.value

        candy_y = self.candy.state[1]
        candy_x = self.candy.state[0]

        state[candy_y][candy_x] = GameEntity.CANDY.value

        return state

    def flatten_state(self):
        np_state = np.array(self.state)
        return np.array([np_state.flatten()])

    def close(self):
        pygame.quit()
        sys.exit()
