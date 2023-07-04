import pygame 

pygame.init()

screen = pygame.display.set_mode((800, 700))
pygame.display.set_caption("paint")
clock = pygame.time.Clock()

# цвета, которые испульзую
blue = (0, 204, 204)
red = (50, 0, 0)
pink = (204, 0, 102)
black = (20, 20, 20)

# квадратики для выбора цвета
redRect = pygame.Rect(0, 0, 30, 30)
blueRect = pygame.Rect(30, 0, 30, 30)
pinkRect = pygame.Rect(60, 0, 30, 30)
blackRect = pygame.Rect(90, 0, 30, 30)

# лист квадратичков и их цветов
rects = [[red, redRect], [blue, blueRect], [black, blackRect], [pink, pinkRect]]

# изначальный цвет карандаша
colour = pink

# определить координаты курсора для того, чтобы изменить цвет при выборе квадратиков
def colour_pick():
    posX, posY = pygame.mouse.get_pos()
    # нажатие кнопки мышки
    clik = pygame.mouse.get_pressed()
    global colour
    # нажатие левой кнопки
    if clik[0]:
        if posX < 30 and posY < 30:
            colour = red
        elif posX < 60 and posX > 30 and posY < 30:
            colour = blue
        elif posX < 90 and posX > 60 and posY < 30:
            colour = pink
        elif posX < 120 and posX > 90 and posY < 30:
            colour = black

# функция для рисования
def draw(mode):
    posX, posY = pygame.mouse.get_pos()
    clik = pygame.mouse.get_pressed()
    if clik[0]:
        if mode == "line":
            pygame.draw.circle(screen, colour, (posX, posY), 10)
        elif mode == "square":
            pygame.draw.rect(screen, colour, pygame.Rect(posX, posY, 80, 80), 1)
        elif mode == "rectangle":
            pygame.draw.rect(screen, colour, pygame.Rect(posX, posY, 80, 80*1.3), 1)
        elif mode == "circle":
            pygame.draw.circle(screen, colour, (posX, posY), 60, 1)
        elif mode == "eraser":
             pygame.draw.circle(screen, (0,0,0), (posX, posY), 40)
        elif mode == "right_triangle":
            pygame.draw.line(screen, colour, (posX, posY), (posX+80, posY+80), 1)
            pygame.draw.line(screen, colour, (posX, posY), (posX, posY+80), 1)
            pygame.draw.line(screen, colour, (posX, posY+80), (posX+80, posY+80), 1)
        elif mode == "equilateral_triangle":
            pygame.draw.line(screen, colour, (posX, posY), (posX+80, posY), 1)
            pygame.draw.line(screen, colour, (posX, posY), (posX+80*0.5, posY+80*3**0.5/2), 1)
            pygame.draw.line(screen, colour,(posX+80*0.5, posY+80*3**0.5/2), (posX+80, posY), 1)
        elif mode == "rhombus":
            pygame.draw.line(screen, colour, (posX, posY),(posX+80*0.5, posY-80*3**0.5/2), 1)
            pygame.draw.line(screen, colour, (posX+80*0.5, posY-80*3**0.5/2), (posX+80, posY), 1)
            pygame.draw.line(screen, colour,(posX, posY), (posX+80*0.5, posY+80*3**0.5/2), 1)
            pygame.draw.line(screen, colour, (posX+80*0.5, posY+80*3**0.5/2), (posX+80, posY), 1)
        elif mode == "star":
            pygame.draw.line(screen, colour, (posX, posY), (posX+80, posY), 1)
            pygame.draw.line(screen, colour, (posX, posY), (posX+80*0.5, posY+80*3**0.5/2), 1)
            pygame.draw.line(screen, colour, (posX+80*0.5, posY+80*3**0.5/2), (posX+80, posY), 1)
            pygame.draw.line(screen, colour, (posX, posY+45), (posX+80, posY+45), 1)
            pygame.draw.line(screen, colour, (posX, posY+45), (posX+80*0.5, posY-80*3**0.5/2+45), 1)
            pygame.draw.line(screen, colour, (posX+80*0.5, posY-80*3**0.5/2+45), (posX+80, posY+45), 1)


# очистить экран при нажатии пробела
def clear_all():
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE]:
            screen.fill((0, 0, 0))

# линия по дефолту
figure = "line"

RUN = True
while RUN:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            RUN = False
        if event.type == pygame.KEYDOWN:
            # выбор фигур
            if event.key == pygame.K_2:
                figure = 'circle'
            elif event.key == pygame.K_0:
                figure = 'eraser'
            elif event.key == pygame.K_1:
                figure = 'line'
            elif event.key == pygame.K_3:
                figure = 'square'
            elif event.key == pygame.K_4:
                figure = 'rectangle'
            elif event.key == pygame.K_5:
                figure = 'right_triangle'
            elif event.key == pygame.K_6:
                figure = "equilateral_triangle"
            elif event.key == pygame.K_7:
                figure = 'rhombus'
            elif event.key == pygame.K_8:
                figure = 'star'

    # вывод квадратиков на экран для выбора цвета
    for colors in rects:
        pygame.draw.rect(screen, colors[0], colors[1])

    # запускаем функции
    draw(figure)
    colour_pick()
    clear_all()

    clock.tick(600)
    pygame.display.update()