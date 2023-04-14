import pygame
import random

WIDTH = 480
HEIGHT = 600
FPS = 60

# Задаем цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Создаем игру и окно
pygame.init()  # это команда, которая запускает pygame
#pygame.mixer.init() # для звука
screen = pygame.display.set_mode((WIDTH, HEIGHT))#окно программы,создается,когда задаем размер в настройках.
pygame.display.set_caption("My first python game")
clock = pygame.time.Clock()

# добавим шрифт и рисуем счет
#score = 0# переменная для счета 
#переменную со счетом, нужно отрисовывать на экране
font_name = pygame.font.match_font('arial')# ищет наиболее подходящий шрифт в системе.
def draw_text(surf, text, size, x, y):# создаем функцию
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)#Отрисовка текста на экране это, вычисление необходимой 
# структуры пикселей называется «рендерингом».True,отвечает за включение и отключение сглаживания.
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)
def show_go_screen():# screen display at the start of the game
    screen.blit(background, background_rect)
    draw_text(screen, "FIRST PYGAME GAME", 48, WIDTH / 2, HEIGHT / 4 -50)
    draw_text(screen, "Rules of the game.", 24,WIDTH / 2, HEIGHT / 2 - 50)
    draw_text(screen, " Goal: score the maximum number of points by moving the robot ", 14,WIDTH / 2, HEIGHT / 2)
    draw_text(screen, "with the arrows left - right, collecting coins. ", 14,WIDTH / 2, HEIGHT / 2 +20)
    draw_text(screen, "When a robot collides with a triangle, the player receives a penalty of 10 points. ", 14,WIDTH / 2, HEIGHT / 2 +50)
    draw_text(screen, "When a robot collides with a coin, the player receives 5 points. ", 14,WIDTH / 2, HEIGHT / 2 +80)
    draw_text(screen, "When a robot collides with a monster, the game over. ", 14,WIDTH / 2, HEIGHT / 2 +110)
    draw_text(screen, "Press a key to begin or X for exit", 18, WIDTH / 2, HEIGHT * 3 / 4)
    
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False

# Загрузка всей игровой графики
robot = pygame.image.load("robo.png")# загружаем изображение робота
ovi = pygame.image.load("ovi.png")# загружаем изображение ovi
coin = pygame.image.load("kolikko.png")# загружаем изображение монеты 
hirvio = pygame.image.load("hirvio.png")# загружаем изображение hirvio 
background = pygame.image.load("starfield.png")# загружаем изображение background 
background_rect = background.get_rect()#определим rect background.
hit_sound = pygame.mixer.Sound("expl6.wav")# загружаем звук столкновения монеты и робота
#gameOver_sound = pygame.mixer.Sound("gameOver.mp3")# загружаем звук столкновения hirvio и робота gameOver

class Player(pygame.sprite.Sprite): #class сообщает Python, что определяется новый объект, который будет спрайтом игрока. Его тип pygame.sprite.Sprite. Это значит, что он будет основан на заранее определенном в Pygame классе Sprite.
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #запускает инициализатор встроенных классов Sprite
        self.image = robot #определить свойство image.у каждого спрайта в Pygame должно быть два свойства: image и rect.
        self.rect = self.image.get_rect() #определим rect спрайта. Это сокращенное от rectangle (прямоугольник)
        self.rect.centerx = WIDTH / 2 # определяем место спрайта по ширине (центр)
        self.rect.bottom = HEIGHT - 10 #определяем место спрайта по высоте
        self.speedx = 0 # устанавливаем скорость спрайта 
        
    def update(self):# при каждом игровом цикле спрайт Player будет обновлен
        self.speedx = 0#скорость изначально 0
        keystate = pygame.key.get_pressed()#возвращает словарь со всеми клавишами клавиатуры и значениями True или False
        if keystate[pygame.K_LEFT]: #если нажата K_LEFT
            self.speedx = -8 # скорость по х -8
        if keystate[pygame.K_RIGHT]:#если нажата K_RIGHT
            self.speedx = 8 # скорость по х 8
        self.rect.x += self.speedx # картинка у нас self.rect присваиваем ей скорость
        if self.rect.right > WIDTH: # делаем так, чтобы спрайт останавливался у края экрана.
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0  

