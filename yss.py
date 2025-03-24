import socket
from ast import literal_eval
import heapq
import time
import random

HOST = '0.0.0.0'
PORT = 5001
WIDTH = 800
HEIGHT = 600
SEG_SIZE = 20

import random

# Snake class to simulate the snake's behavior
class Snake:
    def __init__(self, x, y):
        self.x = x  # Current x-position of the snake
        self.y = y  # Current y-position of the snake
        self.body = [(x, y)]  # Snake's body segments
        self.direction = 'RIGHT'  # Initial direction

    def move(self):
        if self.direction == 'RIGHT':
            self.x += 20
        elif self.direction == 'LEFT':
            self.x -= 20
        elif self.direction == 'UP':
            self.y -= 20
        elif self.direction == 'DOWN':
            self.y += 20

        # Add new head and remove tail (simulating movement)
        self.body.insert(0, (self.x, self.y))
        self.body.pop()

    def grow(self):
        # Grow snake by adding another body part
        if self.direction == 'RIGHT':
            self.x += 20
        elif self.direction == 'LEFT':
            self.x -= 20
        elif self.direction == 'UP':
            self.y -= 20
        elif self.direction == 'DOWN':
            self.y += 20

        # Add the new head to body without removing the tail
        self.body.insert(0, (self.x, self.y))

    def get_head(self):
        return self.body[0]

    def get_tail(self):
        return self.body[-1]

# Apple class to generate apple on the grid
class Apple:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.x = random.randint(0, self.width // 20) * 20
        self.y = random.randint(0, self.height // 20) * 20

    def get_position(self):
        return (self.x, self.y)

# Game class to simulate the overall logic of the game
class Game:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.yellow_snake = Snake(640, 340)  # Starting position of yellow snake
        self.red_snake = Snake(800, 80)  # Starting position of red snake
        self.apple = Apple(self.width, self.height)  # Place first apple
        self.apple_position = self.apple.get_position()

    def move_snakes(self):
        # Move yellow snake towards apple
        self.yellow_snake.move()
        self.avoid_red_snake(self.yellow_snake)

        # Move red snake randomly
        self.red_snake.move()
        self.random_red_snake_move()

    def avoid_red_snake(self, yellow_snake):
        yellow_head = yellow_snake.get_head()
        red_head = self.red_snake.get_head()

        # If the red snake is coming towards yellow snake, reverse direction
        if yellow_head[0] == red_head[0] and yellow_head[1] == red_head[1]:
            self.reverse_direction(yellow_snake)

        # If yellow snake is near the red snake, reverse direction
        elif abs(yellow_head[0] - red_head[0]) <= 20 and abs(yellow_head[1] - red_head[1]) <= 20:
            self.reverse_direction(yellow_snake)

    def reverse_direction(self, snake):
        # Reverse the direction of the snake
        if snake.direction == 'RIGHT':
            snake.direction = 'LEFT'
        elif snake.direction == 'LEFT':
            snake.direction = 'RIGHT'
        elif snake.direction == 'UP':
            snake.direction = 'DOWN'
        elif snake.direction == 'DOWN':
            snake.direction = 'UP'

    def random_red_snake_move(self):
        directions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        self.red_snake.direction = random.choice(directions)

    def eat_apple(self):
        # Check if yellow snake eats the apple
        if self.yellow_snake.get_head() == self.apple_position:
            self.yellow_snake.grow()  # Grow snake
            self.apple = Apple(self.width, self.height)  # Generate a new apple
            self.apple_position = self.apple.get_position()

    def print_game_state(self):
        print(f"Yellow Snake Position: {self.yellow_snake.get_head()}")
        print(f"Red Snake Position: {self.red_snake.get_head()}")
        print(f"Apple Position: {self.apple_position}")

# Game loop to simulate the snake game
def game_loop():
    game = Game(1000, 600)  # Game area size
    move_count = 0
    while True:
        move_count += 1
        game.move_snakes()
        game.eat_apple()
        game.print_game_state()

        # Simulate game time step
        if move_count % 100 == 0:
            print("Updating game state...")

        # Break condition (can be added as needed, such as snake collision or game over condition)
        if move_count > 500:  # Limit game to 500 moves for testing
            print("Game Over!")
            break

if __name__ == "__main__":
    game_loop()
