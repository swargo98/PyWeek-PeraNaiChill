import pygame, os

from gamelib.Design import design

pygame.init()

# size of the game window
win_width, win_height = 800, 480

# Font for game over window
FONT = "freesandsbold.ttf"

# win_size = (win_width, win_height)
win_size = win_width, win_height

window = pygame.display.set_mode(win_size)
fade = pygame.Surface((win_width, win_height))
fade.fill((0,0,0))


# set_caption(title, icontitle=None) -> None
#If the display has a window title, this function will change the name on the window
pygame.display.set_caption("Pera Nai Chill")

# create an object to help track time
clock = pygame.time.Clock()

fps = 30


def loadImageListInDict(path):
    listsDict = {}
    for folder in os.listdir(path):
        subPath = os.path.join(path, folder)
        if os.path.isdir(subPath):
            listsDict[folder] = []
            for image in os.listdir(subPath):
                if os.path.isfile(os.path.join(subPath, image)):
                    listsDict[folder].append(pygame.image.load(os.path.join(subPath, image)).convert_alpha())

    return listsDict

def loadImageInList(path):
    # Load all the files(only images) under the directory into a list and return.
    imageList = []
    for image in os.listdir(path):
        subPath = os.path.join(path, image)
        if os.path.isfile(subPath):
            imageList.append(pygame.image.load(subPath).convert_alpha())
    return imageList


