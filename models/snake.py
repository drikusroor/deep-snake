import numpy as np
from enums.action import Action

from enums.direction import *
from constants import *
from enums.game_entity import GameEntity

class Snake():

    state = []
    game = None
    direction_state = Direction.LEFT
    prev_direction_state = None
    initial_snake_length = 5

    def __init__(self, game) -> None:
        self.state = []
        self.game = game

    def reset(self):
        self.clear_state()
        self.prev_direction_state = self.direction_state
        spawn_point = self.compose_random_spawn_point()
        self.state = spawn_point

        for i, v in enumerate(spawn_point):
            segment = spawn_point[i]
            if i == 0:
                self.game.state[segment[0]][segment[1]
                                            ] = GameEntity.SNAKE_HEAD.value
            else:
                self.game.state[segment[0]][segment[1]
                                            ] = GameEntity.FORBIDDEN.value

    def compose_random_spawn_point(self) -> list:

        initial_direction = np.random.choice(
            [Direction.UP, Direction.RIGHT, Direction.DOWN, Direction.LEFT])

        random_x = np.random.choice(range(0, ROWS_AMOUNT))
        random_y = np.random.choice(range(0, COLS_AMOUNT))

        spawn_point = [(random_x, random_y)]

        if initial_direction == Direction.UP:
            for i in range(1, self.initial_snake_length):
                spawn_point.append((random_x - i, random_y))
        elif initial_direction == Direction.RIGHT:
            for i in range(1, self.initial_snake_length):
                spawn_point.append((random_x, random_y + i))
        elif initial_direction == Direction.DOWN:
            for i in range(1, self.initial_snake_length):
                spawn_point.append((random_x + i, random_y))
        else:
            for i in range(1, self.initial_snake_length):
                spawn_point.append((random_x, random_y - i))

        if self.check_spawn_point_validity(spawn_point):
            return spawn_point
        else:
            return self.compose_random_spawn_point()

    def check_spawn_point_validity(self, spawn_point) -> bool:
        for segment in spawn_point:
            if segment[0] < 0 or segment[0] > ROWS_AMOUNT - 1:
                return False
            elif segment[1] < 0 or segment[1] > COLS_AMOUNT - 1:
                return False
            game_state_segment = self.game.state[segment[0]][segment[1]]
            if game_state_segment != GameEntity.EMPTY.value:
                return False
        return True

    def get_normalized_coordinates(self) -> np.ndarray:
        normalized_coordinates = []
        for segment in self.state:
            normalized_coordinates.append(
                [segment[0] / (ROWS_AMOUNT - 1), segment[1] / (COLS_AMOUNT - 1)])
        return np.array(normalized_coordinates)

    def turn(self, action: Action) -> Direction:
        if action == Action.LEFT:
            if self.direction_state == Direction.UP:
                return Direction.LEFT
            elif self.direction_state == Direction.LEFT:
                return Direction.DOWN
            elif self.direction_state == Direction.DOWN:
                return Direction.RIGHT
            else:
                return Direction.UP
        else:
            if self.direction_state == Direction.UP:
                return Direction.RIGHT
            elif self.direction_state == Direction.LEFT:
                return Direction.UP
            elif self.direction_state == Direction.DOWN:
                return Direction.LEFT
            else:
                return Direction.DOWN

    def clear_state(self):
        self.state = []
