import pygame
from random import randint
from enum import Enum
from collections import namedtuple
import numpy as np

pygame.font.init()
Font = pygame.font.Font("Consolas.ttf", 25)

#function to reset the game

#reward system

#change the play function play(keypress) -> direction calculate direction

#game_iteration (current frame)

#change in _is_collided function for ai to check collision happened or not

class Direction(Enum):
    # These are Constants
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4


Point = namedtuple('Point', ('x', 'y'))

SNAKE_SIZE = 20
SPEED = 10000
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
RED = (255, 0, 0)


class SnakeGameAI:
    def __init__(self):
        pygame.init()  #Initializing the Pygame
        self.width = 640
        self.height = 480
        self.display = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Snake")
        self.clock = pygame.time.Clock()
        self.reset()

    def reset(self):
        self.direction = Direction.RIGHT
        self.snake_head = Point(self.width//2, self.height//2)
        self.snake = [self.snake_head, Point(self.snake_head.x-SNAKE_SIZE, self.snake_head.y), Point(self.snake_head.x-(2*SNAKE_SIZE), self.snake_head.y)]

        self.score = 0
        self.food = None
        self._place_food()
        self.current_iteration = 0

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

    def _move_snake(self, agent_action):
        # [straight, right, left]

        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        current_dir_index = clock_wise.index(self.direction)
        if np.array_equal(agent_action, [1, 0, 0]):
            new_direction = clock_wise[current_dir_index] #no change
        elif np.array_equal(agent_action, [0, 1, 0]):
            new_current_dir_index = (current_dir_index + 1) % 4
            new_direction = clock_wise[new_current_dir_index]
        else:
            new_current_dir_index = (current_dir_index - 1) % 4
            new_direction = clock_wise[new_current_dir_index]

        self.direction = new_direction

        x = self.snake_head.x
        y = self.snake_head.y
        if self.direction == Direction.RIGHT:
            x += SNAKE_SIZE
        elif self.direction == Direction.LEFT:
            x -= SNAKE_SIZE
        elif self.direction == Direction.UP:
            y -= SNAKE_SIZE
        elif self.direction == Direction.DOWN:
            y += SNAKE_SIZE
        self.snake_head = Point(x, y)

    def play_step(self, agent_action):
        self.current_iteration += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        self._move_snake(agent_action)
        self.snake.insert(0, self.snake_head)

        reward = 0

        game_over = False
        if self.is_collided() or self.current_iteration > 100*len(self.snake):
            game_over = True
            reward -= 10
            return reward, game_over, self.score
        if self.snake_head == self.food:
            self.score += 1
            reward += 10
            self._place_food()
        else:
            self.snake.pop()
        self._update_screen()
        self.clock.tick(SPEED)

        return reward, game_over, self.score

    def is_collided(self, points=None):
        if points is None:
            points = self.snake_head
        #     Checking if the snake touches the boundary
        if points.x > self.width - SNAKE_SIZE or points.x < 0 or points.y > self.height - SNAKE_SIZE or points.y < 0:
            return True
        #     Checking if the snake touches its body
        if points in self.snake[1:]:
            return True

        return False

    def _update_screen(self):
        self.display.fill(BLACK)

        for points in self.snake:
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(points.x, points.y, SNAKE_SIZE, SNAKE_SIZE))
            pygame.draw.rect(self.display, BLUE2, pygame.Rect(points.x+4, points.y+4, 12, 12))
        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y,SNAKE_SIZE, SNAKE_SIZE))

        text = Font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()


