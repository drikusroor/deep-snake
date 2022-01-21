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
        state[0] = np.array([GameEntity.FORBIDDEN.value] * COLS_AMOUNT)
        state[ROWS_AMOUNT -
              1] = np.array([GameEntity.FORBIDDEN.value] * COLS_AMOUNT)

        for i in range(ROWS_AMOUNT):
            state[i][0] = GameEntity.FORBIDDEN.value
            state[i][COLS_AMOUNT - 1] = GameEntity.FORBIDDEN.value

        return state

    def reset_state(self):
        self.state = self.generate_empty_state()

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
            self.state[next_move[0]][next_move[1]
                                     ] == GameEntity.FORBIDDEN.value
            or next_move[0] < 0
            or next_move[0] > ROWS_AMOUNT - 1
            or next_move[1] < 0
            or next_move[1] > COLS_AMOUNT - 1
        ):
            move_possible = False

        if move_possible:
            self.snake.state.insert(0, next_move)

            # if self.snake.prev_direction_state != self.snake.direction_state:
            #     reward += .5

            reward += 1

            if self.snake.state[0] == self.candy.state:
                self.candy.reset()
                # reward += 1
            else:
                self.snake.state.pop()

        else:
            reward -= 1
            done = True

        self.state = self.generate_state()
        state = self.get_observation()
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

                if col == GameEntity.FORBIDDEN.value:
                    color = (127, 0, 0)  # border / tail red
                elif col == GameEntity.SNAKE_HEAD.value:
                    color = (0, 0, 127)  # head / green
                elif col == GameEntity.CANDY.value:
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

    def get_observation(self):
        snake_vision_forbidden = self.get_snake_vision(
            2, GameEntity.FORBIDDEN.value)
        snake_direction = self.get_snake_direction()        

        return np.concatenate([
            snake_vision_forbidden,
            snake_direction
        ])

    def get_snake_vision(self, vision_size=3, game_entity=GameEntity.FORBIDDEN.value):
        snake_head_state = np.array(self.snake.state[0])
        vision = []
        for s_y in range(-vision_size, vision_size + 1):
            for s_x in range(-vision_size, vision_size + 1):
                y = np.clip([snake_head_state[1] + s_y], 0, ROWS_AMOUNT - 1)
                x = np.clip([snake_head_state[0] + s_x], 0, COLS_AMOUNT - 1)

                point = 0

                if self.state[y, x] == game_entity:
                    point = 1

                if s_y != 0 or s_x != 0:
                    vision.append(point)

        vision = np.array(vision)

        return vision

    def get_snake_direction(self):
        return np.array([
            1 if self.snake.direction_state == Direction.UP else 0,
            1 if self.snake.direction_state == Direction.RIGHT else 0,
            1 if self.snake.direction_state == Direction.DOWN else 0,
            1 if self.snake.direction_state == Direction.LEFT else 0,
        ])

    def close(self):
        pygame.quit()
        sys.exit()
