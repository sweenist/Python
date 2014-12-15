import Comp_Logo
import StartMenu
import pygame
from pygame.locals import *
from sys import exit
from math import *
import Maze_1
level = Maze_1.Maze_Array()

WINSIZE = (640, 480)

screen = pygame.display.set_mode(WINSIZE, 0, 32)
background = pygame.Surface(screen.get_size())

class Pie(object):
    def __init__(self):
        self.pie_level = 1
        self.offset = (40, -210)
        self.ned_pos = (306, 222)
        self.image = pygame.image.load("NedPie.bmp")
        trans_col = self.image.get_at((0,0))
        self.image.set_colorkey(trans_col)
        self.x = 580
        self.y = -110
        self.rect = Rect(self.x, self.y, 40,40)

    def update(self):
        self.rect = Rect(self.x, self.y, 40, 40)
        
    def draw(self):
        screen.blit(self.image, (self.x, self.y))

    def levelUp(self):
        if self.rect.contains(ned.rect):
            self.pie_level=2
            self.offset = (200,-730)
            self.ned_pos = (306, 222)
            self.x = 1020
            self.y = -560
            NED_MAZE.__init__()
            ned.__init__()
            self.pie_scene()

    def pie_scene(self):
        pieback = pygame.image.load("cherry pie.jpg").convert()
        w = pieback.get_width()/2
        screen.fill((0,0,240))
        screen.blit(pieback, (320 - w,0))
        int_font = pygame.font.SysFont("trebuchetms", 48)
        message = int_font.render("Easy as Pie, right?", True, (250, 0, 25))
        smessage = int_font.render("Easy as Pie, right?", True, (0, 0, 30))
        wl = message.get_width()/2
        screen.blit(smessage, (322 - wl, 22))
        screen.blit(message, (320-wl , 20))
        pygame.display.update()
        pygame.time.wait(2500)
        do = True
        while do:
            if pygame.key.get_focused():
                do = False
        
            

