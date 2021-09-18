import pygame
from random import randint
from enum import Enum
from collections import namedtuple

from pygame import KEYDOWN


class Direction(Enum):
    # These are Constants
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4


pygame.font.init()
Font = pygame.font.Font("Consolas.ttf", 25)

Point = namedtuple('Point', ('x', 'y'))

SNAKE_SIZE = 20
SPEED = 10
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
RED = (255, 0, 0)


class SnakeGame:
    def __init__(self):
        pygame.init()  #Initializing the Pygame
        self.width = 1000
        self.height = 480
        self.display = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Snake")
        self.clock = pygame.time.Clock()
        self.direction = Direction.RIGHT
        self.snake_head = Point(self.width//2, self.height//2)
        self.snake = [self.snake_head, Point(self.snake_head.x-SNAKE_SIZE, self.snake_head.y), Point(self.snake_head.x-(2*SNAKE_SIZE), self.snake_head.y)]

        self.score = 0
        self.food = None
        self._place_food()

    def _place_food(self):
        x = randint(0, (self.width-SNAKE_SIZE) // SNAKE_SIZE) * SNAKE_SIZE
        y = randint(0, (self.height-SNAKE_SIZE) // SNAKE_SIZE) * SNAKE_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()

    def get_key(self, keypress):
        if self.direction == Direction.LEFT and keypress == pygame.K_RIGHT:
            pass
        elif self.direction == Direction.RIGHT and keypress == pygame.K_LEFT:
            pass
        elif self.direction == Direction.UP and keypress == pygame.K_DOWN:
            pass
        elif self.direction == Direction.DOWN and keypress == pygame.K_UP:
            pass
        else:
            if keypress == pygame.K_LEFT:
                self.direction = Direction.LEFT
            elif keypress == pygame.K_RIGHT:
                self.direction = Direction.RIGHT
            elif keypress == pygame.K_UP:
                self.direction = Direction.UP
            elif keypress == pygame.K_DOWN:
                self.direction = Direction.DOWN

    def _move_snake(self, direction):
        x = self.snake_head.x
        y = self.snake_head.y
        if direction == Direction.RIGHT:
            x += SNAKE_SIZE
        elif direction == Direction.LEFT:
            x -= SNAKE_SIZE
        elif direction == Direction.UP:
            y -= SNAKE_SIZE
        elif direction == Direction.DOWN:
            y += SNAKE_SIZE
        self.snake_head = Point(x, y)

    def play_step(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                self.get_key(event.key)
        self._move_snake(self.direction)
        self.snake.insert(0, self.snake_head)

        game_over = False
        if self._is_collided():
            game_over = True
            return game_over, self.score
        if self.snake_head == self.food:
            self.score += 1
            self._place_food()
        else:
            self.snake.pop()
        self._update_screen()
        self.clock.tick(SPEED)

        return game_over, self.score

    def _is_collided(self):
        #     Checking if the snake touches the boundary
        if self.snake_head.x > self.width - SNAKE_SIZE or self.snake_head.x < 0 or self.snake_head.y > self.height - SNAKE_SIZE or self.snake_head.y < 0:
            return True
        #     Checking if the snake touches its body
        if self.snake_head in self.snake[1:]:
            return True

        return False

    def _update_screen(self):
        self.display.fill(BLACK)

        for points in self.snake:
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(points.x, points.y, SNAKE_SIZE, SNAKE_SIZE))
            pygame.draw.rect(self.display, BLUE2, pygame.Rect(points.x+4, points.y+4, 12, 12))
            pass
        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y,SNAKE_SIZE, SNAKE_SIZE))

        text = Font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()


if __name__ == "__main__":
    game = SnakeGame()

    running = True
    while running:
        game_over, score = game.play_step()
        if game_over:
            running = False
    print(f'Final score : {score}')

    pygame.font.quit()
    pygame.quit()
