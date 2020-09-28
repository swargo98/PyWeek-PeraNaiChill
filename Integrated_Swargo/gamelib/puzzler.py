
# Sliding Picture Puzzle Game
# Developed in python 3.7 and pygame

import pygame
import random
import sys
import time

def initialize():

   global window_width, window_height, tile_width, tile_height, coloumn, rows, img_list, background, sprite, empty_tile, emptyc,emptyr
   global color, white, black, tiles, gameWindow, level, start_background
   window_width = 800
   window_height = 480

   tile_width = 150
   tile_height = 100

   coloumn = 4
   rows = 4

   pygame.init()
   gameWindow = pygame.display.set_mode((window_width, window_height))
   pygame.display.set_caption("Map_Puzzler")
   start_background = pygame.image.load("data/puzzler/start_background.png")
   gameWindow.blit(start_background, (0, 0))
   pygame.display.update()
   time.sleep(5)

   img_list = [0, "island1.jpg"]
   background = pygame.image.load("data/puzzler/background.png")
   sprite = pygame.image.load("data/puzzler/Idle.png")

   empty_tile = (3, 3)
   emptyc, emptyr = 3, 3

   color = (255, 130, 130)
   white = (215, 215, 215)
   black = (0, 0, 0)

   tiles = {}

   gameWindow.fill(white)
   gameWindow.blit(background, (0, 0))
   gameWindow.blit(sprite, (620,180))
   pygame.display.update()

   level = 2

   start()

def message(v1,u1,text):
   rect_w = 70
   rect_h = 70

   font = pygame.font.SysFont('comicsansms',25)
   TextSurf = font.render(text,True,black)
   TextRect = TextSurf.get_rect()
   TextRect.center = ((v1*rect_w+((rect_w-3)/2)),
                      (u1*rect_h+(rect_h/2)))

   gameWindow.blit(TextSurf,TextRect)
   pygame.display.update()


def labels(v1,u1,text,color,size=20):
   font = pygame.font.SysFont('comicsansms',size)
   TextSurf = font.render(text,True,color)
   TextRect = TextSurf.get_rect()
   TextRect.center = (v1,u1)

   gameWindow.blit(TextSurf,TextRect)
   pygame.display.update()

def check():

   global game_over
   j,k = 0,0
   tag_list = []

   for i in range(1,17):

      tag = "tag"+str(i)

      if tiles[(j,k)][1] == tag:
         tag_list.append(tag)
         j += 1
         if j > 3:
            k += 1
            j = 0

      else:
         break

   if i == 16:
      print("GAME FINISHED")
      game_over = True

def shift (c, r) :

   global emptyc, emptyr, empty_tile, tile_width, tile_height
   rect_color = (255,255,255)
   gameWindow.blit(tiles[(c, r)][0],(emptyc*tile_width, emptyr*tile_height))
   gameWindow.blit(sprite, (620, 180))

   gameWindow.blit(
        tiles[empty_tile][0],
        (c*tile_width, r*tile_height))

   temp = tiles[(c,r)]

   tiles[(c,r)] = tiles[(emptyc,emptyr)]
   tiles[(emptyc,emptyr)] = temp

   emptyc, emptyr = c, r

   pygame.draw.rect(gameWindow,rect_color,[c*tile_width,r*tile_height,
                                   tile_width-1,tile_height-1])

   empty_tile = (emptyc, emptyr)

   pygame.display.flip()

def shuffle() :
   # keep track of last shuffling direction to avoid "undo" shuffle moves
   last_r = 0
   for i in range(100):
      # slow down shuffling for visual effect
      pygame.time.delay(50)
      while True:
         # pick a random direction and make a shuffling move
         # if that is possible in that direction
         r = random.randint(1, 4)
         if (last_r + r == 5):
            # don't undo the last shuffling move
            continue
         if r == 1 and (emptyc > 0):
            shift(emptyc - 1, emptyr) # shift left
         elif r == 4 and (emptyc < coloumn - 1):
            shift(emptyc + 1, emptyr) # shift right
         elif r == 2 and (emptyr > 0):
            shift(emptyc, emptyr - 1) # shift up
         elif r == 3 and (emptyr < rows - 1):
            shift(emptyc, emptyr + 1) # shift down
         else:
            # the random shuffle move didn't fit in that direction
            continue
         last_r=r
         break # a shuffling move was made

def start():
   f=1
   global game_over, image
   game_over = False
   level = 2
   img = img_list[f]
   image = pygame.image.load("data/puzzler/Res/"+img)

   #self.gameWindow.fill((190,190,190))
   for r in range (coloumn):

      for c in range (rows):

         tag = "tag"+str(f)

         tile = image.subsurface(c*tile_width,r*tile_height,
                           tile_width-1,tile_height-1)
         #print(tile)
         f += 1
         tiles [(c, r)] = (tile,tag)

         if(c,r) == empty_tile:
            pygame.draw.rect(gameWindow,(255,255,255),
                         [c*tile_width,r*tile_height,
                          tile_width-1,tile_height-1])
            break

         gameWindow.blit(tile,(c*tile_width,r*tile_height))
         pygame.display.update()
         #print(tile)

   #print(tiles)
   text = "Level "+str(level)
   labels(75,425,text,(253,232,39))
   labels(300,425,"Click to start Game",(253, 232, 39))

   pygame.display.update()

def main():

   initialize()
   global started, show_sol, game_over
   game_over = False
   started = False
   show_sol = False
   #self.gameWindow.fill((190,190,190),(150,610,300,40))

   while True:
      if game_over:
         gameWindow.blit(background, (0, 0))
         gameWindow.blit(sprite, (620,180))
         labels(400, 200, "Congratulations!! Well played, Press 'q' to continue",(0,0,255),30)
         pygame.display.update()
         #time.sleep(15)
         #break
         #self.labels(300,625,"Click to next Level",(0,0,255))

      for event in pygame.event.get():

         #print(event)
         if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

         if (game_over == True and event.type == pygame.KEYDOWN and event.key == pygame.K_q):
            return True
            #pygame.quit()
            #sys.exit()

         if event.type == pygame.MOUSEBUTTONDOWN:

            if not started:
               #self.gameWindow.fill((190, 190, 190), (40, 400, 350, 40))
               gameWindow.blit(background, (0, 0))
               gameWindow.blit(sprite, (620, 180))
               shuffle()
               labels(300,425,"Right click to see Solution",(253,232,39))
               started = True
               count = -1

            elif game_over == False and event.dict['button'] == 1 and count == 0:
               mouse_pos = pygame.mouse.get_pos()
               #print("HI")

               c = int(mouse_pos[0] / tile_width)
               r = int(mouse_pos[1] / tile_height)

               if(c > 3 or r > 3):
                  continue
               if c == emptyc and r == emptyr:
                  continue
               else:
                  shift(c, r)
                  check()

            elif game_over == False and event.dict['button'] == 3:
               saved_image = gameWindow.copy()
               gameWindow.blit(image, (0, 0))
               pygame.display.flip()
               show_sol= True

         elif show_sol and (event.type == pygame.MOUSEBUTTONUP):
            gameWindow.blit (saved_image, (0, 0))
            pygame.display.flip()
            show_sol = False

         count = 0

#main()
