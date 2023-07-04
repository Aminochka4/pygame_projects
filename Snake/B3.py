import pygame
import random, time
from connection import conn
from pygame.math import Vector2

cur = conn.cursor()

# создание таблиц для данных игры
# cur.execute("CREATE TABLE snake_users (userid SERIAL PRIMARY KEY, username TEXT)")
# cur.execute("CREATE TABLE snake_scores (userid SERIAL PRIMARY KEY, score INTEGER, level INTEGER)")
# conn.commit()

def login(cur, username):
    cur.execute(F"SELECT userid FROM snake_users WHERE username = '{username}'")
    result = cur.fetchone()
    if result:
        cur.execute(f"""SELECT snake_scores.score, snake_scores.level
                        FROM snake_users
                        INNER JOIN snake_scores ON snake_users.userid = snake_scores.userid
                        WHERE username = '{username}'""")
        data = cur.fetchone()
        score, level = data[0], data[1]
        userid = result[0]
        return score, level, userid

    else:
        cur.execute(f"INSERT INTO snake_users (username) VALUES ('{username}')")
        cur.execute(f"INSERT INTO snake_scores (score, level) VALUES (0, 0)")
        cur.execute(f"SELECT userid FROM snake_users WHERE username = '{username}'")
        global conn
        temp = cur.fetchone()
        userid = temp[0]
        score, level = 0, 0
        return score, level, userid
    
# задаем позиции для стен, которые будут на разных уровнях
def position_of_walls(filename):
    walls = []
    with open(filename, 'r') as file:
        # эта функция перечисляет элементы в итерируемом объекте и возвращает тапл с индексом и самим элементом
        for i, line in enumerate(file):
            col = 0
            for char in line:
                if char == '1':
                    walls.append((col, i))
                    col += 1
                else:
                    col += 1
    return walls

# нарисовать шахматное поле для змейки и стены припятствии
def draw_map():
    global count_column, count_row, walls
    surface.fill(border_color)
    for column in range(count_column):
        for row in range(count_row):
            if (column+row) % 2 == 0:
                colour = block_color1
            else: colour = block_color2
            draw_block(colour, column, row)
    for block in walls:
        draw_block(head_color, block[0], block[1])


#  рисут блок на определенной позиции column row
def draw_block(colour, column, row):
            pygame.draw.rect(surface, colour, [20+block_size*column, 20+row*block_size, block_size, block_size])


pygame.init()

# параметры цветов и шрифтов, также нужные файлы для игры
block_size = 35
menu_color = (255, 153, 255)
surface_size = (block_size*20+250, block_size*20+40)
count_column, count_row = 20, 20
zhylan_color = (204, 0, 204)
head_color = (102, 0, 102)
border_color = (255, 153, 255)
font_color = (0, 0, 0)
block_color1 = (255, 204, 255)
block_color2 = (255, 255, 255)
font_size = 30
ms = 150
cur_time = time.time()
fonts = pygame.font.SysFont('Arial Black', font_size)  # шрифт для меню
fonts1 = pygame.font.SysFont('Cooper Black', 50)
image_heart1 = pygame.image.load(r"lab 10\Snake3\heart.png")
image_heart = pygame.transform.scale(image_heart1, (35, 35))
masic = pygame.mixer.music.load(r"lab 10\Snake3\music.mp3")
pygame.mixer.music.play(-1)
levels = [r"lab 10\Snake3\lvl1.txt", r"lab 10\Snake3\lvl2.txt", r"lab 10\Snake3\lvl3.txt"]

surface = pygame.display.set_mode(surface_size)
surface.fill(border_color)
clock = pygame.time.Clock()
done = False
start_of_game = True
pause = False


