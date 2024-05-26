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

    def draw(self, surface):
        for segment in self.body:
            pygame.draw.rect(surface, self.color, (segment[0], segment[1], SNAKE_SIZE, SNAKE_SIZE))

    def check_eat_food(self, food_position, tolerance=SNAKE_SIZE):
        head_x, head_y = self.body[0]
        food_x, food_y = food_position
        x_distance = abs(head_x - food_x)
        y_distance = abs(head_y - food_y)
        if x_distance < tolerance and y_distance < tolerance:
            return True
        return False

    def check_collision_with_other(self, other_snake):
        head = self.body[0]
        return head in other_snake.body

# Yem sınıfı
class Food:
    def __init__(self):
        self.x = random.randrange(0, SCREEN_WIDTH - FOOD_SIZE, FOOD_SIZE)
        self.y = random.randrange(0, SCREEN_HEIGHT - FOOD_SIZE, FOOD_SIZE)

    def draw(self, surface):
        pygame.draw.rect(surface, RED, (self.x, self.y, FOOD_SIZE, FOOD_SIZE))

# Oyun sınıfı
class Game:
    def __init__(self):
        self.surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()

        self.player = Snake(200, 200, GREEN)
        self.ai = Snake(600, 400, ORANGE)
        self.food = Food()

        self.score_player = 0
        self.score_ai = 0

        self.error_rate = 0.0

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.player.direction = Direction.UP
                elif event.key == pygame.K_DOWN:
                    self.player.direction = Direction.DOWN
                elif event.key == pygame.K_LEFT:
                    self.player.direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT:
                    self.player.direction = Direction.RIGHT

    def bfs(self, start, target, snake_body):
        queue = deque()
        visited = set()
        queue.append((start, []))

        while queue:
            current_node, path = queue.popleft()
            if current_node == target:
                return path

            if current_node in visited:
                continue

            visited.add(current_node)
            x, y = current_node

            # Yukarı
            next_node = (x, y - SNAKE_SPEED)
            if y - SNAKE_SPEED >= 0 and next_node not in visited and next_node not in snake_body:
                queue.append((next_node, path + [Direction.UP]))
            # Aşağı
            next_node = (x, y + SNAKE_SPEED)
            if y + SNAKE_SPEED < SCREEN_HEIGHT and next_node not in visited and next_node not in snake_body:
                queue.append((next_node, path + [Direction.DOWN]))
            # Sol
            next_node = (x - SNAKE_SPEED, y)
            if x - SNAKE_SPEED >= 0 and next_node not in visited and next_node not in snake_body:
                queue.append((next_node, path + [Direction.LEFT]))
            # Sağ
            next_node = (x + SNAKE_SPEED, y)
            if x + SNAKE_SPEED < SCREEN_WIDTH and next_node not in visited and next_node not in snake_body:
                queue.append((next_node, path + [Direction.RIGHT]))

        return []

    def move_ai(self):
        x, y = self.ai.body[0]
        target = (self.food.x, self.food.y)

        if random.random() < self.error_rate:
            self.ai.direction = random.choice([Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT])
        else:
            path = self.bfs((x, y), target, set(self.player.body))
            if path:
                self.ai.direction = path[0]
        
        self.ai.move()

    def check_collisions(self):
        if self.player.check_collision_with_other(self.ai):
            print("Player loses!")
            pygame.quit()
            quit()
        if self.ai.check_collision_with_other(self.player):
            print("AI loses!")
            pygame.quit()
            quit()

    def check_food_collision(self):
        if self.player.check_eat_food((self.food.x, self.food.y)):
            self.score_player += 1
            self.player.grow_snake()
            self.food = Food()
        if self.ai.check_eat_food((self.food.x, self.food.y)):
            self.score_ai += 1
            self.ai.grow_snake()
            self.food = Food()

    def draw_score(self):
        font = pygame.font.SysFont(None, 30)
        score_player_text = font.render("Player Score: " + str(self.score_player), True, GREEN)
        score_ai_text = font.render("AI Score: " + str(self.score_ai), True, ORANGE)
        self.surface.blit(score_player_text, (10, 10))
        self.surface.blit(score_ai_text, (10, 40))

    def run(self):
        while True:
            self.surface.fill((0, 0, 0))

            self.handle_events()

            self.player.move()
            self.move_ai()

            self.check_collisions()
            self.check_food_collision()

            self.player.draw(self.surface)
            self.ai.draw(self.surface)
            self.food.draw(self.surface)
            self.draw_score()

            pygame.display.update()
            self.clock.tick(10)

# Oyunu başlat
if __name__ == "__main__":
    pygame.init()
    game = Game()
    game.run()























    


