import pygame

from enums.direction import *
from constants import *
from game import *

class Snake():

    state = []
    game = None
    direction_state = Direction.LEFT
    prev_direction_state = None

    def __init__(self, game) -> None:
        self.state = []
        self.game = game

    def move(self):
        move_possible = True
        head = self.state[0]

        # predict here?
        # prediction = model.predict(
        #     convert_game_state_to_input(game_state, snake, candy))[0]
        # print(prediction)

        # if predict:
        #     predicted_direction = np.argmax(prediction)
        #     if predicted_direction == 0:
        #         direction_state = Direction.UP
        #     elif predicted_direction == 1:
        #         direction_state = Direction.RIGHT
        #     elif predicted_direction == 2:
        #         direction_state = Direction.DOWN
        #     else:
        #         direction_state = Direction.LEFT

        #     print(predicted_direction, direction_state)

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
                self.state.pop()

        else:
            self.game.reset_game()
            self.game.score -= 5

    def reset(self):
        self.clear_state()
        self.prev_direction_state = self.direction_state
        self.direction_state = Direction.LEFT
        
        for r_index, row in enumerate(self.game.game_state):
            if r_index == len(self.game.game_state) / 2:
                head_index = int((COLS_AMOUNT / 2) - 1)
                self.state.append((r_index, head_index))
                self.state.append((r_index, head_index + 1))
                self.state.append((r_index, head_index + 2))
                self.state.append((r_index, head_index + 3))
                self.state.append((r_index, head_index + 4))

    def clear_state(self):
        self.state = []

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            scancode = event.scancode
            if scancode == 82:
                self.direction_state = Direction.UP
            elif scancode == 79:
                self.direction_state = Direction.RIGHT
            elif scancode == 81:
                self.direction_state = Direction.DOWN
            elif scancode == 80:
                self.direction_state = Direction.LEFT