class ZHYLAN():
    def __init__(self):
        # позиция во время начала игры
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        # нейтральное движение для змейки, где она стоит на одном месте
        self.direction = Vector2(0,0)
        self.new_block = False

    def draw_zhylan(self):
        # голова змейки
        draw_block(head_color, self.body[0].x, self.body[0].y)
        # тело змейки (отличаются по цветам)
        for block in self.body[1:]:
            draw_block(zhylan_color, block.x, block.y)         

    def move_zhylan(self):
        # если змейка скушала еду
        if self.new_block == True:
            body_copy = self.body[:]
            body_copy.insert(0,body_copy[0]+self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            # для предотвращения ошибок когда змея двигается внутри головы
            if self.direction != Vector2(0, 0):
                # копируем тело змеи без хвоста
                body_copy = self.body[:-1]
                # добавляем блок в напралении змейки в начале тела
                body_copy.insert(0,body_copy[0]+self.direction)
                self.body = body_copy[:]
    
    def reset(self):
        # перезапуск игры и позиция, где игра снова начинается
        self.direction = Vector2(0,0)
        self.body = [Vector2(5,10),Vector2(4,10),Vector2(3,10)]


class HEART():
    def __init__(self):
        self.random_spawn(10, 5)

    def random_spawn(self, x, y):
        # обновляет позицию еды
        self.pos = Vector2(x, y)
        # задает время спауна
        self.time = time.time()
   
    def draw(self):
        # изображение еды для змейки
        surface.blit(image_heart, (int(self.pos.x * block_size+20) , int(self.pos.y * block_size+20)))


class MAIN():
    def __init__(self):
        self.zhylan = ZHYLAN()
        self.heart = HEART()
        self.score = 0
        self.level = 0
        # обновление каждые 150 миллисекунд 
        self.speed = [150, 140, 130]
    
    def update(self):
        self.zhylan.move_zhylan()
        self.colission()
        cur_time = time.time()
        # рандомное перемещение еды в новом месте спустя 6 секунд
        if cur_time - self.heart.time > 6:
            x, y = self.random_location()
            self.heart.random_spawn(x, y)
        self.death()

    def draw_game(self):
        self.zhylan.draw_zhylan()
        self.heart.draw()
        self.menu()
    
    # столкновение змейки с едой
    def colission(self):
        if self.heart.pos == self.zhylan.body[0]:
            x, y = self.random_location()
            self.heart.random_spawn(x, y)
            self.zhylan.new_block = True
            self.score += 1
            if self.score % 7 == 0:
                # меняем уровень
                self.level += 1
                global walls
                walls = position_of_walls(levels[self.level%3])
                # для начальной в позиции в новой "локации"
                self.game_over()
                # для того что бы появление не было на месте стен
                self.random_location()
                # меняем скорость
                self.update_speed()

    def random_location(self):
        global walls
        # задает рандомные координаты для еды
        x = random.randint(0, count_column - 1)
        y = random.randint(0, count_row - 1)
        # для того чтобы еда не появлялась в змее или в стенах
        while (Vector2(x,y) in self.zhylan.body or ((x, y) in walls)):
            x = random.randint(0, count_column - 1)
            y = random.randint(0, count_row - 1)
        return x,y    

    def death(self):
        global walls
        # змейка умирает, когда бьется об границы поля
        if not 0 <= self.zhylan.body[0].x < count_column or not 0<= self.zhylan.body[0].y < count_row:
            self.game_over()
        # чтобы змейка умирала, когда бьется об саму себя
        for block in self.zhylan.body[1:]:
            if block == self.zhylan.body[0]:
                self.game_over()
        # чтобы хззмейка умирала, когда бьется об стены
        for block in walls:
            if block == self.zhylan.body[0]:
                self.game_over()

    # перезапуск игры, когда змейка умирает
    def game_over(self):
        self.score = 0
        self.zhylan.reset()

    def update_speed(self):
        # ускоряем змейку с каждым уровнем 
        pygame.time.set_timer(pygame.USEREVENT, self.speed[self.level%3])

    def menu(self):
        # рисуем меню на экране с текстом
        pygame.draw.rect(surface, menu_color, [block_size*count_column + 40, 0, 1000, 1000])
        score_text = fonts.render("score: " + str(self.score), True, font_color, menu_color)
        level_text = fonts.render("level: "+ str(self.level), True, font_color, menu_color)
        surface.blit(score_text, (block_size*20 + 50, 20))
        surface.blit(level_text, (block_size*20 + 50, 20 + font_size*2))

username = ''
# квадратик на экране в котором мы вводим юзернейм
input_box = pygame.Rect(340, 270, 200, 50) 

while start_of_game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            start_of_game = False
            done = True
        if event.type == pygame.KEYDOWN:
            # удаление букв при ошибочном введении
            if event.key == pygame.K_BACKSPACE:
                username = username[:-1]
            elif event.key == pygame.K_RETURN and username != "":
                # начало игры когда юзернейм введен
                start_of_game = False
            else:
                username += event.unicode
    surface.fill(border_color)
    # рисую квадратик где вводят юзернейм
    pygame.draw.rect(surface, font_color, input_box, 2)
    username_surface = fonts.render(username, True, font_color)
    name_of_game = fonts1.render("snake heartbreaker", True, font_color)
    surface.blit(username_surface, (input_box.x + 10, input_box.y + 10))
    surface.blit(name_of_game, (220, 200))
    # для того чтобы расширять квадратик при введении длинного юзернейма
    input_box.w = max(200, username_surface.get_width() + 10)
    pygame.display.update()

game = MAIN()
# задаем скорость данного уровня
pygame.time.set_timer(pygame.USEREVENT, game.speed[game.level%3])
walls = position_of_walls(levels[game.level%3])
# получить данные из таблицы
game.score, game.level, userid = login(cur, username)

cur = conn.cursor()


while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            cur.execute(f"UPDATE snake_scores SET score = {game.score}, level = {game.level} WHERE userid = {userid}")
            conn.commit()
            done = True
        if event.type == pygame.USEREVENT and not pause:
            game.update()
        # меняем направление движения с клавишами
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                game.zhylan.direction = Vector2(0, -1)
            if event.key == pygame.K_DOWN:
                game.zhylan.direction = Vector2(0, 1)
            if event.key == pygame.K_RIGHT:
                game.zhylan.direction = Vector2(1, 0)
            if event.key == pygame.K_LEFT:
                game.zhylan.direction = Vector2(-1, 0)
            if event.key == pygame.K_SPACE:
                pause = not pause

    draw_map()

    if pause:
        # позиция кнопки с текстом
        pos = block_size*8 + 20
        pause_text = fonts.render("quit and save", True, font_color, head_color)
        surface.blit(pause_text, (pos, pos + 45))
        posX, posY = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        # условие при нажатии кнопки
        if click[0] and pos < posX < pos + 4 * block_size + 20 and pos + block_size < posY < pos + 2 * block_size:
            # обновляет данные в таблице
            cur.execute(f"UPDATE snake_scores SET score = {game.score}, level = {game.level} WHERE userid = {userid}")
            conn.commit()
            done = True

    game.draw_game()

    pygame.display.flip()

    clock.tick(60)