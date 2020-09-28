import math
import random

import pygame
from pygame import mixer

# Intialize the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 480))

# Background
background = pygame.image.load('data/animal_hunt_data/animal_hunt_bg.png')
background = pygame.transform.rotozoom(background, 0, 0.54)




# Player
playerImg = pygame.image.load('data/animal_hunt_data/PicsArt_09-25-01.43.48.png')
playerImg = pygame.transform.rotozoom(playerImg, 0, 0.1)
playerX = 370
playerY = 350
playerX_change = 0

# Caption and Icon
pygame.display.set_caption("Animal Hunt")
icon = playerImg
pygame.display.set_icon(icon)



# Enemy
enemy_one_img = []
enemy_one_x = []
enemy_one_y = []
enemy_one_x_change = []
enemy_one_y_change = []

enemy_two_img = []
enemy_two_x = []
enemy_two_y = []
enemy_two_x_change = []
enemy_two_y_change = []
num_of_enemies = 3

enemy_one_image = pygame.image.load('data/animal_hunt_data/PicsArt_09-25-02.06.32.png')
enemy_one_image = pygame.transform.rotozoom(enemy_one_image, 0, 0.08)
enemy_one_image = pygame.transform.flip(enemy_one_image, True, False)


enemy_two_image = pygame.image.load('data/animal_hunt_data/PicsArt_09-25-02.05.07.png')
enemy_two_image = pygame.transform.rotozoom(enemy_two_image, 0, 0.25)


# Bullet

# Ready - You can't see the bullet on the screen
# Fire - The bullet is currently moving

bulletImg = pygame.image.load('data/animal_hunt_data/PicsArt_09-25-01.49.01.png')
bulletImg = pygame.transform.rotozoom(bulletImg, 0, 0.03)

bulletX = 0
bulletY = 350
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"


font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
testY = 10

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x, y):
    #fire = font.render("Lion_value : " + str(fire_value), True, (0, 0, 0))
    #ship = font.render("Spider_value : " + str(ship_value), True, (0, 0, 0))
    total_score= font.render("Total Score : " + str(ship_value+fire_value), True, (0, 0, 0))
    #screen.blit(fire, (x, y))
    #screen.blit(ship, (500-x, y))
    screen.blit(total_score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (0, 0, 0))
    #ship_text = font.render("Lion_value : " + str(ship_value), True, (255, 255, 255))
    #fire_text = font.render("Spider_value : " + str(fire_value), True, (255, 255, 255))
    total_text = font.render("Total Score : " + str(ship_value+fire_value), True, (0, 0, 0))
    if ship_value+fire_value > 10: screen.blit(font.render("Level Succeeded", True, (0, 0, 255)), (200, 330))
    else : screen.blit(font.render("Level Failed", True, (255, 0, 0)), (200, 330))
    screen.blit(over_text, (200, 200))
    screen.blit(total_text, (200, 260))
    #if str(ship_value+fire_value)>50:
    #screen.blit(ship_text, (200, 260))
    #screen.blit(fire_text, (200, 300))



