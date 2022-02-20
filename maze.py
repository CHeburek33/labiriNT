from pygame import *
from time import sleep
class GameSprite(sprite.Sprite):
   def __init__(self, player_image, player_x, player_y, player_speed):
       super().__init__()
       self.image = transform.scale(image.load(player_image), (65, 65))
       self.speed = player_speed
       self.rect = self.image.get_rect()
       self.rect.x = player_x
       self.rect.y = player_y
       
 
   def reset(self):
       window.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite):
    def Update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_UP] and self.rect.y >5 :
            self.rect.y -= self.speed
        if keys_pressed[K_DOWN]and self.rect.y <600:
            self.rect.y+= self.speed
        if keys_pressed[K_LEFT]and self.rect.x >5:
            self.rect.x -= self.speed
        if keys_pressed[K_RIGHT]and self.rect.x <800:
            self.rect.x += self.speed
class Enemy(GameSprite):
    direction = 1
    def Update(self):
        # 0 = Право, 1 = Лево
        if self.direction == 1:
            self.rect.x -= 5
        if self.direction == 0:
            self.rect.x += 5
        if self.rect.x <= 620:
            self.direction = 0
        if self.rect.x >= 820:
            self.direction = 1
class Wall(sprite.Sprite):
    def __init__(self,color_1,color_2,color_3,wall_x,wall_y,wall_width,wall_height):
        super().__init__()
        self.color_1 = color_1
        self.color_2 = color_2
        self.color_3 = color_3
        self.width = wall_width
        self.height = wall_height
        self.image = Surface((self.width,self.height))
        self.image.fill((color_1,color_2,color_3))
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y
    def draw_wall(self):
        window.blit(self.image,(self.rect.x,self.rect.y))
 
win_width = 900
win_height = 700
window = display.set_mode((win_width, win_height))
display.set_caption("Maze")
background = transform.scale(image.load("background.jpg"), (win_width, win_height))

player = Player('hero.png', 5, win_height - 80, 4)
cyborg = Enemy('cyborg.png', win_width - 80, 500, 2)
final = GameSprite('treasure.png', win_width - 120, win_height - 80, 0)

wall_1 = Wall(55, 140, 169,56,78,150,45)
wall_2 = Wall(55, 140, 169,56,78,45,150)
wall_3 = Wall(55, 140, 169,560,78,150,45)
walls = [wall_1,wall_2,wall_3]

game = True
finish = False
clock = time.Clock()
FPS = 60

mixer.init()
mixer.music.load('jungles.ogg')
mixer.music.play()

money = mixer.Sound('money.ogg')
kick = mixer.Sound('kick.ogg')

font.init()
font = font.Font(None,70)
win = font.render(
    'You win',True,(255,215,0)
)
lose = font.render(
    'You Lox',True,(124,215,0)
)
 
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
    if finish != True:
        cyborg.Update()
        player.Update()
        window.blit(background,(0, 0))
        cyborg.reset()
        player.reset()
        wall_1.draw_wall()
        wall_2.draw_wall()
        wall_3.draw_wall()
        final.reset()
        for wall in walls:
            if sprite.collide_rect(player,wall):
                player.rect.x = 5
                player.rect.y = win_height - 80
                window.blit(lose,(win_width/2-80,win_height/2-80))
                display.update()
                kick.play()
                finish = True
                time.delay(3000)
                finish = False

        
        if sprite.collide_rect(player,final):
            finish = True
            window.blit(win,(win_width/2-80,win_height/2-80))
            money.play()
            mixer.music.stop()
    display.update()
    clock.tick(FPS)
