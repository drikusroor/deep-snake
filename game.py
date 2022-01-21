import pygame
import numpy as np
import sys
from enums.action import Action
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

        state = np.array([[0] * ROWS_AMOUNT for i in range(COLS_AMOUNT)])

        state[0] = np.array([GameEntity.FORBIDDEN.value] * ROWS_AMOUNT)
        state[ROWS_AMOUNT -
              1] = np.array([GameEntity.FORBIDDEN.value] * COLS_AMOUNT)

        for i in range(ROWS_AMOUNT):
            state[i][0] = GameEntity.FORBIDDEN.value
            state[i][ROWS_AMOUNT - 1] = GameEntity.FORBIDDEN.value

        return state

    def reset_state(self):
        self.state = self.generate_empty_state()

    def step(self, action: Action):
        move_possible = True
        reward = 0
        done = False
        head = self.snake.state[0]
        predicted_direction = action

        self.snake.prev_direction_state = self.snake.direction_state

        if predicted_direction == 0:
            self.snake.direction_state = self.snake.turn(action)
        elif predicted_direction == 1:
            self.snake.direction_state = self.snake.turn(action)

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
            or next_move[0] > COLS_AMOUNT - 1
            or next_move[1] < 0
            or next_move[1] > ROWS_AMOUNT - 1
        ):
            move_possible = False

        if move_possible:
            self.snake.state.insert(0, next_move)

            reward += 1

            if self.snake.state[0] == self.candy.state:
                self.candy.reset()
                reward += 100
            else:
                self.snake.state.pop()

        else:
            reward -= 10
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
                    r_index * BLOCK_SIZE, c_index * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE
                )
                pygame.draw.rect(self.screen, color, rect)

        pygame.display.flip()

        if RENDER_MODE == 'human':
            self.clock.tick(FPS)

    def generate_state(self):
        state = self.generate_empty_state()

        for s, segment in enumerate(self.snake.state):
            if s == 0:
                state[segment[0]][segment[1]] = GameEntity.SNAKE_HEAD.value
            else:
                state[segment[0]][segment[1]] = GameEntity.FORBIDDEN.value

        candy_y = self.candy.state[0]
        candy_x = self.candy.state[1]

        state[candy_y][candy_x] = GameEntity.CANDY.value

        return state

    def get_observation(self):
        snake_vision_forbidden = self.get_proximities_to_type(
            GameEntity.FORBIDDEN.value)
        snake_vision_candy = self.get_proximities_to_type(
            GameEntity.CANDY.value)
        snake_direction = self.get_snake_direction_hot_encoded()

        return np.concatenate([
            snake_vision_forbidden,
            snake_vision_candy,
            snake_direction
        ])

    def get_proximities_to_type(self, game_entity=GameEntity.FORBIDDEN.value):
        snake_direction = self.snake.direction_state

        left = self.get_proximity_to_type(
            game_entity, snake_direction.get_left())
        forward = self.get_proximity_to_type(game_entity, snake_direction)
        right = self.get_proximity_to_type(
            game_entity, snake_direction.get_right())

        proximities = np.array([left, forward, right])

        return proximities

    def get_proximity_to_type(self, game_entity: GameEntity, snake_direction: Direction):
        snake_head_state = np.array(self.snake.state[0])
        vector = snake_direction.get_vector()
        stepper = vector
        distance = 1
        steps = COLS_AMOUNT

        while steps > 0:
            adjacent_tile = snake_head_state + stepper
            adjacent_tile[0] = np.clip(adjacent_tile[0], 0, COLS_AMOUNT - 1)
            adjacent_tile[1] = np.clip(adjacent_tile[1], 0, ROWS_AMOUNT - 1)

            adjacent_tile_value = self.state[adjacent_tile[0],
                                             adjacent_tile[1]]

            if adjacent_tile_value == game_entity:
                break
            else:
                distance += 1
                stepper += vector
                steps -= 1

        return 1 / distance

    def get_snake_direction_hot_encoded(self):
        return np.array([
            1 if self.snake.direction_state == Direction.UP else 0,
            1 if self.snake.direction_state == Direction.RIGHT else 0,
            1 if self.snake.direction_state == Direction.DOWN else 0,
            1 if self.snake.direction_state == Direction.LEFT else 0,
        ])

    def close(self):
        pygame.quit()
        sys.exit()
