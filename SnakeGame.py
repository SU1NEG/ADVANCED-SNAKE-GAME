
import pygame  # Pygame kütüphanesini import eder
import random  # Rastgele sayı üretmek için random kütüphanesini import eder
from enum import Enum  # Enum sınıfını import eder
from collections import deque  # Deque veri yapısını import eder

# Ekran boyutları
SCREEN_WIDTH = 800  # Ekran genişliği
SCREEN_HEIGHT = 600  # Ekran yüksekliği
# Yılan boyutları
SNAKE_SIZE = 20  # Yılanın bir parçasının boyutu
# Yem boyutları
FOOD_SIZE = 20  # Yemin boyutu
# Yılan hızı
SNAKE_SPEED = 20  # Yılanın hareket hızı

# Renkler
ORANGE = (255, 127, 0)  # Turuncu renk
RED = (255, 0, 0)  # Kırmızı renk
GREEN = (0, 255, 0)  # Yeşil renk

# Yönler
class Direction(Enum):  # Yönleri tanımlayan Enum sınıfı
    UP = 1  # Yukarı yön
    DOWN = 2  # Aşağı yön
    LEFT = 3  # Sol yön
    RIGHT = 4  # Sağ yön

# Yılan sınıfı
class Snake:
    def __init__(self, x, y, color):  # Yılanın başlangıç durumu
        self.body = [(x, y)]  # Yılanın gövdesi, başlangıç noktası
        self.color = color  # Yılanın rengi
        self.direction = Direction.RIGHT  # Başlangıç yönü
        self.grow = False  # Büyüme durumu

    def move(self):  # Yılanın hareket fonksiyonu
        x, y = self.body[0]  # Yılanın başının koordinatları
        if self.direction == Direction.UP:  # Eğer yön yukarıysa
            y -= SNAKE_SPEED  # Y koordinatını azalt
            if y < 0:  # Ekran dışına çıkarsa
                y = SCREEN_HEIGHT - SNAKE_SIZE  # Ekranın altından tekrar giriş yap
        elif self.direction == Direction.DOWN:  # Eğer yön aşağıysa
            y += SNAKE_SPEED  # Y koordinatını artır
            if y >= SCREEN_HEIGHT:  # Ekran dışına çıkarsa
                y = 0  # Ekranın üstünden tekrar giriş yap
        elif self.direction == Direction.LEFT:  # Eğer yön solaysa
            x -= SNAKE_SPEED  # X koordinatını azalt
            if x < 0:  # Ekran dışına çıkarsa
                x = SCREEN_WIDTH - SNAKE_SIZE  # Ekranın sağından tekrar giriş yap
        elif self.direction == Direction.RIGHT:  # Eğer yön sağaysa
            x += SNAKE_SPEED  # X koordinatını artır
            if x >= SCREEN_WIDTH:  # Ekran dışına çıkarsa
                x = 0  # Ekranın solundan tekrar giriş yap

        self.body.insert(0, (x, y))  # Yeni pozisyonu yılanın başına ekle
        if not self.grow:  # Eğer büyümüyorsa
            self.body.pop()  # Kuyruk parçasını çıkar
        else:  # Eğer büyüyorsa
            self.grow = False  # Büyüme durumu kapat

    def grow_snake(self):  # Yılanın büyümesini sağlar
        self.grow = True  # Büyüme durumunu aktif et

    def draw(self, surface):  # Yılanı çizer
        for segment in self.body:  # Yılanın her parçası için
            pygame.draw.rect(surface, self.color, (segment[0], segment[1], SNAKE_SIZE, SNAKE_SIZE))  # Dikdörtgen çizer

    def check_eat_food(self, food_position, tolerance=SNAKE_SIZE):  # Yılanın yemi yediğini kontrol eder
        head_x, head_y = self.body[0]  # Yılanın başının koordinatları
        food_x, food_y = food_position  # Yemin koordinatları
        x_distance = abs(head_x - food_x)  # X eksenindeki mesafe
        y_distance = abs(head_y - food_y)  # Y eksenindeki mesafe
        if x_distance < tolerance and y_distance < tolerance:  # Eğer mesafe toleranstan küçükse
            return True  # Yemi yedi
        return False  # Yemi yemedi

    def check_collision_with_other(self, other_snake):  # Yılanın diğer yılanla çarpışmasını kontrol eder
        head = self.body[0]  # Yılanın başı
        return head in other_snake.body  # Diğer yılanın gövdesinde olup olmadığını kontrol eder