class Player(pygame.sprite.Sprite):

    def __init__(self , imageLists = {} , width = 64, height = 64):
        super().__init__()

        #set start image of player
        self.image= imageLists['Left'][0]
        #self.image = pygame.transform.scale(IMAGE, (32, 32))

        # fetch rectangle object that has dimension of the image
        self.rect = self.image.get_rect()

        self.hSpeed = 0
        self.vSpeed = 0
        self.speed = 8
        self.imageLists = imageLists
        self.direction = 'L'
        self.walkCount = 0
        self.abs_x = 0
        self.abs_y = 0
        self.treasureCount = 0
        self.winGame = False
        self.side = 'L'

    def set_position(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def set_absolute_position(self, x, y):
        self.abs_x = x
        self.abs_y = y

    # update function, every loop this function will be called
    def update(self,event, collidable=pygame.sprite.Group(), treasures = pygame.sprite.Group() , waterfall = pygame.sprite.Group()):
        side = self.move(event,collidable)
        self.isCollided_with_treasures(treasures)
        self.winGame = self.isCollided_with_waterfall(waterfall)

        # Implement animation
        self.walkAnimation(side)


    def move(self,event, collidable):
        # get key pressed by user
        keys = pygame.key.get_pressed()

        # If any direction key is pressed
        if (keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_UP] or keys[pygame.K_DOWN]):

            # account for horizontal movement if pressed left key
            if (keys[pygame.K_LEFT]):
                # left = negative speed, right = positive speed
                self.hSpeed = -self.speed

            elif (keys[pygame.K_RIGHT]):
                # self.image = spriteLists[]
                self.hSpeed = self.speed

            else:
                self.hSpeed = 0

            # account for vertical movement
            if (keys[pygame.K_UP]):
                self.vSpeed = -self.speed

            elif (keys[pygame.K_DOWN]):
                self.vSpeed = self.speed

            else:
                self.vSpeed = 0

            # Redefine direction
            if self.hSpeed > 0:
                self.direction = 'R'
            elif self.hSpeed < 0:
                self.direction = 'L'
            elif self.vSpeed > 0:
                self.direction = 'D'
            elif self.vSpeed < 0:
                self.direction = 'U'

            # If all direction keys are not pressed
        else:
            self.hSpeed = 0
            self.vSpeed = 0
            self.direction = 'N'

        last_side = self.side
        if self.direction == 'L' or self.direction == 'R':
            self.side = self.direction

        # after determining the direction of player, check if there is any collision
        self.isCollided(collidable)
        return last_side


    def walkAnimation(self, side):

        self.walkCount += 1
        if self.walkCount >= 30 :
            self.walkCount = 0


        if self.direction == 'L':
            self.image = self.imageLists['Left'][self.walkCount // 3]
        elif self.direction == 'R':
            self.image = self.imageLists['Right'][self.walkCount // 3]
        elif self.direction == 'U' or self.direction == 'D':
            if side == 'L':
                self.image = self.imageLists['UpLeft'][self.walkCount // 3]
            else:
                self.image = self.imageLists['UpRight'][self.walkCount // 3]
        elif self.direction == 'N':
            if side == 'L':
                self.image = self.imageLists['Idle'][0]
            else:
                self.image = self.imageLists['Idle'][1]






    def isCollided(self, collidable):
        # Find sprites in a group that intersect another sprite.
        # spritecollide(sprite, group, dokill, collided = None)
        # Intersection is determined by comparing the Sprite.rect attribute of each Sprite

        self.rect.x += self.hSpeed
        self.abs_x += self.hSpeed

        # Find sprites in a group that intersect another sprite.
        # spritecollide(sprite, group, dokill, collided = None)
        # Intersection is determined by comparing the Sprite.rect attribute of each Sprite
        collision_list = pygame.sprite.spritecollide(self, collidable, False)

        # if intersection with collidable object in collision_list ( horizontal x direction )
        for collided_object in collision_list:
            # if (self.rect.bottom <= collided_object.rect.top or self.rect.top >= collided_object.rect.bottom):
            if (self.hSpeed > 0):
                # Update Absoulte position
                hDiff = collided_object.rect.left - self.rect.right
                self.abs_x += hDiff
                # Update relative position
                self.rect.right = collided_object.rect.left
                self.hSpeed = 0

            elif (self.hSpeed < 0):
                # Update Absoulte position
                hDiff = collided_object.rect.right - self.rect.left
                self.abs_x += hDiff
                # Update relative position
                self.rect.left = collided_object.rect.right
                self.hSpeed = 0

        self.rect.y += self.vSpeed
        self.abs_y += self.vSpeed
        # if intersection with collidable object in y direction
        collision_list = pygame.sprite.spritecollide(self, collidable, False)
        for collided_object in collision_list:
            # Moving down
            if (self.vSpeed > 0):
                # Update Absoulte position
                vDiff = collided_object.rect.top - self.rect.bottom
                self.abs_y += vDiff

                # Update relative position
                self.rect.bottom = collided_object.rect.top
                self.vSpeed = 0
            # Moving up
            elif (self.vSpeed < 0):
                # Update Absoulte position
                vDiff = collided_object.rect.bottom - self.rect.top
                self.abs_y += vDiff

                # Update relative position
                self.rect.top = collided_object.rect.bottom
                self.vSpeed = 0

    def isCollided_with_treasures(self, treasures):
        if (pygame.sprite.spritecollide(self, treasures, True)):
            treasure_sound.play()
            self.treasureCount += 1

    def isCollided_with_waterfall(self, waterfall):
        collision_list = pygame.sprite.spritecollide(self, waterfall, False)
        for spring in collision_list:
            if (self.rect.collidepoint(spring.rect.centerx, spring.rect.centery)):
                return True



class Wall(pygame.sprite.Sprite):

    def __init__(self,type, x, y, width=64, height=64):

        super().__init__()
        self.image = None
        if type == 'G':
            self.image = pygame.image.load('data/Image/Walls/g.png').convert_alpha()
        else:
            self.image = pygame.image.load('data/Image/Walls/5.png').convert_alpha()

        # self.image = pygame.Surface((width, height))
        # self.image.fill((255,100,180))

        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

    def shift_world(self, shift_x, shift_y):
        self.rect.x += shift_x
        self.rect.y += shift_y


    def draw(self, window):
        window.blit(self.image, (self.rect.x, self.rect.y))



class Treasure(pygame.sprite.Sprite):

    def __init__(self, x, y, width = 64, height = 64):

        super().__init__()
        self.image = pygame.image.load('data/Image/treasure.png').convert_alpha()

        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

    def shift_world(self, shift_x, shift_y):
        self.rect.x += shift_x
        self.rect.y += shift_y


class WaterFall(pygame.sprite.Sprite):

    def __init__(self, x, y, imageList = None, width = 64, height = 64):

        super().__init__()
        self.image = pygame.image.load('data/Image/Waterfall/rsz_w1001.png').convert_alpha()
        self.imageList = imageList
        self.image = imageList[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.count = 0

    def update(self):
        self.animation()

    def animation(self):
        self.count += 1
        if self.count >= 16:
            self.count = 0

        self.image = self.imageList[self.count // 2]

    def shift_world(self, shift_x, shift_y):
        self.rect.x += shift_x
        self.rect.y += shift_y

class MiniMap(object):
    def __init__(self, win_width, win_height):
        super().__init__()

        self.width, self.height = 190, 190

        self.image = pygame.image.load('data/Image/frame.png').convert_alpha()
        self.rect = self.image.get_rect()

        self.bg = pygame.Surface((self.width - 20, self.height - 20))
        self.bg.fill((0,0,0))
        self.bg1 = pygame.Surface((160, 160))
        self.bg1.fill((0,0,0))

        self.rect.x = win_width - self.width
        self.rect.y = win_height - self.height

    def draw(self, window):
        window.blit(self.bg,(self.rect.x + 10, self.rect.y + 10))
        window.blit(self.image,(self.rect.x, self.rect.y))
        window.blit(self.bg1,(self.rect.x + 15, self.rect.y + 15))

class MiniWall(pygame.sprite.Sprite):
    def __init__(self, x, y):

        super().__init__()

        self.image = pygame.image.load('data/Image/miniWall.png').convert_alpha()

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class MiniPlayer (object):
    def __init__(self, player_abs_x = 0, player_abs_y = 0, win_width = 800, win_height = 480):

        super().__init__()

        self.image = pygame.image.load('data/Image/miniPlayer.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.win_width = win_width
        self.win_height = win_height

    def update(self, player_abs_x, player_abs_y):
        mini_x = 150 / (64 * 50) * player_abs_x
        mini_y = 150 / (64 * 50) * player_abs_y

        self.rect.x = self.win_width - 170 + mini_x
        self.rect.y = self.win_height - 170 + mini_y

    def draw(self, window):
        window.blit(self.image, (self.rect.x - 5, self.rect.y - 5))



def run_viewbox(player_x, player_y):
    # global player, walls_Group, enemies_Group, treasures_group, portal_group, spikes_group, traps_group

    left_viewbox = win_width/2 - win_width/8
    right_viewbox = win_width/2 + win_width/8
    top_viewbox = win_height/2 - win_height/8
    bottom_viewbox = win_height/2 + win_height/8
    dx, dy = 0, 0

    if(player_x <= left_viewbox):
        dx = left_viewbox - player_x
        player.set_position(left_viewbox, player.rect.y)

    elif(player_x >= right_viewbox):
        dx = right_viewbox - player_x
        player.set_position(right_viewbox, player.rect.y)

    if(player_y <= top_viewbox):
        dy = top_viewbox - player_y
        player.set_position(player.rect.x, top_viewbox)

    elif(player_y >= bottom_viewbox):
        dy = bottom_viewbox - player_y
        player.set_position(player.rect.x, bottom_viewbox)

    if (dx != 0 or dy != 0):
        for wall in walls_group:
            wall.shift_world(dx, dy)

        for treasure in treasures_group:
            treasure.shift_world(dx, dy)

        for waterfall in waterfall_group:
            waterfall.shift_world(dx, dy)







def createInstances():
    global player, player_group, walls_group, miniMap, miniPlayer, miniWalls_group, treasures_group, waterfall_group
    global win_width, win_height

    player = Player(imageLists = playerImageLists)
    player_group = pygame.sprite.Group()
    player_group.add(player)

    walls_group = pygame.sprite.Group()
    miniMap = MiniMap(win_width, win_height)
    miniPlayer = MiniPlayer(win_width, win_height)
    miniWalls_group = pygame.sprite.Group()
    treasures_group = pygame.sprite.Group()
    waterfall_group = pygame.sprite.Group()


def setup_maze():

    for y in range(len(design)):
        for x in range(len(design[y])):
            character = design[y][x]
            pos_x = (x*64)
            pos_y = (y*64)

            if character == "X" or character == "G":
                #Update wall coordinates
                walls_group.add(Wall(character,pos_x, pos_y))
                miniWalls_group.add(MiniWall(win_width - 170 + (x * 3), win_height - 170 + (y * 3)))


            elif character == "P":
                player.set_position(pos_x, pos_y)
                player.set_absolute_position(pos_x, pos_y)
                miniPlayer.update(pos_x, pos_y)

            elif character == "T":
                # Update treasure coordinates
                treasures_group.add(Treasure(pos_x, pos_y))

            elif character == "U":
                # Update waterfall coordinates
                waterfall_group.add(WaterFall(pos_x, pos_y, waterfallList))


# Empty the maze
def clear_maze():
    walls_group.empty()
    treasures_group.empty()
    waterfall_group.empty()
    miniWalls_group.empty()
    player_group.empty()

    player.winGame = False





playerImageLists = loadImageListInDict('data/Image/Player')
waterfallList = loadImageInList('data/Image/Waterfall')
# Load font
font1 = pygame.font.SysFont('Calibri',24,True,True)
player_image = pygame.image.load('data/Image/player.png').convert_alpha()
bg = pygame.image.load('data/Image/BG.png').convert_alpha()

treasure_sound = pygame.mixer.Sound(os.path.join('data/audios','treasure_sound.wav'))

def main():
    start = True
    isGameOver = False
    running = True
    end = False

    # fading
    i = 0
    window.fill((255, 255, 255))

    while running:
        for event in pygame.event.get():
            if (event.type == pygame.QUIT) or \
                    (event.type == pygame.KEYDOWN \
                     and (event.key == pygame.K_ESCAPE or event.key == pygame.K_q)):
                running = False

        if end == True :
            return True

        if start == True:
            createInstances()
            setup_maze()
            breakLoop = True
            while breakLoop:
                window.blit(bg, (0, 0))
                window.blit(player_image, (50, 150))
                Text = font1.render('Level 3 ', 1, (0, 0, 0))
                StartText = font1.render('Press any key to start ', 1, (0, 0, 0))
                Instructions1 = font1.render('Find the waterfall to pass the level ', 1, (0, 0, 0))
                Instructions2 = font1.render('There are 10 treasures along the way. Find all of them ', 1, (0, 0, 0))
                Instructions3 = font1.render('Press key UP, DOWN, LEFT, RIGHT to move', 1, (0, 0, 0))
                window.blit(Text, (450, 50))
                window.blit(StartText, (380, 100))
                window.blit(Instructions1, (250, 200))
                window.blit(Instructions2, (220, 250))
                window.blit(Instructions3, (240, 300))
                pygame.display.flip()
                for event in pygame.event.get():
                    if (event.type == pygame.QUIT) or \
                            (event.type == pygame.KEYDOWN \
                             and (event.key == pygame.K_ESCAPE or event.key == pygame.K_q)):
                        running = False
                        start = False
                        breakLoop = False
                    if (event.type == pygame.KEYDOWN):
                        start = False
                        breakLoop = False







        elif isGameOver == True :
            breakLoop = True
            Fail = False
            if player.treasureCount < 10 :
                Fail = True
            while breakLoop:
                window.blit(bg, (0, 0))
                window.blit(player_image, (50, 150))
                Text = font1.render('Level 3 Passed, YOU WIN!!!', 1, (0, 0, 0))
                Point= font1.render('Treasures : ' + str(player.treasureCount), 1, (0, 0, 0))
                Retry = font1.render('Press P to Play Again', 1, (0, 0, 0))
                Quit = font1.render('Press Q to Quit', 1, (0, 0, 0))
                NextLevel = font1.render('Press A to go to next Level', 1, (0, 0, 0))
                Menu = font1.render('Press M to go to Main Menu', 1, (0, 0, 0))
                window.blit(Point, (300, 120))
                if Fail == False:
                    window.blit(Text, (250, 200))
                    window.blit(NextLevel,(200,250))
                else:
                    window.blit(font1.render('You have not found all treasures!!', 1, (0, 0, 0)), (220,200))
                window.blit(Retry, (300, 350))
                window.blit(Quit, (300, 400))
                window.blit(Menu,(300,450))
                clear_maze()
                for event in pygame.event.get():
                    if (event.type == pygame.QUIT) or \
                            (event.type == pygame.KEYDOWN \
                             and (event.key == pygame.K_ESCAPE or event.key == pygame.K_q)):
                        running = False
                        isGameOver = False
                        breakLoop = False

                    if (event.type == pygame.KEYDOWN):
                        key_name = pygame.key.name(event.key)
                        if key_name == 'p':
                            isGameOver = False
                            start = True
                            breakLoop = False
                        elif key_name == 'a':
                            running = False
                            isGameOver = False
                            breakLoop = False
                            end = True
                        elif key_name == 'm':
                            isGameOver = False
                            breakLoop = False
                            end = True



                pygame.display.flip()


        else:
            player_group.update(event,walls_group, treasures_group, waterfall_group)

            # from player group update -> check if collide with portal to advance to next stage

            waterfall_group.update()
            miniPlayer.update(player.abs_x, player.abs_y)

            # Fill background with black color
            window.fill((255,255,255))


            # Update view camera
            run_viewbox(player.rect.x, player.rect.y)


            for wall in walls_group:
                if (wall.rect.x < win_width) and (wall.rect.y < win_height):
                    wall.draw(window)



            player_group.draw(window)
            treasures_group.draw(window)
            waterfall_group.draw(window)
            miniMap.draw(window)
            miniWalls_group.draw(window)
            miniPlayer.draw(window)

            scoreText = font1.render('Treasures : ' + str(player.treasureCount), 1, (0 , 0, 0))
            window.blit(scoreText, (10, 10))

            if player.winGame == True :
                isGameOver = True


        # Delay & Update Screen
        pygame.display.flip()
        clock.tick_busy_loop(fps)

    pygame.quit()

#main()