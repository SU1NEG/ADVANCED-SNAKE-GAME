import pygame
import random
from enum import Enum
from collections import deque

# Ekran boyutları
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
# Yılan boyutları
SNAKE_SIZE = 20
# Yem boyutları
FOOD_SIZE = 20
# Yılan hızı
SNAKE_SPEED = 20

# Renkler
ORANGE = (255, 127, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Yönler
class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

# Yılan sınıfı
class Snake:
    def __init__(self, x, y, color):
        self.body = [(x, y)]
        self.color = color
        self.direction = Direction.RIGHT
        self.grow = False
    def move(self):
        x, y = self.body[0]
        if self.direction == Direction.UP:
            y -= SNAKE_SPEED
            if y < 0:
                y = SCREEN_HEIGHT - SNAKE_SIZE
        elif self.direction == Direction.DOWN:
            y += SNAKE_SPEED
            if y >= SCREEN_HEIGHT:
                y = 0
        elif self.direction == Direction.LEFT:
            x -= SNAKE_SPEED
            if x < 0:
                x = SCREEN_WIDTH - SNAKE_SIZE
        elif self.direction == Direction.RIGHT:
            x += SNAKE_SPEED
            if x >= SCREEN_WIDTH:
                x = 0

        self.body.insert(0, (x, y))
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False

    def grow_snake(self):
        self.grow = True