# Yem sınıfı
class Food:
    def __init__(self):  # Yemin başlangıç durumu
        self.x = random.randrange(0, SCREEN_WIDTH - FOOD_SIZE, FOOD_SIZE)  # Rastgele x koordinatı
        self.y = random.randrange(0, SCREEN_HEIGHT - FOOD_SIZE, FOOD_SIZE)  # Rastgele y koordinatı

    def draw(self, surface):  # Yemi çizer
        pygame.draw.rect(surface, RED, (self.x, self.y, FOOD_SIZE, FOOD_SIZE))  # Dikdörtgen çizer

# Oyun sınıfı
class Game:
    def __init__(self):  # Oyunun başlangıç durumu
        self.surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Ekran boyutlarını ayarlar
        pygame.display.set_caption("Snake Game")  # Pencere başlığını ayarlar
        self.clock = pygame.time.Clock()  # Saat objesini oluşturur

        self.player = Snake(200, 200, GREEN)  # Oyuncu yılanını oluşturur
        self.ai = Snake(600, 400, ORANGE)  # AI yılanını oluşturur
        self.food = Food()  # Yemi oluşturur

        self.score_player = 0  # Oyuncu skoru
        self.score_ai = 0  # AI skoru

        self.error_rate = 0.0  # Hata oranı

    def handle_events(self):  # Olayları işler
        for event in pygame.event.get():  # Pygame olaylarını döngüye alır
            if event.type == pygame.QUIT:  # Çıkış olayı
                pygame.quit()  # Pygame'i kapat
                quit()  # Programı sonlandır
            elif event.type == pygame.KEYDOWN:  # Tuş basımı olayı
                if event.key == pygame.K_UP:  # Yukarı ok tuşu
                    self.player.direction = Direction.UP  # Yönü yukarı olarak değiştir
                elif event.key == pygame.K_DOWN:  # Aşağı ok tuşu
                    self.player.direction = Direction.DOWN  # Yönü aşağı olarak değiştir
                elif event.key == pygame.K_LEFT:  # Sol ok tuşu
                    self.player.direction = Direction.LEFT  # Yönü sol olarak değiştir
                elif event.key == pygame.K_RIGHT:  # Sağ ok tuşu
                    self.player.direction = Direction.RIGHT  # Yönü sağ olarak değiştir

    def bfs(self, start, target, snake_body):  # Genişlik öncelikli arama algoritması
        queue = deque()  # Kuyruk oluşturur
        visited = set()  # Ziyaret edilen düğümler kümesi
        queue.append((start, []))  # Başlangıç düğümünü kuyruğa ekler

        while queue:  # Kuyruk boş olmadığı sürece
            current_node, path = queue.popleft()  # Kuyruktan düğümü ve yolu al
            if current_node == target:  # Eğer hedef düğüme ulaştıysa
                return path  # Yolu döndür

            if current_node in visited:  # Eğer düğüm ziyaret edildiyse
                continue  # Devam et

            visited.add(current_node)  # Düğümü ziyaret edilmiş olarak işaretle
            x, y = current_node  # Düğümün koordinatları

            # Yukarı
            next_node = (x, y - SNAKE_SPEED)  # Yukarıdaki düğüm
            if y - SNAKE_SPEED >= 0 and next_node not in visited and next_node not in snake_body:  # Geçerli ve ziyaret edilmemişse
                queue.append((next_node, path + [Direction.UP]))  # Kuyruğa ekle
            # Aşağı
            next_node = (x, y + SNAKE_SPEED)  # Aşağıdaki düğüm
            if y + SNAKE_SPEED < SCREEN_HEIGHT and next_node not in visited and next_node not in snake_body:  # Geçerli ve ziyaret edilmemişse
                queue.append((next_node, path + [Direction.DOWN]))  # Kuyruğa ekle
            # Sol
            next_node = (x - SNAKE_SPEED, y)  #Soldaki düğüm
            if x - SNAKE_SPEED >= 0 and next_node not in visited and next_node not in snake_body:  # Geçerli ve ziyaret edilmemişse
                queue.append((next_node, path + [Direction.LEFT]))  # Kuyruğa ekle
            # Sağ
            next_node = (x + SNAKE_SPEED, y)  # Sağdaki düğüm
            if x + SNAKE_SPEED < SCREEN_WIDTH and next_node not in visited and next_node not in snake_body:  # Geçerli ve ziyaret edilmemişse
                queue.append((next_node, path + [Direction.RIGHT]))  # Kuyruğa ekle

        return []  # Hedefe ulaşılamadıysa boş liste döndür

    def move_ai(self):  # AI'nın hareket etme fonksiyonu
        x, y = self.ai.body[0]  # AI yılanının başının koordinatları
        target = (self.food.x, self.food.y)  # Hedef yem koordinatları

        if random.random() < self.error_rate:  # Eğer rastgele hata oranı küçükse
            self.ai.direction = random.choice([Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT])  # Rastgele bir yön seç
        else:  # Hata yapmadığında
            path = self.bfs((x, y), target, set(self.player.body))  # BFS ile hedefe giden yolu bul
            if path:  # Eğer yol varsa
                self.ai.direction = path[0]  # İlk yönü seç
        
        self.ai.move()  # AI yılanını hareket ettir

    def check_collisions(self):  # Çarpışmaları kontrol eder
        if self.player.check_collision_with_other(self.ai):  # Eğer oyuncu AI ile çarpıştıysa
            print("Player loses!")  # Oyuncu kaybetti mesajı
            pygame.quit()  # Pygame'i kapat
            quit()  # Programı sonlandır
        if self.ai.check_collision_with_other(self.player):  # Eğer AI oyuncu ile çarpıştıysa
            print("AI loses!")  # AI kaybetti mesajı
            pygame.quit()  # Pygame'i kapat
            quit()  # Programı sonlandır

    def check_food_collision(self):  # Yem ile çarpışmaları kontrol eder
        if self.player.check_eat_food((self.food.x, self.food.y)):  # Eğer oyuncu yemi yediyse
            self.score_player += 1  # Oyuncu skorunu artır
            self.player.grow_snake()  # Oyuncu yılanını büyüt
            self.food = Food()  # Yeni yem oluştur
        if self.ai.check_eat_food((self.food.x, self.food.y)):  # Eğer AI yemi yediyse
            self.score_ai += 1  # AI skorunu artır
            self.ai.grow_snake()  # AI yılanını büyüt
            self.food = Food()  # Yeni yem oluştur

    def draw_score(self):  # Skorları ekrana çizer
        font = pygame.font.SysFont(None, 30)  # Font objesi oluşturur
        score_player_text = font.render("Player Score: " + str(self.score_player), True, GREEN)  # Oyuncu skorunu yazdırır
        score_ai_text = font.render("AI Score: " + str(self.score_ai), True, ORANGE)  # AI skorunu yazdırır
        self.surface.blit(score_player_text, (10, 10))  # Oyuncu skorunu ekrana yerleştirir
        self.surface.blit(score_ai_text, (10, 40))  # AI skorunu ekrana yerleştirir

    def run(self):  # Oyunu çalıştırır
        while True:  # Sürekli döngü
            self.surface.fill((0, 0, 0))  # Ekranı siyah renkle doldur

            self.handle_events()  # Olayları işle

            self.player.move()  # Oyuncu yılanını hareket ettir
            self.move_ai()  # AI yılanını hareket ettir

            self.check_collisions()  # Çarpışmaları kontrol et
            self.check_food_collision()  # Yem ile çarpışmaları kontrol et

            self.player.draw(self.surface)  # Oyuncu yılanını çiz
            self.ai.draw(self.surface)  # AI yılanını çiz
            self.food.draw(self.surface)  # Yemi çiz
            self.draw_score()  # Skorları çiz

            pygame.display.update()  # Ekranı güncelle
            self.clock.tick(10)  # Oyunun hızını ayarla

# Oyunu başlat
if __name__ == "__main__":  # Eğer bu dosya çalıştırılıyorsa
    pygame.init()  # Pygame'i başlat
    game = Game()  # Oyun objesini oluştur
    game.run()  # Oyunu çalıştır
