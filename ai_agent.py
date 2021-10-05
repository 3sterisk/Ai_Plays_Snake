import random
import numpy as np
from collections import deque

import torch

from game import SnakeGameAI, Direction, Point

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LEARNING_RATE = 0.001


class AGENT:
    def __init__(self):
        self.num_games = 0
        self.randomness = 0
        self.discount_rate = 0
        self.memory = deque(maxlen=MAX_MEMORY) # Calls popleft() when full automatically
        self.model = None
        self.trainer = None
        # TODO: model, trainer

    def get_current_state(self, game):
        head = game.snake[0]
        point_l = Point(head.x - 20, head.y)
        point_r = Point(head.x + 20, head.y)
        point_u = Point(head.x, head.y - 20)
        point_d = Point(head.x, head.y + 20)

        dir_l = game.direction == Direction.LEFT
        dir_r = game.direction == Direction.RIGHT
        dir_u = game.direction == Direction.UP
        dir_d = game.direction == Direction.DOWN

        state = [
            # Danger ahead
            (dir_r and game.is_collided(point_r)) or
            (dir_l and game.is_collided(point_l)) or
            (dir_u and game.is_collided(point_u)) or
            (dir_d and game.is_collided(point_d)),

            # Danger on right
            (dir_u and game.is_collided(point_r)) or
            (dir_d and game.is_collided(point_l)) or
            (dir_l and game.is_collided(point_u)) or
            (dir_r and game.is_collided(point_d)),

            # Danger on left
            (dir_d and game.is_collided(point_r)) or
            (dir_u and game.is_collided(point_l)) or
            (dir_r and game.is_collided(point_u)) or
            (dir_l and game.is_collided(point_d)),

            # Mover Direction
            dir_l,
            dir_r,
            dir_u,
            dir_d,

            # Food Location
            game.food.x < game.snake_head.x,
            game.food.x > game.snake_head.x,
            game.food.y < game.snake_head.y,
            game.food.y > game.snake_head.y
        ]
        return np.array(state, dtype=int)

    def remember(self, state, action, reward, next_state, current_game_over):
        self.memory.append((state, action, reward, next_state, current_game_over))

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)  # returns list of tuple
        else:
            mini_sample = self.memory
            states, actions, rewards, next_states, current_game_overs = zip(*mini_sample)
            self.trainer.train_step(states, actions, rewards, next_states, current_game_overs)

    def train_short_memory(self, state, action, reward, next_state, current_game_over):
        self.trainer.train_step(state, action, reward, next_state, current_game_over)

    def get_action(self, sate):
        #some random moves : tradeoff exploration and exploitation
        self.randomness = 80 - self.num_games
        final_move = [0, 0, 0]
        if random.randint(0, 200) < self.randomness:
            move = random.randint(0, 2)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype = torch.float)
            prediction = self.model.prediction(state, final_move)
            move = torch.argmax(prediction).item()
            final_move[move] = 1
        return final_move

def train():
    scores = []
    mean_scores = []
    total_score = 0
    best_score = 0
    agent = AGENT()
    game = SnakeGameAI()
    while True:
        # capture the current state

        state_old = agent.get_current_state(game)

        final_move = agent.get_action(state_old)

        reward, done, score = game.play_step(final_move)

        state_new = agent.get_current_state(game)

        #train one step at a time

        agent.train_short_memory(state_old, final_move, reward, state_new, done)

        agent.remember(state_old, final_move, reward, state_new, done)

        if done:
            # train from experience, and show result plot
            game.reset()
            agent.num_games += 1
            agent.train_long_memory()
            if score > best_score:
                best_score = score
                # agent.model.save()
            print("Game: ", agent.num_games, "Score :", score, "BestScore :", best_score)

            # TODO: plot_graph
if __name__ == '__main__':
    train()

