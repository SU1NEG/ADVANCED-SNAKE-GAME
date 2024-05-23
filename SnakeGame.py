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
