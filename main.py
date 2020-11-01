import sys, pygame
from enum import Enum


class Direction(Enum):
    UP = (1,)
    RIGHT = (2,)
    DOWN = (3,)
    LEFT = 4


pygame.init()
clock = pygame.time.Clock()
FPS = 4

size = width, height = 320, 240
speed = [2, 2]
black = 0, 0, 0

screen = pygame.display.set_mode(size)

BLOCK_SIZE = 10
ROWS_AMOUNT = int(height / BLOCK_SIZE)
COLS_AMOUNT = int(width / BLOCK_SIZE)

game_state = [[0] * COLS_AMOUNT for i in range(ROWS_AMOUNT)]
direction_state = Direction.LEFT
snake = []


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


reset_snake()


def move_snake():
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

    if move_possible:
        snake.insert(0, next_move)
        snake.pop()
    else:
        reset_snake()


def draw_blocks():
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
