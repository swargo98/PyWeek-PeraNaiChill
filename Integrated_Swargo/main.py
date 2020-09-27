import pygame
from gamelib import peranaichill_running
from gamelib import runMaze
from gamelib import animal_hunt

#peranaichill_running.main()
#runMaze.main()
#animal_hunt.main()

pygame.init()

 # size of the game window
win_width, win_height = 1280, 720

# Font for game over window
FONT = "freesandsbold.ttf"

win_width = 800
win_height = 480
win_size = win_width, win_height

window = pygame.display.set_mode(win_size)
fade = pygame.Surface((win_width, win_height))
fade.fill((0,0,0))


# set_caption(title, icontitle=None) -> None
#If the display has a window title, this function will change the name on the window
pygame.display.set_caption("PeraNaiChill")

start = 1
level1 = 0
level2 = 0
level3 = 0
font1 = pygame.font.SysFont('Calibri',24,True,True)

running = True

while running:
    for event in pygame.event.get():
        if (event.type == pygame.QUIT) or \
                (event.type == pygame.KEYDOWN \
                 and (event.key == pygame.K_ESCAPE or event.key == pygame.K_q)):
            running = False

    if start == 1:
        breakLoop = True
        window.fill((255,255,255))
        while breakLoop:
            StartText = font1.render('Press any key to start ', 1, (0, 0, 0))
            window.blit(StartText, (450, 50))
            pygame.display.flip()
            for event in pygame.event.get():
                if (event.type == pygame.QUIT) or \
                        (event.type == pygame.KEYDOWN \
                         and (event.key == pygame.K_ESCAPE or event.key == pygame.K_q)):
                    running = False
                    start = 0
                    breakLoop = False
                if (event.type == pygame.KEYDOWN):
                    start = 0
                    breakLoop = False
                    level1 = 1
    elif level1 == 1:
        level1end = runMaze.main()
        if level1end == True:
            level1 = 0
            #level2 = 1
            start = 1



