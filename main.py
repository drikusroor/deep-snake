import sys, pygame
from enum import Enum
import tensorflow as tf
import numpy as np
from tensorflow.keras import datasets, layers, models, Sequential
import matplotlib.pyplot as plt
import random

BLOCK_SIZE = 20
ROWS_AMOUNT = int(24)
COLS_AMOUNT = int(32)

class Direction(Enum):
    UP = (1,)
    RIGHT = (2,)
    DOWN = (3,)
    LEFT = 4

# Model
model = Sequential(
    [
        layers.Dense(2, activation="relu"),
        layers.Dense(3, activation="relu"),
        layers.Dense(4),
    ]
)

# Game
pygame.init()
pygame.font.init()
font = pygame.font.SysFont('Comic Sans MS', 24)
clock = pygame.time.Clock()
FPS = 4

size = width, height = COLS_AMOUNT * BLOCK_SIZE, ROWS_AMOUNT * BLOCK_SIZE
speed = [2, 2]
black = 0, 0, 0

screen = pygame.display.set_mode(size)

ROWS_AMOUNT = int(height / BLOCK_SIZE)
COLS_AMOUNT = int(width / BLOCK_SIZE)

game_state = [[0] * COLS_AMOUNT for i in range(ROWS_AMOUNT)]
direction_state = Direction.LEFT
snake = []
candy = None
turns = 0

def reset_snake():
    snake.clear()
    for r_index, row in enumerate(game_state):
        if r_index == len(game_state) / 2:
            head_index = int((COLS_AMOUNT / 2) - 1)
            snake.append((r_index, head_index))
            snake.append((r_index, head_index + 1))
            snake.append((r_index, head_index + 2))
            snake.append((r_index, head_index + 3))
            snake.append((r_index, head_index + 4))

def reset_candy():
    global game_state
    global candy

    if candy != None:
        game_state[candy[0]][candy[1]] = 0

    candy_row = random.randint(0, ROWS_AMOUNT - 1)
    candy_col = random.randint(0, COLS_AMOUNT - 1)

    valid_pos = True

    for segment in snake:
        if candy_row == segment[0] and candy_col == segment[1]:
            valid_pos = False

    if candy is not None and candy[0] == candy_row and candy[1] == candy_col:
        valid_pos = False

    if valid_pos:
        candy = (candy_row, candy_col)
    else:
        reset_candy()

reset_snake()
reset_candy()
session_samples = np.array([])

def append_data():
    global game_state
    global snake
    global turns
    game_map = game_state.copy()
    for segment in snake:
        game_map[segment[1]][segment[0]] = 1

    sample = np.array([game_map, len(snake), turns])
    sample_flat = sample.flatten()

    np.append(session_samples, sample_flat)

def move_snake():
    global turns
    global direction_state
    global session_samples
    move_possible = True
    head = snake[0]
    if direction_state == Direction.UP:
        next_move = (head[0] - 1, head[1])
    elif direction_state == Direction.RIGHT:
        next_move = (head[0], head[1] + 1)
    elif direction_state == Direction.DOWN:
        next_move = (head[0] + 1, head[1])
    else:
        next_move = (head[0], head[1] - 1)

    for segment in snake:
        if segment[0] == next_move[0] and segment[1] == next_move[1]:
            move_possible = False
        elif (
            next_move[0] < 0
            or next_move[0] > ROWS_AMOUNT - 1
            or next_move[1] < 0
            or next_move[1] > COLS_AMOUNT - 1
        ):
            move_possible = False

    # Create data sample and label here and send it to train model
    # Information about game_state (empty = 0, snake = 1, snake_head = 2)
    # Information about world size? (or is this implicit from game_state?)
    # Information about direction choice, which is the label
    # move_possible should become the loss function as it tells the NN whether the direction choice was correct
    # But also score and snake length should taken into account
    # append_data(game_state, snake)

    if move_possible:
        snake.insert(0, next_move)
        
        if snake[0] == candy:
            reset_candy()
        else:
            snake.pop()

        turns = turns + 1
    else:
        direction_state = Direction.LEFT
        reset_snake()
        session_samples = 0
        turns = 0


def draw_blocks():
    global candy
    
    for r_index, row in enumerate(game_state):
        for c_index, col in enumerate(row):
            color = (0, 0, 0)
            rect = pygame.Rect(
                c_index * BLOCK_SIZE, r_index * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE
            )
            pygame.draw.rect(screen, color, rect)

    for segment in snake:
        color = (255, 0, 0)
        rect = pygame.Rect(
            segment[1] * BLOCK_SIZE, segment[0] * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE
        )
        pygame.draw.rect(screen, color, rect)

    if candy is not None:
        candy_color = (0, 255, 0)
        rect = pygame.Rect(candy[1] * BLOCK_SIZE, candy[0] * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
        pygame.draw.rect(screen, candy_color, rect)

    score_text = "Turn: %s. Snake length: %s." % (turns, len(snake))
    text_surface = font.render(score_text, False, (255, 255, 255))
    screen.blit(text_surface, (8, 8))

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN:
            scancode = event.scancode
            if scancode == 82:
                direction_state = Direction.UP
            elif scancode == 79:
                direction_state = Direction.RIGHT
            elif scancode == 81:
                direction_state = Direction.DOWN
            elif scancode == 80:
                direction_state = Direction.LEFT

    screen.fill(black)
    move_snake()
    draw_blocks()
    pygame.display.flip()
    clock.tick(FPS)
