from pygame.locals import *
import random, sys, time, pygame

pygame.init()

screen_width = 600
screen_height = 600
speed = 5
score = 0
font = pygame.font.SysFont("Times New Roman", 60)
font_small = pygame.font.SysFont("Times New Roman", 30)
the_end_of_game = font.render ("Game Over", True, (255, 0, 0))

surface = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

#files
road = pygame.image.load(r"lab 8\Racer\road.jpg")
music = pygame.mixer.music.load(r"lab 8\Racer\music.mp3")
pygame.mixer.music.play(-1)


class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image1 = pygame.image.load(r"lab 8\Racer\coin.png")
        self.image = pygame.transform.scale(self.image1, (80, 80))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, screen_width-40), 0)
        # для рандомного веса монет
        self.weights = [1, 2, 3, 4]

    def move(self):
        self.rect.move_ip(0, 5)
        if (self.rect.bottom > 600):
            self.rect.top = 0
            self.rect.center = (random.randint(40, screen_width-40), 0)


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image1 = pygame.image.load(r"lab 8\Racer\enemy.png")
        self.image = pygame.transform.scale(self.image1, (75, 150))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40,screen_width-40),0) 
 
    def move(self):
        self.rect.move_ip(0,speed)
        if (self.rect.bottom > 600):
            self.rect.top = 0
            self.rect.center = (random.randint(60, 340), 0)
 

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image1 = pygame.image.load(r"lab 8\Racer\player.png")
        self.image = pygame.transform.scale(self.image1, (75, 150))
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)
 
    def move(self):
        pressed_keys = pygame.key.get_pressed()
         
        if self.rect.left > 0:
              if pressed_keys[K_LEFT]:
                  self.rect.move_ip(-10, 0)
        if self.rect.right < screen_width:        
              if pressed_keys[K_RIGHT]:
                  self.rect.move_ip(10, 0)

C1 = Coin()
P1 = Player()
E1 = Enemy()

# создание групп
enemies = pygame.sprite.Group()
enemies.add(E1)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)

# создание персонального события для игры
inc_speed = pygame.USEREVENT + 1
pygame.time.set_timer(inc_speed, 1000)

time_collision = time.time()

collision = False

#main part
while True:
    
    for event in pygame.event.get():
        # if event.type == inc_speed:
        #     speed += 0.2

        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    
    surface.blit(road, (0, 0))
    scores = font_small.render("coins:"+str(score), True, (255, 255, 255))
    surface.blit(scores, (480, 6))


    for entity in all_sprites:
        surface.blit(entity.image, entity.rect)
        entity.move()

    cur_time = time.time()

    if C1.rect.colliderect(P1.rect):
        if cur_time - time_collision > 0.5:
            # обновить время столкновения
            time_collision = time.time()
            # добавление рандомного веса
            addition = C1.weights[random.randint(0, 3)]
            # добовлление коинсов по одной монете
            while(addition):
                score += 1
                addition -= 1
                # каждые 4 очка повышение скорости
                if score % 4 == 0:
                    speed += 0.5
            # изменяем это значение чтобы в if not collision давало нам False, чтобы изображение монеты больше не blit()
            collision = True

    C1.move()

    if not collision:
        surface.blit(C1.image, C1.rect)
        # это время time3 перестанет обновляться как только произошло столкновение,
        # пототму что после столкновения этот if будет давать False
        time3 = time.time()

    # так как время time3 перестанет обновляться после столкновения то реальное время его обгонит
    # и спустя полсекунды опять уберет статус столкновения    
    if cur_time - time3 > (0.5):
        time3 = time.time()
        collision = False

    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.music.pause()
        pygame.mixer.Sound(r"lab 8\Racer\crash.wav").play()
        time.sleep(2)

        surface.fill((0, 0, 0))
        surface.blit(the_end_of_game, (155, 250))
        surface.blit(scores, (250, 330))
        
        pygame.display.update()
        for entity in all_sprites:
            entity.kill()
        time.sleep(5)
        pygame.quit()
        sys.exit()
    
    pygame.display.update()
    clock.tick(60)