def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(enemy_one_img,enemy_two_img,x1, y1, x2, y2, i):
    screen.blit(enemy_one_img[i], (x1, y1))
    screen.blit(enemy_two_img[i], (x2, y2))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemy_x, enemy_y, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemy_x - bulletX, 2) + (math.pow(enemy_y - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False

def main():
    # Game Loop
    player_image = pygame.image.load('data/Image/player.png').convert_alpha()
    bg = pygame.image.load('data/animal_hunt_data/BG.png').convert_alpha()
    end = False
    start = 1
    running = True
    global playerX, playerY, playerImg, playerX_change, playerY_change, bulletX, bulletY, bulletX_change, bulletY_change, bullet_state, fire_value, ship_value
    # Background Image

    while running:
        # RGB = Red, Green, Blue
        if start == 1:
            breakLoop = True

            enemy_one_img = []
            enemy_one_x = []
            enemy_one_y = []
            enemy_one_x_change = []
            enemy_one_y_change = []

            enemy_two_img = []
            enemy_two_x = []
            enemy_two_y = []
            enemy_two_x_change = []
            enemy_two_y_change = []

            #INITIALIZING ENEMY ONE CO-ORDINATES
            for i in range(num_of_enemies):
                enemy_one_img.append(enemy_one_image)
                enemy_one_x.append(random.randint(0, 736))
                enemy_one_y.append(random.randint(50, 150))
                enemy_one_x_change.append(4)
                enemy_one_y_change.append(10)

            #INITIALIZING ENEMY TWO CO-ORDINATES
            for i in range(num_of_enemies):
                enemy_two_img.append(enemy_two_image)
                enemy_two_x.append(random.randint(0, 736))
                enemy_two_y.append(random.randint(150, 200))
                enemy_two_x_change.append(4)
                enemy_two_y_change.append(40)

            # Score

            fire_value = 0
            ship_value = 0




            while breakLoop:
                screen.blit(bg, (0, 0))
                screen.blit(player_image, (50, 150))
                font1 = pygame.font.SysFont('Calibri', 30, True, True)
                Text = font1.render('Level 4 ', 1, (0, 0, 0))
                StartText = font1.render('Press any key to start ', 1, (0, 0, 0))
                Instructions1 = font1.render('Space_key = shoot ', 1, (0, 0, 0))
                Instructions2 = font1.render('right & left arrow = navigation ', 1, (0, 0, 0))
                screen.blit(Text, (450, 50))
                screen.blit(StartText, (380, 100))
                screen.blit(Instructions1, (250, 200))
                screen.blit(Instructions2, (220, 250))

                pygame.display.flip()
                for event in pygame.event.get():
                    if (event.type == pygame.QUIT) or \
                            (event.type == pygame.KEYDOWN \
                             and (event.key == pygame.K_ESCAPE or event.key == pygame.K_q)):
                        running = False
                        start = False
                        breakLoop = False
                    if (event.type == pygame.KEYDOWN):
                        start = 0
                        breakLoop = False

        else:
            screen.fill((0, 0, 0))
            screen.blit(background, (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                # if keystroke is pressed check whether its right or left
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        playerX_change = -5
                    if event.key == pygame.K_RIGHT:
                        playerX_change = 5
                    if event.key == pygame.K_SPACE:
                        if bullet_state is "ready":
                            bulletSound = mixer.Sound("data/animal_hunt_data/laser.wav")
                            bulletSound.play()
                            # Get the current x cordinate of the spaceship
                            bulletX = playerX
                            fire_bullet(bulletX, bulletY)

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        playerX_change = 0

            # 5 = 5 + -0.1 -> 5 = 5 - 0.1
            # 5 = 5 + 0.1


            playerX += playerX_change
            if playerX <= 0:
                playerX = 0
            elif playerX >= 736:
                playerX = 736

            '''
            # bonus_point
            bonus_stone = pygame.image.load("data/tileset_2/Objects/Stones/3.png")
            bonus_stone_x = random.randint(0, 736)
            bonus_stone_y = random.randint(0, 500)
            bonus_stone_x_change = 0
            bonus_stone_y_change = 0
            if (fire_value + ship_value) > 1:
                screen.blit(bonus_stone, (bonus_stone_x, bonus_stone_y))
            '''

            # Enemy Movement
            for i in range(num_of_enemies):
                # Game Over
                if enemy_one_y[i] > 340:
                    for j in range(num_of_enemies):
                        #SOURCE OF PROBLEM
                        enemy_one_y[j] = 2000
                        game_over_text()
                        running = False
                        end = True
                        return True, str(ship_value + fire_value)



                enemy_one_x[i] += enemy_one_x_change[i]
                if enemy_one_x[i] <= 0:
                    enemy_one_x_change[i] = 4
                    enemy_one_y[i] += enemy_one_y_change[i]
                    enemy_one_img[i] = pygame.transform.flip(enemy_one_img[i], True, False)
                elif enemy_one_x[i] >= 736:
                    enemy_one_x_change[i] = -4
                    enemy_one_y[i] += enemy_one_y_change[i]
                    enemy_one_img[i] = pygame.transform.flip(enemy_one_img[i], True, False)

                # Game Over
                if enemy_two_y[i] > 340:
                    for j in range(num_of_enemies):
                        #SOURCE OF PROBLEM
                        enemy_two_y[j] = 2000
                        game_over_text()
                        running = False
                        end = True
                        return True,str(ship_value+fire_value)



                enemy_two_x[i] += enemy_two_x_change[i]
                if enemy_two_x[i] <= 0:
                    enemy_two_x_change[i] = 4
                    enemy_two_y[i] += enemy_two_y_change[i]
                    enemy_two_img[i] = pygame.transform.flip(enemy_two_img[i], True, False)
                elif enemy_two_x[i] >= 736:
                    enemy_two_x_change[i] = -4
                    enemy_two_y[i] += enemy_two_y_change[i]
                    enemy_two_img[i] = pygame.transform.flip(enemy_two_img[i], True, False)

                # Collision
                collision1 = isCollision(enemy_one_x[i], enemy_one_y[i], bulletX, bulletY)
                collision2 = isCollision(enemy_two_x[i], enemy_two_y[i], bulletX, bulletY)
                if collision1 | collision2:
                    explosionSound = mixer.Sound("data/animal_hunt_data/explosion.wav")
                    explosionSound.play()
                    bulletY = 480
                    bullet_state = "ready"
                    if collision1: fire_value += 1
                    elif collision2: ship_value+=5
                    if collision1:
                        enemy_one_x[i] = random.randint(0, 736)
                        enemy_one_y[i] = random.randint(50, 150)
                    if collision2:
                        enemy_two_x[i] = random.randint(0, 736)
                        enemy_two_y[i] = random.randint(50, 150)

                enemy(enemy_one_img,enemy_two_img,enemy_one_x[i], enemy_one_y[i], enemy_two_x[i], enemy_two_y[i], i)

            # Bullet Movement
            if bulletY <= 0:
                bulletY = 480
                bullet_state = "ready"

            if bullet_state is "fire":
                fire_bullet(bulletX, bulletY)
                bulletY -= bulletY_change

            player(playerX, playerY)
            show_score(textX, testY)
            pygame.display.update()
#main()
