import numpy as np
from tensorflow.keras import layers, Sequential
from constants import *
from enums.direction import *

class NeuralNetwork:

    def __init__(self, game) -> None:

        self.game = game

        self.model = Sequential(
            [
                layers.Dense(
                    ROWS_AMOUNT * COLS_AMOUNT, activation="relu",
                    kernel_initializer='random_uniform',
                    bias_initializer='zeros'),
                layers.Dense(
                    ROWS_AMOUNT,
                    activation="relu"
                ),
                layers.Dense(4, activation='sigmoid'),
            ]
        )

        self.model.compile(loss='mean_squared_error', optimizer='adam')

    def append_data(self):
        game_state = self.game.game_state
        snake = self.snake
        candy = self.candy
        prev_direction_state = self.game.snake.prev_direction_state

        if prev_direction_state == None:
            return

        X = self.convert_game_state_to_input(game_state, snake, candy)

        y = np.array([[
            prev_direction_state == Direction.UP,
            prev_direction_state == Direction.RIGHT,
            prev_direction_state == Direction.DOWN,
            prev_direction_state == Direction.LEFT,
        ]])

        self.model.fit(X, y, epochs=10, batch_size=len(X), verbose=0)

    def convert_game_state_to_input(self, game_state, snake, candy):
        game_map = game_state.copy()
        for s, segment in enumerate(snake.state):
            if s == 0:
                game_map[segment[1]][segment[0]] = 2
            else:
                game_map[segment[1]][segment[0]] = 1

        candy_y = candy[1]
        candy_x = candy[0]

        game_map[candy_y][candy_x] = 3

        sample = np.array(game_map)
        X = np.array([sample.flatten()])

        return X
