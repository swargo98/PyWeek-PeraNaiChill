import pygame
from pygame import mixer
from gamelib import peranaichill_running
from gamelib import runMaze
from gamelib import animal_hunt

#peranaichill_running.main()
#runMaze.main()
#animal_hunt.main()

pygame.init()

 # size of the game window
win_width, win_height = 800, 480

# Font for game over window
FONT = "freesandsbold.ttf"


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

# Sound
mixer.music.load("data/audios/bgmusic.wav")
mixer.music.play(-1)

player_image = pygame.image.load('data/Image/player.png').convert_alpha()
bg = pygame.image.load('data/tileset_1(main)/BG/BG1.jpg').convert_alpha()

running = True
GameEnd  = 0
score = 0

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
            window.blit(bg, (0, 0))
            window.blit(player_image, (50, 150))
            StartText = font1.render('Press any key to start ', 1, (0, 0, 0))
            window.blit(StartText, (450, 50))
            pygame.display.flip()
            if GameEnd == 1:
                scoreText = font1.render('Score: ' + score, 1, (0, 0, 0))
                window.blit(scoreText, (400, 200))

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
        level1end = peranaichill_running.main()

        if level1end == True:
            level1 = 0
            level3 = 1
        else:
            level1 = 0
            start = 1


    elif level3 == 1:
        level3end = runMaze.main()
        if level3end == True:
            level3 = 0
            level4 = 1
        else:
            level3 = 0
            start = 1

    elif level4 == 1:
        level4end,score = animal_hunt.main()
        print(score)
        if level4end == True:
            start = 1
            GameEnd = 1
            level4 = 0




