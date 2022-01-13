import pygame
import numpy as np
import sys

from models.candy import *
from models.snake import Snake

class Game:

    screen = None
    running = False
    game_state = []
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
        pygame.font.init()
        self.font = pygame.font.SysFont('Comic Sans MS', 24)
        self.game_state = [[0] * COLS_AMOUNT for i in range(ROWS_AMOUNT)]
        self.snake = Snake(self)
        self.candy = Candy(self)
        self.turns = 0
        self.score = 0
        self.snake.reset()
        self.candy.reset()
        self.screen = pygame.display.set_mode(self.size)

    def start(self):

        self.running = True

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                self.snake.handle_input(event)

            # reset view
            self.screen.fill(self.black)
            self.snake.move()
            self.turns += 1
            
            self.draw_blocks()
            pygame.display.flip()
            self.clock.tick(FPS)
            self.generate_data()

    def stop(self):
        self.running = False

    def reset_game(self):
        self.snake.reset()

    def draw_blocks(self):

        for r_index, row in enumerate(self.game_state):
            for c_index, col in enumerate(row):
                color = (0, 0, 0)
                rect = pygame.Rect(
                    c_index * BLOCK_SIZE, r_index * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE
                )
                pygame.draw.rect(self.screen, color, rect)

        for segment in self.snake.state:
            color = (255, 0, 0)
            rect = pygame.Rect(
                segment[1] * BLOCK_SIZE, segment[0] *
                BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE
            )
            pygame.draw.rect(self.screen, color, rect)

        if self.candy and self.candy.state is not None:
            candy_color = (0, 255, 0)
            rect = pygame.Rect(self.candy.state[1] * BLOCK_SIZE, self.candy.state[0]
                            * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(self.screen, candy_color, rect)

        score_text = "Turn: %s. Snake length: %s. Score: %s" % (
            self.turns, len(self.snake.state), self.score)
        text_surface = self.font.render(score_text, False, (255, 255, 255))
        self.screen.blit(text_surface, (8, 8))


    def generate_data(self):
        # Create data sample and label here and send it to train model
        # Information about game_state (empty = 0, snake = 1, snake_head = 2)
        # Information about world size? (or is this implicit from game_state?)
        # Information about direction choice, which is the label
        # Score should be the loss function

        game_data = np.array(self.game_state)
        for i, segment in enumerate(self.snake.state):
            if i == 0:
                game_data[segment[1]][segment[0]] = 2
            else:
                game_data[segment[1]][segment[0]] = 1

        game_data[self.candy.state[1]][self.candy.state[0]] = 4