class Mob(pygame.sprite.Sprite):# свойства спрайты ovi.
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #запускает инициализатор встроенных классов Sprite
        self.image = ovi #определить свойство image.
        #у каждого спрайта в Pygame должно быть два свойства: image и rect.сейчас это кусе 30 на 40
        self.rect = self.image.get_rect()#определим rect спрайта.
        self.rect.x = random.randrange(WIDTH - self.rect.width)#ограничим случайное положение rect по х шириной 
        self.rect.y = random.randrange(-100, -40)# то же высотой появляется сверху
        self.speedy = random.randrange(5, 8)#определим скорость спрайта случайной скоростью от 1 до 8 по у
        #self.speedx = random.randrange(-3, 3)# и от -3 до 3 по х
  
    def update(self):#для функции обновления нужно задать движения спрайта с определенной скоростью,
        #self.rect.x += self.speedx # берем скорости из self.speedx
        self.rect.y += self.speedy# и self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
       # когда спрайт доберется до низа перенесем его в случайное место вверху        
            self.rect.x = random.randrange(WIDTH - self.rect.width)# ограничение по случайному месту по х
            self.rect.y = random.randrange(-100, -40)# ограничение по случайному месту по у
            self.speedy = random.randrange(1, 8) # случайный выбор скорости   

class Coin(pygame.sprite.Sprite):# свойства спрайты kolikko.
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #запускает инициализатор встроенных классов Sprite
        self.image = coin #определить свойство image.
        #у каждого спрайта в Pygame должно быть два свойства: image и rect.сейчас это кусе 30 на 40
        self.rect = self.image.get_rect()#определим rect спрайта.
        self.rect.x = random.randrange(WIDTH - self.rect.width)#ограничим случайное положение rect по х шириной 
        self.rect.y = random.randrange(-100, -40)# то же высотой появляется сверху
        self.speedy = random.randrange(3, 8)#определим скорость спрайта случайной скоростью от 1 до 8 по у
        self.speedx = random.randrange(-3, 3)# и от -3 до 3 по х
  
    def update(self):#для функции обновления нужно задать движения спрайта с определенной скоростью,
        self.rect.x += self.speedx# берем скорости из self.speedx
        self.rect.y += self.speedy# и self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -20 or self.rect.right > WIDTH + 20:
       # когда спрайт доберется до низа перенесем его в случайное место вверху        
            self.rect.x = random.randrange(WIDTH - self.rect.width)# ограничение по случайному месту по х
            self.rect.y = random.randrange(-100, -40)# ограничение по случайному месту по у
            self.speedy = random.randrange(1, 5) # случайныйвыбор скорости 

class Hirvio(pygame.sprite.Sprite):# свойства спрайты hirvio.
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #запускает инициализатор встроенных классов Sprite
        self.image = hirvio #определить свойство image.
        #у каждого спрайта в Pygame должно быть два свойства: image и rect.сейчас это кусе 30 на 40
        self.rect = self.image.get_rect()#определим rect спрайта.
        self.rect.x = random.randrange(WIDTH - self.rect.width)#ограничим случайное положение rect по х шириной 
        self.rect.y = random.randrange(-100, -40)# то же высотой появляется сверху
        self.speedy = random.randrange(3, 8)#определим скорость спрайта случайной скоростью от 1 до 8 по у
        self.speedx = random.randrange(-3, 3)# и от -3 до 3 по х
  
    def update(self):#для функции обновления нужно задать движения спрайта с определенной скоростью,
        self.rect.x += self.speedx# берем скорости из self.speedx
        self.rect.y += self.speedy# и self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
       # когда спрайт доберется до низа перенесем его в случайное место вверху        
            self.rect.x = random.randrange(WIDTH - self.rect.width)# ограничение по случайному месту по х
            self.rect.y = random.randrange(-100, -40)# ограничение по случайному месту по у
            self.speedy = random.randrange(5, 10) # случайный выбор скорости 

