import pygame
from pygame.locals import *
import os
import sys
import math
from pygame.image import load as imload
import random

pygame.init()

W, H = 800, 447
win = pygame.display.set_mode((W,H))
pygame.display.set_caption('PeraNaiChill')

bg_path = "data/tileset_1(main)/BG/"
char_path = "data/character"
obj_path = "data/tileset_1(main)/Object/"
tile_path = "data/tileset_1(main)/Tiles/"

target = 50
lives = 10

bg = imload(os.path.join(bg_path,'BG.png')).convert()
bgX = 0
bgX2 = bg.get_width()

class player(object):
    run = [pygame.image.load(os.path.join(char_path, "Run__00" + str(x) + '.png')) for x in range(1, 10)]
    still = [pygame.image.load(os.path.join(char_path, "Idle__00" + str(x) + '.png')) for x in range(1, 10)]
    death = [pygame.image.load(os.path.join(char_path, "Dead__00" + str(x) + '.png')) for x in range(1, 10)]
    jump = [pygame.image.load(os.path.join(char_path, "Jump__00" + str(x) + '.png')) for x in range(1, 10)]
    slide = [pygame.image.load(os.path.join(char_path, "slide__00" + str(x) + '.png')) for x in range(1, 10)]

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.jumping = False
        self.sliding = False
        self.running = False
        self.is_still = True
        self.is_dead = False
        self.right_pressed = False
        self.left_pressed = False
        self.left_movement = True
        self.slideCount = 0
        self.jumpCount = 0
        self.runCount = 0
        self.stillCount = 0
        self.deathCount = 0
        self.slideUp = False
        self.hitbox = ()
        self.life_remaining = lives
        self.score = 0
        self.revive_x = 0

    def draw_player(self, win):
        if (self.right_pressed == False) and self.left_movement == True:
            self.x-=3
        if self.is_still:
            if self.stillCount > 26:
                self.stillCount = 0
            picture = self.still[self.stillCount // 3]
            picture = pygame.transform.scale(picture, (self.width, self.height))
            win.blit(picture , (self.x, self.y))
            self.stillCount += 1
            self.hitbox = (self.x + 4, self.y, self.width - 12, self.height)

        if self.running:
            if self.runCount > 26:
                self.runCount = 0
                self.running = False
                self.sliding = False
                self.jumping = False
                self.is_still = True
                self.right_pressed = False
                self.left_movement = True
            picture = self.run[self.runCount // 3]
            self.x += 4
            picture = pygame.transform.scale(picture, (self.width, self.height))
            win.blit(picture , (self.x, self.y))
            self.runCount += 1
            self.hitbox = (self.x + 4, self.y, self.width - 12, self.height)

        if self.jumping:
            if self.jumpCount>35:
                self.y += 8
            else:
                self.y -= 8
            picture = self.jump[self.jumpCount // 8]
            picture = pygame.transform.scale(picture, (self.width, self.height))
            win.blit(picture, (self.x, self.y))
            self.jumpCount += 1
            #if self.right_pressed:
            self.x += 4
            if self.jumpCount > 71:
                self.jumpCount = 0
                self.running = False
                self.sliding = False
                self.jumping = False
                self.is_still = True
                self.right_pressed = False
                self.left_movement = True
                self.runCount = 0
            self.hitbox = (self.x + 4, self.y, self.width - 24, self.height - 10)

        if self.sliding:
            picture = self.slide[self.slideCount // 8]
            picture = pygame.transform.scale(picture, (self.width, self.height))
            win.blit(picture, (self.x, self.y))
            self.slideCount += 1
            self.x += 4
            if self.slideCount > 71:
                self.slideCount = 0
                self.running = False
                self.sliding = False
                self.jumping = False
                self.is_still = True
                self.right_pressed = False
                self.left_movement = True
                self.runCount = 0

            self.hitbox = (self.x+ 4,self.y,self.width-10,self.height)

        if self.x<-64:
            #print("baire gechega")
            self.left_movement=False
            self.is_dead=True
            self.is_still = False
            self.x = 0

        if self.x>750:
            #print("baire gechega")
            self.x = 736

        if self.is_dead:
            self.y = 313
            #self.x = self.revive_x
            picture = self.death[self.deathCount // 3]
            picture = pygame.transform.scale(picture, (self.width, self.height))
            win.blit(picture , (self.x, self.y))
            if(self.deathCount < 25):
                self.deathCount += 1
                self.x += 0.5
                self.is_still = False

            '''if(self.deathCount == 25 and self.life_remaining>0):
                self.is_still = True
                self.is_dead = False
                self.life_remaining-=1
                print(self.deathCount, self.life_remaining, self.is_dead, self.x)'''

        #pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

class land(object):
    tileimg = [imload(os.path.join(tile_path, str(x) + '.png')) for x in range(1, 4)]

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.left_movement = True
        self.is_visible = True
        self.hitbox = ()

    def draw_tile(self, win):
        if self.is_visible:
            if self.left_movement == True:
                self.x -= 3
            if self.x < -self.width:
                self.is_visible = False
            for i in range (3):
                picture = self.tileimg[i]
                picture = pygame.transform.scale(picture, (int(self.width/3), self.height))
                win.blit(picture , (self.x+i*int(self.width/3), self.y))
            self.hitbox = (self.x, self.y, self.width, self.height)

            #pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

class sea(object):
    tileimg = [imload(os.path.join(tile_path, str(17) + '.png')) for x in range(1, 3)]

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.left_movement = True
        self.is_visible = True
        self.hitbox = (self.x, self.y, self.width, self.height)

    def draw_tile(self, win):
        if self.is_visible:
            if self.left_movement == True:
                self.x -= 3
            if self.x < -self.width:
                self.is_visible = False
            for i in range (1):
                picture = self.tileimg[i]
                picture = pygame.transform.scale(picture, (self.width, self.height))
                win.blit(picture , (self.x+i*self.width , self.y))
            self.hitbox = (self.x, self.y, self.width, self.height)

            #pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

    def collide(self, rect):
        midpoint = rect[0] + (rect[2]//2)
        if midpoint > self.hitbox[0] and midpoint < self.hitbox[0] + self.hitbox[2]:
            print("X clear", rect[1] + rect[3], self.hitbox[1])
            if rect[1] + rect[3] >= self.hitbox[1]:
                print("Y clear")
                return True
        return False

class mushroom(object):
    tileimg = [imload(os.path.join(obj_path, "Mushroom_" + str(x) + '.png')) for x in range(1, 3)]

    def __init__(self, x, y, width, height, mushroomtype):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.mushroomtype = mushroomtype
        self.left_movement = True
        self.is_visible = True
        self.hitbox = (self.x, self.y, self.width, self.height)

    def draw_tile(self, win):
        if self.is_visible:
            if self.left_movement == True:
                self.x -= 3
            if self.x < -self.width:
                self.is_visible = False
            picture = self.tileimg[self.mushroomtype]
            picture = pygame.transform.scale(picture, (self.width, self.height))
            win.blit(picture , (self.x, self.y))
            self.hitbox = (self.x, self.y, self.width, self.height)

            #pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)
    def collide(self, rect):
        rect_right = rect[0] + rect[2]
        rect_bottom = rect[1] + rect[3]
        self_right = self.hitbox[0] + self.hitbox[2]
        self_bottom = self.hitbox[1] + self.hitbox[3]

        if (rect[0] >= self.hitbox[0] and rect[0] <= self_right) or (rect_right >= self.hitbox[0] and rect_right <= self_right) or (rect[0] < self.hitbox[0] and rect_right >= self_right):
            if (rect[1] >= self.hitbox[1] and rect[1] <= self_bottom) or (rect_bottom >= self.hitbox[1] and rect_bottom <= self_bottom)or (rect[1] < self.hitbox[1] and rect_bottom >= self_bottom):
                self.is_visible = False
                return True
        return False

class bird(object):
    tileimg = [imload(os.path.join(obj_path, "tile00" + str(x) + '.png')) for x in range(0, 9)]
    tileimg2 = [imload(os.path.join(obj_path, "tile00" + str(8-x) + '.png')) for x in range(0, 9)]

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.left_movement = True
        self.is_visible = True
        self.framecount = 0
        self.hitbox = (self.x, self.y+20, self.width, self.height-30)

    def draw_tile(self, win):
        if self.is_visible:
            if self.left_movement == True:
                self.x -= 5
            if self.x < -self.width:
                self.is_visible = False
            if(self.framecount%54<27):
                picture = self.tileimg[(self.framecount//3)%9]
            else:
                picture = self.tileimg2[(self.framecount//3)%9]
            picture = pygame.transform.scale(picture, (self.width, self.height))
            win.blit(picture , (self.x, self.y))
            self.hitbox = (self.x, self.y+20, self.width, self.height-30)
            self.framecount+=1

            #pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

    def collide(self, rect):
        rect_right = rect[0] + rect[2]
        rect_bottom = rect[1] + rect[3]
        self_right = self.hitbox[0] + self.hitbox[2]
        self_bottom = self.hitbox[1] + self.hitbox[3]

        if (rect[0] >= self.hitbox[0] and rect[0] <= self_right) or (rect_right >= self.hitbox[0] and rect_right <= self_right):
            #print("X clear", rect[1] + rect[3], self.hitbox[1])
            if (rect[1] >= self.hitbox[1] and rect[1] <= self_bottom) or (rect_bottom >= self.hitbox[1] and rect_bottom <= self_bottom):
                #print("BIRD Y clear")
                return True
        return False

def redrawWindow():
    win.blit(bg, (bgX, 0))  # draws our first bg image
    win.blit(bg, (bgX2, 0))  # draws the seconf bg image
    player.draw_player(win)
    for tile in tileset:
        tile.draw_tile(win)
    for mush in mushrooms:
        mush.draw_tile(win)
    for b in birds:
        b.draw_tile(win)
    text = font.render('Score: ' + str(player.score), 1, (0, 0, 0))
    win.blit(text, (650, 10))
    text = font.render('Lives: ' + str(player.life_remaining), 1, (0, 0, 0))
    win.blit(text, (20, 10))
    pygame.display.update()  # updates the screen

#main_loop
font = pygame.font.SysFont('comicsans', 30, True)
player = player(400,313,64,64)
tileset = [
    sea(0,377, 64, 100),
    sea(64,377, 64, 100),
    sea(128,377, 64, 100),
    sea(192,377, 64, 100),
    sea(256,377, 64, 100),
    land(320,377, 192, 100),
    sea(512,377, 64, 100),
    sea(576,377, 64, 100),
    land(640,377, 192, 100),
]

mushrooms = [mushroom(600,250, 32, 32, 0),]

birds = [bird(800, 200, 64, 64)]

Tile = land(400,377, 64, 100)
Tile2 = sea(600,377, 64, 100)
run = True
speed = 60
clock = pygame.time.Clock()

while run:
    redrawWindow()

    if player.is_dead == False:
        if player.score<target:
            print(player.score, target)
            bgX -= 1
            bgX2 -= 1

    if bgX < bg.get_width() * -1:
        bgX = bg.get_width()

    if bgX2 < bg.get_width() * -1:
        bgX2 = bg.get_width()

    for event in pygame.event.get():  # Loop through a list of events
        if event.type == pygame.QUIT:  # See if the user clicks the red x
            run = False    # End the loop
            pygame.quit()  # Quit the game
            quit()

    if player.is_dead or player.score>=target:
        player.left_movement = False
        if player.is_dead:
            player.is_dead = True
            player.is_still = False
        else:
            player.is_dead = False
            player.is_still = True

        for tile in tileset:
            tile.left_movement = False

        for mush in mushrooms:
            mush.left_movement = False

        for b in birds:
            b.left_movement = False


    if player.is_dead == False:
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE] or keys[pygame.K_UP]:  # If user hits space or up arrow key
            if not (player.jumping):  # If we are not already jumping
                player.running = False
                player.sliding = False
                player.jumping = True
                player.is_still = False
                player.right_pressed = False
                player.left_movement = True

        if keys[pygame.K_RIGHT]:  # If user hits right arrow key
            player.right_pressed = True
            if player.is_still:
                player.running = True
                player.sliding = False
                player.jumping = False
                player.is_still = False
                player.left_movement = True


        if keys[pygame.K_DOWN]:
            if player.is_still:
                player.running = False
                player.sliding = True
                player.jumping = False
                player.is_still = False
                player.right_pressed = False
                player.left_movement = True

        last_x = tileset[-1].x
        last_width = tileset[-1].width

        last_mushroom_x = mushrooms[-1].x
        last_bird_x = birds[-1].x

        if last_x+last_width <= 800:
            #r = random.randrange(0, 2)
            if last_width==192:
                r2 = random.randrange(0, 2)
                tileset.append(sea(last_x+last_width, 377, 64,100))
                if r2 == 1:
                    tileset.append(sea(last_x + last_width +64, 377, 64, 100))
            elif last_width==64:
                r2 = random.randrange(0, 2)
                tileset.append(land(last_x+last_width, 377, 192,100))
                if r2 == 1:
                    tileset.append(land(last_x + last_width + 192, 377, 192, 100))

        if len(mushrooms)<3:
            r = random.randrange(10, 300)
            mush_x = 800
            if(800 - last_mushroom_x)<200:
                mush_x = 1000
            mushrooms.append(mushroom(mush_x, r, 32, 32, r%2))


        for tile in tileset:
            if tile.is_visible == False:
                tileset.pop(tileset.index(tile))
            '''if tile.width == 192:
                player.revive_x = tile.x + 96'''
            if tile.width == 64:
                if tile.collide(player.hitbox):
                    if player.life_remaining > 0:
                        player.life_remaining-=1
                        player.x -= 100
                        player.jumping = False
                        player.running = False
                        player.is_still = True
                        player.right_pressed = False
                    else:
                        player.left_movement = False
                        player.is_dead = True
                        player.is_still = False
            #if player.is_dead:
                #tile.left_movement = False

        for mush in mushrooms:
            if mush.is_visible == False:
                mushrooms.pop(mushrooms.index(mush))
            if mush.collide(player.hitbox):
                player.score+=5

        for b in birds:
            if b.is_visible == False:
                birds.pop(birds.index(b))
            if b.collide(player.hitbox):
                if player.life_remaining>0:
                    b.is_visible = False
                    player.life_remaining-=1
                else:
                    player.left_movement = False
                    player.is_dead = True
                    player.is_still = False
                    player.jumping = False
                    player.sliding = False

        if len(birds)<1:
            r = random.randrange(10, 300)
            bird_x = 800
            if(800 - last_bird_x)<200:
                bird_x = 1000
            birds.append(bird(bird_x, r, 64, 64))




    clock.tick(speed)
