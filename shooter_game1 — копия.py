from pygame import *
from random import randint


#класс-родитель для спрайтов 
class GameSprite(sprite.Sprite):
    #конструктор класса
    def __init__(self, player_image, player_x, player_y, player_speed, w, h):
        super().__init__()
 
        # каждый спрайт должен хранить свойство image - изображение
        self.image = transform.scale(image.load(player_image), (65, 65))
        self.speed = player_speed
 
        # каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        mw.blit(self.image, (self.rect.x, self.rect.y))

#класс-наследник для спрайта-игрока (управляется стрелками)
class Player(GameSprite):
    fire_reload = 10
    live = 3

    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_height - 80:
            self.rect.y += self.speed
        if keys[K_SPACE]:
            if self.fire_reload <= 0:
                self.fire()
                self.fire_reload = 30

        self.fire_reload -= 1

    def fire(self):
        #fire_sound.play() 
        shot = Shot('fire.png',
                self.rect.x, self.rect.y,
                4, 
                40, 40) 
        shots.add(shot)



class Star(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.kill()

class Ufo(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.kill()
            global miss
            miss += 1

class Shot(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < -100:
            self.kill()
            
class Boom(sprite.Sprite):
    def __init__(self, ufo_center, boom_sprites, booms) -> None:
        super().__init__() 
        #global booms, boom_sprites              
        self.frames = boom_sprites        
        self.frame_rate = 1   
        self.frame_num = 0
        self.image = boom_sprites[0]
        self.rect = self.image.get_rect()
        self.rect.center = ufo_center
        self.add(booms)
    
    def next_frame(self):
        self.image = self.frames[self.frame_num]
        self.frame_num += 1
        
    
    def update(self):
        self.next_frame()
        if self.frame_num == len(self.frames)-1:
            self.kill()


    
def create_star():
    star = Star('star.png',
                randint(0,win_width), -10,
                randint(3, 10), 20, 20) 
    stars.add(star)
    

def create_ufo():
    ufo = Ufo('ufo1.png',
                randint(0,win_width), -50,
                2, 90, 90) 
    ufos.add(ufo)
    
def sprites_load(folder:str, file_name:str, size:tuple, colorkey:tuple = None):    
    sprites = []
    load = True
    num = 1
    while load:
        try:
            print(num)
            spr = transform.scale(image.load(f'{folder}\\{file_name}{num}.png'),size)
            if colorkey: spr.set_colorkey((0,0,0))
            sprites.append(spr)
            num += 1
            
        except:
            load = False
    return sprites


mixer.init()
#fon_sound = mixer.Sound('fon1.mp3')
#fire_sound = mixer.Sound('fire2.mp3')
#boom_sound = mixer.Sound('boom1.mp3')
#mixer.music.load('fon1.mp3')
#fon_sound.set_volume(0.6)
#fon_sound.play(-1)


win_width = 800
win_height = 600

stars = sprite.Group()
ufos = sprite.Group()
meteors = sprite.Group()
shots = sprite.Group()
booms = sprite.Group()

ticks = 0
miss = 0


#mw = display.set_mode((win_width, win_height), FULLSCREEN)
mw = display.set_mode((win_width, win_height))
display.set_caption("Космические рейнджеры")
clock = time.Clock()


fon =  transform.scale(image.load('fon1.jpg'), (win_width, win_height))
ship = Player('ship.png', win_width/2, win_height-80, 5, 80, 80)

boom_sprites = sprites_load('boom', 'boom', (100,100), (0,0,0))
#print(boom_sprites)
game = True
finish = False

font.init()
font1 = font.Font(None, 36)

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False 
        elif e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                game = quit()

    if not finish:
        
        if ticks % 10 == 0:
            create_star()

        if ticks % 90 == 0:
            create_ufo()

        mw.blit(fon, (0,0))
        
    
        stars.update()
        shots.update()
        ufos.update()
        ship.update()
        booms.update()

        collisions = sprite.groupcollide(shots, ufos, True, True)    
        for ufo, shot in collisions.items():       
            Boom(ufo.rect.center, boom_sprites, booms)
            #boom_sound.play()

        stars.draw(mw)
        shots.draw(mw)
        ufos.draw(mw)
        booms.draw(mw)    
        ship.reset()

        mw.blit(font1.render("Пропущено: " + str(miss), 1, 
                (255, 255, 255)), (10,10))
        mw.blit(font1.render("Жизни: " + str(ship.live), 1, 
                (255, 255, 255)), (600,10))

        if miss >= 3: 
            finish = True

    else:
        mw.blit(fon, (0,0))


    ticks += 1
    display.update()
    clock.tick(60)