# Цикл игры
game_over = True #Создадим в начале переменную game_over:
running = True
while running:
    if game_over:
        show_go_screen()#перейти к функции
        game_over = False
        all_sprites = pygame.sprite.Group()#собираем все спрайты что бы обновлять и прорисовывать их вместе а не по одному
        mobs = pygame.sprite.Group()
        coins = pygame.sprite.Group()
        hirvios = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)# нужно добавить спрайт в группу all_sprites.
        score = 0

        for i in range(6):#монет много,нужно создать группу coins для них всех
            c = Coin()
            all_sprites.add(c)
            coins.add(c)

        for i in range(8):#Треугольников много,нужно создать группу mobs для них всех
            m = Mob()
            all_sprites.add(m)
            mobs.add(m)
            
        for i in range(1):#Врагов много,нужно создать группу hirvios для них всех
            h = Hirvio()
            all_sprites.add(h)
            hirvios.add(h)

    # Держим цикл на правильной скорости
    clock.tick(FPS)# tick() просит pygame определить, сколько занимает цикл,и сделать паузу, чтобы цикл длился нужно время.
    # Ввод процесса (события)
    for event in pygame.event.get():
        # проверка для закрытия окна
        if event.type == pygame.QUIT:#событие,стартует после нажатия крестика передает False переменной running
            running = False

    # Обновление
    all_sprites.update()

    # Проверка, не ударил ли robot монету если True монета пропадает
    hits = pygame.sprite.spritecollide(player,coins,True)
    #Если просто удалять coin, то появится проблема: они закончатся.
    # Нужно проходить циклом по hits и для каждого пропавшей монеты создать новую.
    for hit in hits:
        score += 5 #если событие произошло +5 очков
        hit_sound.play()#играем звук столкновения монеты и робота
        c = Coin()
        all_sprites.add(c)
        coins.add(c)
    # Проверка, не ударил ли robot hirvio если True конец игры
    hits = pygame.sprite.spritecollide(player, hirvios, False)
    if hits:  
        #gameOver_sound.play()#играем звук gameOver
        #player.kill() игрок был убит этой функцией 
        #if not player.alive(): эта функция проверяет жив спрайт иди нет  
       #game_over = True
       running = False
       show_go_screen()#tckb столкновение с hirvi переходим к началу
 
    # Проверка, не ударил ли robot моб если True mob пропадает
    hits = pygame.sprite.spritecollide(player, mobs, True)
    if hits:
        score -= 10 ##если это событие произошло -10 очков
        running = True

    #if not player.alive(): #эта функция проверяет жив спрайт иди нет  
        #game_over = True

    # Рендеринг(отрисовка)
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, str(score), 18, WIDTH / 2, 10)#вызов функц отвечающий за рисование счета
    # экран на котором рисуем,счет,размер шрифта, положение по х и по у 

    # После отрисовки всего, переворачиваем экран
    pygame.display.flip()

pygame.quit()

