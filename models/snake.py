import numpy as np

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

    # not used anymore, see deep_snake_env
    def move(self, action):
        move_possible = True
        head = self.state[0]

        # predict here?
        if predict:
            input = self.game.neural_network.convert_game_state_to_input(
                self.game.game_state, self, self.game.candy)
            prediction = self.game.neural_network.model.predict(input)

            predicted_direction = np.argmax(prediction[0])
            if predicted_direction == 0:
                self.direction_state = Direction.UP
            elif predicted_direction == 1:
                self.direction_state = Direction.RIGHT
            elif predicted_direction == 2:
                self.direction_state = Direction.DOWN
            else:
                self.direction_state = Direction.LEFT

            print(prediction, predicted_direction, self.direction_state)

        if self.direction_state == Direction.UP:
            next_move = (head[0] - 1, head[1])
        elif self.direction_state == Direction.RIGHT:
            next_move = (head[0], head[1] + 1)
        elif self.direction_state == Direction.DOWN:
            next_move = (head[0] + 1, head[1])
        else:
            next_move = (head[0], head[1] - 1)

        for segment in self.state:
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
            self.state.insert(0, next_move)

            if self.state[0] == self.game.candy.state:
                self.game.candy.reset()
                self.game.score += 10
            else:
                self.game.score += 1
                self.state.pop()

        else:
            self.game.reset_game()
            self.game.score -= 5

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

    def clear_state(self):
        self.state = []