class Maze_Map(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.get_images()
        self.get_map(tart.pie_level)
        self.image = self.wall_img[0]
        self.rect = self.image.get_rect()
        self.rect.center = (-40, -40)
        self.offset_x = tart.offset[0]
        self.offset_y = tart.offset[1]
        
    def update(self):
        for x in xrange(self.longitude):
            for y in xrange(self.latitude):
                screen.blit(self.wall_img[int(self.mapPlot[y][x])], (x*40+ self.offset_x, y*40 + self.offset_y))

    def get_images(self):
        self.wall_img = []
        for x in range(15):
            curr_img = pygame.image.load('mazeWall' + str(x) + '.bmp')
            self.wall_img.append(curr_img)
        for x in range(12):
            curr_img = pygame.image.load('mazeJunct' + str(x+1) + '.bmp')
            self.wall_img.append(curr_img)

    def get_map(self, arena):
        if arena == 1:
            self.mapPlot = level._1Map()
        elif arena == 2:
            self.mapPlot = level._2Map()
        self.longitude = len(self.mapPlot[0])
        self.latitude = len(self.mapPlot)


class Ned_Movement(object):
    def __init__(self):
        self.image = pygame.image.load("NedRed.bmp")
        self.rect = self.image.get_rect()
        transparent_color = self.image.get_at((0,0))
        self.image.set_colorkey(transparent_color)

        self.flip = 0
        self.pos_x = tart.ned_pos[0]
        self.pos_y = tart.ned_pos[1]
        self.rect.center = (self.pos_x +14, self.pos_y + 14)

    def update(self, x, y):
        if x == 0 and y == 0:
            return
        mag = sqrt(x**2 + y**2)
        self.flip +=1
        i_x = x / mag
        i_y = y / mag
        if pygame.key.get_mods() == 8192 or pygame.key.get_mods() == 12288:
            i_x *=4
            i_y *=4
        MOVE = NORTH = SOUTH = EAST = WEST = NORTHEAST = SOUTHEAST = NORTHWEST = SOUTHWEST = False

        if x == 1. and y == 0.:
            EAST = True
        elif x == 1. and y == 1.:
            SOUTHEAST = True
        elif x == 0. and y == 1.:
            SOUTH = True
        elif x ==-1. and y == 1.:
            SOUTHWEST = True
        elif x == -1. and y == 0.:
            WEST = True
        elif x == -1. and y == -1.:
            NORTHWEST = True
        elif x == 0. and y == -1.:
            NORTH = True
        elif x == 1. and y == -1.:
            NORTHEAST = True

#Check for walls     
        if NORTH and self.pos_y >= 160:
            rx, gx, bx, ax = screen.get_at((int(self.pos_x+14), int(self.pos_y) + 8))
            if rx > 180:
                self.pos_y += i_y
                MOVE = True
        elif SOUTH and self.pos_y <= 320:
            rx, gx, bx, ax = screen.get_at((int(self.pos_x) + 14, int(self.pos_y) + 28))
            if rx > 180:
                self.pos_y += i_y
                MOVE = True
        elif EAST and self.pos_x <= 560:
            rx, gx, bx, ax = screen.get_at((int(self.pos_x +20), int(self.pos_y)+14))
            if rx > 180:
                self.pos_x += i_x
                MOVE = True
        elif WEST and self.pos_x >=160:
            rx, gx, bx, ax = screen.get_at((int(self.pos_x) + 8 , int(self.pos_y)+14))
            if rx > 180:
                self.pos_x += i_x
                MOVE = True
        elif NORTHWEST and self.pos_y >= 160 and self.pos_x >= 160:
            rx,gx,bx,ax = screen.get_at((int(self.pos_x) + 8, int(self.pos_y) + 8))
            if rx > 180:
                self.pos_x += i_x * 2
                self.pos_y += i_y * 2
                MOVE = True
        elif NORTHEAST and self.pos_y >=160 and self.pos_x <=560:
            rx,gx,bx,ax = screen.get_at((int(self.pos_x) + 20, int(self.pos_y) +8))
            if rx > 180:
                self.pos_x += i_x * 2
                self.pos_y += i_y * 2
                MOVE = True
        elif SOUTHEAST and self.pos_y <=320 and self.pos_x <= 560:
            rx,gx,bx,ax = screen.get_at((int(self.pos_x) + 20, int(self.pos_y) +28))
            if rx > 180:
                self.pos_x += i_x * 2
                self.pos_y += i_y * 2
                MOVE = True
        elif SOUTHWEST and self.pos_y <=320 and self.pos_x >= 160:
            rx,gx,bx,ax = screen.get_at((int(self.pos_x) + 8, int(self.pos_y) + 28))
            if rx > 180:
                self.pos_x += i_x * 2
                self.pos_y += i_y * 2
                MOVE = True
        
#Check for out of Bounds and move screen and pie if it's okay
        if NORTH and self.pos_y <= 160:
           self.pos_y = 160
           rx,gx,bx,ax = screen.get_at((int(self.pos_x)+14, int(self.pos_y) + 14))
           if rx > 180:
               NED_MAZE.offset_y -= i_y
               tart.y -=i_y
               MOVE = True
        if SOUTH and self.pos_y >= 320:
            self.pos_y = 320
            rx, gx, bx, ax = screen.get_at((int(self.pos_x) + 14, int(self.pos_y) + 28))
            if rx > 180:
                NED_MAZE.offset_y -= i_y
                tart.y -= i_y
                MOVE = True
        if EAST and self.pos_x >= 560:
            self.pos_x = 560
            rx, gx, bx, ax = screen.get_at((int(self.pos_x +20), int(self.pos_y)+14))
            if rx > 180:
                NED_MAZE.offset_x -= i_x
                tart.x -= i_x
                MOVE = True
        if WEST and self.pos_x <= 160:
            self.pos_x = 160
            rx,gx,bx,ax = screen.get_at((int(self.pos_x)+14, int(self.pos_y) + 14))
            if rx > 180:
                NED_MAZE.offset_x -= i_x
                tart.x -=i_x
                MOVE = True
        if NORTHWEST and self.pos_x <=160:
            self.pos_x = 160
            rx,gx,bx,ax = screen.get_at((int(self.pos_x) + 6, int(self.pos_y) + 14))
            if rx > 180:
                NED_MAZE.offset_x -=i_x
                tart.x -=i_x
                MOVE = True
        if NORTHWEST and self.pos_y <=160:
            self.pos_y = 160
            rx,gx,bx,ax = screen.get_at((int(self.pos_x) + 6, int(self.pos_y) + 14))
            if rx > 180:
                NED_MAZE.offset_y -=i_y
                tart.y -=i_y
                MOVE = True
        if NORTHEAST and self.pos_x >=560:
            self.pos_x = 560
            rx,gx,bx,ax = screen.get_at((int(self.pos_x) + 20, int(self.pos_y) +14))
            if rx > 180:
                NED_MAZE.offset_x -=i_x
                tart.x -=i_x
                MOVE = True
        if NORTHEAST and self.pos_y <=160:
            self.pos_y = 160
            rx,gx,bx,ax = screen.get_at((int(self.pos_x) + 20, int(self.pos_y) +14))
            if rx > 180:
                NED_MAZE.offset_y -=i_y
                tart.y -=i_y
                MOVE = True

        if SOUTHEAST and self.pos_x >= 560:
            self.pos_x = 560
            rx,gx,bx,ax = screen.get_at((int(self.pos_x) + 20, int(self.pos_y) +28))
            if rx > 180:
                NED_MAZE.offset_x -= i_x
                tart.x -= i_x
                MOVE = True
        if SOUTHEAST and self.pos_y >=320:
            self.pos_y = 320
            rx,gx,bx,ax = screen.get_at((int(self.pos_x) + 20, int(self.pos_y) +28))
            if rx > 180:
                NED_MAZE.offset_y -= i_y
                tart.y -= i_y
                MOVE = True
        if SOUTHWEST and self.pos_x <= 160:
            self.pos_x = 160
            rx,gx,bx,ax = screen.get_at((int(self.pos_x) + 6, int(self.pos_y) + 28))
            if rx > 180:
                NED_MAZE.offset_x -=i_x
                tart.x -=i_x
                MOVE = True
        if SOUTHWEST and self.pos_y >= 320:
            self.pos_y = 320
            rx,gx,bx,ax = screen.get_at((int(self.pos_x) + 6, int(self.pos_y) + 28))
            if rx > 180:
                NED_MAZE.offset_y -=i_y
                tart.y -=i_y
                MOVE = True
        if not MOVE:
            #print "Ned hits wall"
            pass
        tart.update()

    def draw(self):
        self.rect = Rect(self.pos_x, self.pos_y, 28, 28)
        if self.flip == 5:
            self.image = pygame.transform.flip(self.image, 1, 0)
        screen.blit(self.image, (self.pos_x, self.pos_y))
        if self.flip == 5:
            self.flip = 0
        
Comp_Logo.run()
StartMenu.play()
tart = Pie()    
NED_MAZE = Maze_Map()
ned = Ned_Movement()

pygame.display.set_caption("Level "+str(tart.pie_level), "   (ESC)to quit")

screen.fill((250, 250, 250))
bkg_spr = pygame.sprite.Group(NED_MAZE)
clock = pygame.time.Clock()
pygame.mouse.set_visible(False)

while True:
    for e in pygame.event.get():
        if e.type == QUIT:
            pygame.mouse.set_visible(True)
            pygame.quit()
            exit(0)
        if e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                pygame.mouse.set_visible(True)
                pygame.quit()
                exit(0)
            elif e.key == K_s:
                pygame.image.save(screen, "MazeSample.bmp")
            elif e.key == K_p:
                print ned.pos_x, ned.pos_y, tart.x, tart.y
                print
                print ned.rect, tart.rect

    time_pass = clock.tick(30)
    time_pass_secs = time_pass / 1000
    
    screen.blit(background, (0,0))
    bkg_spr.update()
    bkg_spr.draw(screen)
    tart.draw()

    kp = pygame.key.get_pressed()
    nx, ny = 0, 0
    if kp[K_UP]:
        ny = -1
    elif kp[K_DOWN]:
        ny = +1
    if kp[K_RIGHT]:
        nx = +1
    elif kp[K_LEFT]:
        nx = -1
    ned.update(nx, ny)

    ned.draw()
    pygame.display.update()
    tart.levelUp()