"""#__________________________________________________________________________________
#Считаем очки
class Score:
    # конструктор
    def __init__(self, canvas, color):
        # в самом начале счёт равен нулю
        self.score = 0
        # будем использовать наш холст
        self.canvas = canvas
        # создаём надпись, которая показывает текущий счёт, делаем его нужно цвета и запоминаем внутреннее имя этой надписи
        self.id = canvas.create_text(450, 10, text=self.score, font=('Courier', 15), fill=color)
    # обрабатываем касание платформы
    def hit(self):
        # увеличиваем счёт на единицу
        self.score += 1
        # пишем новое значение счёта 
        self.canvas.itemconfig(self.id, text=self.score)
            
#__________________________________________________________________________________


#______________________________________________________________________________
#Робот перемещается во все четыре стороны
import pygame
pygame.init()
window = pygame.display.set_mode((640, 480))
robo = pygame.image.load("robo.png")
x = 0
y = 0
to_right = False
to_left = False
to_up = False
to_down = False

clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                to_left = True
            if event.key == pygame.K_RIGHT:
                to_right = True
            if event.key == pygame.K_UP:
                to_up  = True
            if event.key == pygame.K_DOWN:
                to_down = True    

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                to_left = False
            if event.key == pygame.K_RIGHT:
                to_right = False
            if event.key == pygame.K_UP:
                to_up  = False
            if event.key == pygame.K_DOWN:
                to_down = False       

        if event.type == pygame.QUIT:
            exit()

    if to_right:
        x += 2
    if to_left:
        x -= 2
    if to_up:
        y -= 2
    if to_down:
        y += 2    

    window.fill((0, 0, 0))
    window.blit(robo, (x, y))
    pygame.display.flip()

    clock.tick(60)


#---------------------------------- готовый модуль с падающими фигурами но робот не вставляется        
import pygame
import random
# Название игры
pygame.display.set_caption("First Pygame GAME")
pygame.init()
naytto = pygame.display.set_mode((640, 480))
robo = pygame.image.load("kolikko.png")
robo1 = pygame.image.load("ovi.png")
robo2 = pygame.image.load("hirvio.png")
robo3 = pygame.image.load("robo.png")

x3 = 320
y3 = 390
to_right = False
to_left = False
to_up = False
to_down = False

clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                to_left = True
            if event.key == pygame.K_RIGHT:
                to_right = True
            if event.key == pygame.K_UP:
                to_up  = True
            if event.key == pygame.K_DOWN:
                to_down = True    

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                to_left = False
            if event.key == pygame.K_RIGHT:
                to_right = False
            if event.key == pygame.K_UP:
                to_up  = False
            if event.key == pygame.K_DOWN:
                to_down = False       

        if event.type == pygame.QUIT:
            exit()

    if to_right:
        x3 += 2
    if to_left:
        x3 -= 2
    if to_up:
        y3 -= 2
    if to_down:
        y3 += 2    
           
    naytto.fill((0, 0, 0))
    naytto.blit(robo3, (x3, y3))
    pygame.display.flip()
    clock.tick(10)
               


def zikl ():   
    for i in range(10):                     
        x = random.randint(60, 640)                   
        y = 0
        nopeus = 0.1
        kello = pygame.time.Clock()        
        while True:
            for tapahtuma in pygame.event.get():
                if tapahtuma.type == pygame.QUIT:
                    exit()

            naytto.fill((0, 0, 0))
            naytto.blit(robo, (x, y))
            pygame.display.flip()            
            y += nopeus             
            
            if  y >= 480-robo.get_height() :
                zikl1 ()
          
def zikl1 ():   
    for i in range(10):                     
        x1 = random.randint(60, 640)                   
        y1 = 0
        nopeus1 = 0.2
        kello = pygame.time.Clock()        
        while True:
            naytto.fill((0, 0, 0))
            naytto.blit(robo1, (x1, y1))
            pygame.display.flip()            
            y1 += nopeus1             
            
            if  y1 >= 480-robo1.get_height() :
                zikl2 ()
    
    
def zikl2 ():   
    for i in range(10):                     
        x2 = random.randint(60, 640)                   
        y2 = 0
        nopeus2 = 0.3
        kello = pygame.time.Clock()

        while True:            
            naytto.fill((0, 0, 0))
            naytto.blit(robo2, (x2, y2))
            pygame.display.flip()            
            y2 += nopeus2             
            
            if  y2 >= 480-robo1.get_height() :
                zikl ()
    #kello.tick(100) 
#zikl ()

#------------модуль с роботом который не вставляется             
                
zikl ()"""    
