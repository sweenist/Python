"""
This new attempt will use prewritten classes from other im.py files
WHAT'S NEW:
    -A class which retrieves level information. This will be used to load
    saved games in the near future. Right now it just loads the first level
    parameters for background and npcs
"""
import pygame
from pygame.locals import *
from pygame.color import THECOLORS as C
import os, sys

pygame.font.init()

level_schemes = {'Blue': ["MazeBlock1.gif", "MazeFloor1.gif"],
                'Green': ["MazeBlock2.gif", "MazeFloor2.gif"],
                'Red': ["MazeBlock3.gif", "MazeFloor3.gif"],
                'Purple': ["MazeBlock4.gif", "MazeFloor4.gif"],
                'Yellow': ["MazeBlock5.gif", "MazeFloor5.gif"],
                'Grey': ["MazeBlock6.gif", "MazeFloor6.gif"],
                }
#################################################################
#          Information loading via Class instance               #
#################################################################
class Level():
    def __init__(self, lev = 1):
        self.lev = str(lev)
        self.mapfile = "00"+self.lev+".map"
        self.maplist = []
        self.npcfile = "00"+self.lev+".npc"
        self.npclist = []

    def load(self):
#########################get map info
        mf = open(self.mapfile) 
        mapx, mapy, scheme = mf.readline().split(',')
        mapx, mapy = int(mapx), int(mapy)
        scheme = scheme.strip().capitalize()
        for line in mf:
            array = line.strip('\n')
            self.maplist.append(array.split(','))
        mf.close()
        
        for i in range(mapy):       #turn strings in array to int
            for j in range(mapx):
                self.maplist[i][j] = int(self.maplist[i][j])
        self.mapX = mapx
        self.mapY = mapy
        self.scheme = scheme

##########################get npc info
        nf = open(self.npcfile) 
        for line in nf:
            x, y, d, w, s = line.split(',')
            d = d.strip()
            x, y, w, s = int(x), int (y), int(w), int(s)
            self.npclist.append((x, y, d, w, s))
        nf.close

level = Level()
level.load()    #Create an instance of Level class
background = pygame.Surface((level.mapX*40, level.mapY*40))

#################### END INFORMATION RETREIVAL ##################

#################################################################
#                  Background Classes                           #
#################################################################

class Field(object):
    def __init__(self, sx = 0, sy = 0):
        # variables from Level instance
        self.x = level.mapX
        self.y = level.mapY
        self.X = self.x * 40
        self.Y = self.y * 40
        self.array = level.maplist
        #self.scheme = level.scheme
        level.scheme = 'Purple'

        #screen positioning
        self.sx = sx
        self.sy = sy
        sw, sh = screen.get_size()
        bw, bh = background.get_size()
        self.max_x, self.max_y = sw-bw, sh - bh - 40

        # other variables and dictionaries
        self.move = False

        # preparing for Wall and Floor sprites
        self.walls = []
        self.floors = []
        self.draw()

        #Now add an offset to all rect parameters
        for f in self.floorGroup:
            f.rect.x += self.sx
            f.rect.y += self.sy
        for w in self.wallGroup:
            w.rect.x += self.sx
            w.rect.y += self.sy

    def update(self, x=0, y=0):
        if x or y:
            for f in self.floorGroup:
                f.rect.x += x
                f.rect.y += y
            for w in self.wallGroup:
                w.rect.x += x
                w.rect.y += y

    def draw(self):
        for i in xrange(self.y):
            for j in xrange(self.x):
                if self.array[i][j] == 0:
                    self.floors.append(Floor(j*40, i*40))
                elif self.array[i][j] == 1:
                    self.walls.append(Block(j*40, i*40))

        self.wallGroup = pygame.sprite.Group(self.walls)
        self.floorGroup = pygame.sprite.Group(self.floors)
        
class Block(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(level_schemes[level.scheme][0])
        self.rect = Rect(x, y, self.image.get_width(), self.image.get_height())
        background.blit(self.image, (x, y))
        
class Floor(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(level_schemes[level.scheme][1])
        self.rect = Rect(x, y, self.image.get_width(), self.image.get_height())
        background.blit(self.image, (x, y))

class StatusBar(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.x = 0
        self.y = screen.get_height() - 40
        self.w = screen.get_width()
        self.h = 40
        self.rect = Rect(self.x, self.y, self.w, self.h)
        self.image = pygame.Surface((self.w, self.h))
        self.image.fill(C['aliceblue'])
        pygame.draw.rect(self.image, C['black'], (0,0, self.w, self.h), 1)

    def update(self):
        pygame.draw.rect(self.image, C['aliceblue'], (0,0, self.w, self.h))
        pygame.draw.rect(self.image, C['black'], (0,0, self.w, self.h), 3)

class Label(pygame.sprite.Sprite):
    def __init__(self, message = ""):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.SysFont('trebuchetms', 16)
        self.center_x = screen.get_width()/2
        self.message = message

    def update(self):
        self.image = self.font.render(self.message, 1, C['black'])
        self.rect = self.image.get_rect()
        self.rect.centerx = self.center_x
        self.rect.y = 440
        
        
#################################################################
#                        Player Class                           #
#################################################################

class Player(pygame.sprite.Sprite):
    def __init__(self, x=None, y=None, max_index = 2):
        pygame.sprite.Sprite.__init__(self)
        self.norm_x = screen.get_width()/2 + 5
        self.norm_y = screen.get_height()/2 - 40
        if x:
            self.x = x
        else:
            self.x = self.norm_x
        if y:
            self.y = y
        else:
            self.y = self.norm_y
        
        self.images=[]
        for i in range(max_index):
            image = pygame.image.load('ned'+str(i)+'.gif')
            t = image.get_at((0,0))
            image.set_colorkey(t)
            self.images.append(image)

        self.index = 0
        self.max_index = max_index

        self.delay = 0
        self.delay_max = 3
        
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.inflate_ip(-2, -2)
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.delay +=1
        if self.delay == self.delay_max:
            self.delay = 0
            self.index += 1
            if self.index == self.max_index:
                self.index = 0
            self.image = self.images[self.index]

#################################################################
#                       Enemy Classes                           #
#################################################################

class SpikeBall(pygame.sprite.Sprite):
    def __init__(self, x, y, dr = 'west', time_max = 1, spd = 3):
        pygame.sprite.Sprite.__init__(self)
    #image setup
        self.index = 0
        self.images = []
        for i in range(2):
            image = pygame.image.load('npc_spike'+ str(i) + '.gif')
            t_color = image.get_at((0,0))
            image.set_colorkey(t_color)
            self.images.append(image)
        self.image = self.images[self.index]
    #dimensional variables
        self.x = x
        self.y = y
        self.rect = Rect(self.x, self.y, 36, 36)
        self.time = 0
        self.S = spd
        self.time_max = time_max
        self.delay = 1
        self.delay_max = 2
        self.dir = dr.lower().strip()
        self.D = {'north':(0,-self.S), 'east':(self.S,0), 'south':(0,self.S), 'west': (-self.S,0)}

    def update(self):
        if bkg.move: increment = 0
        elif not bkg.move: increment = 1
        self.delay += increment
        if self.delay == self.delay_max:    #time between image change
            self.index += 1
            if self.index == 2:  #reset image index to 0 if maxvalue
                self.index = 0
            self.image = self.images[self.index]
            self.delay = 0
        self.time += increment
        if self.time == self.time_max: # Positional move in time
            self.time = 0
            self.x += self.D[self.dir][0]
            self.y += self.D[self.dir][1]
            self.rect = Rect(self.x, self.y, 36, 36)
            self.rect.inflate_ip(-3, -3)            
            self.collide()

    def collide(self):
        if pygame.sprite.spritecollide(self, bkg.wallGroup, False):
            oppList = ['north', 'south', 'east', 'west']
            a = oppList.index(self.dir)
            if a%2 == 0:
                self.dir = oppList[a+1]
            elif a%2 == 1:
                self.dir = oppList[a-1]
#        self.x += self.D[self.dir][0]
#        self.y += self.D[self.dir][1]
#        self.rect = Rect(self.x, self.y, 36, 36)
#        self.rect.inflate_ip(-3, -3)

################ Get the Enemies from presets ###################

def enemyGrab():
    eList = []
    for l in level.npclist:
        eList.append(SpikeBall(*l))
    return eList

####################### Movement from keys ######################
            
def movement(k):
    vkey, hkey = vned, hned = None, None
    screen_move = False
    play_move = False
    collide = False
            
    if k[273]: vkey = vned= 'up'
    elif k[274]: vkey = vned = 'down'
    if k[275]: hkey = hned = 'right'
    elif k[276]: hkey = hned = 'left'
    ##check for endpoints
    if vkey == 'up':        #vertical checking
        if bkg.sy < 0 and ned.rect.y == ned.norm_y:
            screen_move = True
        else:
            vkey = None
    elif vkey == 'down':
        if bkg.sy > bkg.max_y and ned.rect.y == ned.norm_y:
            screen_move = True
        else:
            vkey = None
            
    if hkey == 'right':     #horizontal checking
        if bkg.sx > bkg.max_x and ned.rect.x == ned.norm_x:
            screen_move = True
        else:
            hkey = None
    elif hkey == 'left':
        if bkg.sx < 0 and ned.rect.x == ned.norm_x:
            screen_move = True
        else:
            hkey = None            
            
    if screen_move:
        move_screen(hkey, vkey)
    elif not screen_move: # and (ned.x != ned.norm_x or ned.y != ned.norm_y):
        move_ned(hned, vned)

            
def move_screen(hkey = None, vkey = None):
    move_dict = {None: 0, 'up': 5, 'down': -5, 'right': -5, 'left': 5}
    hmove = vmove = False
    if hkey:
        hmove = True
        bkg.sx += move_dict[hkey]       #screen x
        bkg.update(move_dict[hkey])     #background rects
        if pygame.sprite.spritecollide(ned, bkg.wallGroup, False):
            hmove = False
            bkg.sx -= move_dict[hkey]   #restore original screen x
            bkg.update(-move_dict[hkey])#restore former background rects
            
    if vkey:
        vmove = True
        bkg.sy += move_dict[vkey]
        bkg.update(y = move_dict[vkey])
        if pygame.sprite.spritecollide(ned, bkg.wallGroup, False):
            vmove = False
            bkg.sy -= move_dict[vkey]
            bkg.update(y = -move_dict[vkey])

    if hmove or vmove:
        for e in badsprites:
            if hmove:
                e.x += move_dict[hkey]
            if vmove:
                e.y += move_dict[vkey]
                
def move_ned(hkey = None, vkey = None):
    move_dict = {None: 0, 'up': -5, 'down': 5, 'right': 5, 'left': -5}
    if hkey:
        ned.rect.x += move_dict[hkey]
        if pygame.sprite.spritecollide(ned, bkg.wallGroup, False):
            ned.rect.x -= move_dict[hkey]
    if vkey:
        ned.rect.y += move_dict[vkey]
        if pygame.sprite.spritecollide(ned, bkg.wallGroup, False):
            ned.rect.y -= move_dict[vkey]

###################### Main Game Play ###########################
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Another Game Test")

bkg = Field()
ned = Player()  #save player class

bar = StatusBar()
label = Label("Maze Game")

allsprites = pygame.sprite.Group(ned, bar, label)
badsprites = pygame.sprite.Group(enemyGrab())

if __name__ == "__main__":
    clk = pygame.time.Clock()
    game_over = False
    do = True
    while do:
        clk.tick(30)
        for e in pygame.event.get():
            if e.type == 2:
                if e.key == 27:
                    do = not do
            if e.type == 12:
                do = not do

        k = pygame.key.get_pressed()

        if 1 in k:
            movement(k)
            
        badsprites.update()
        allsprites.update()

        screen.blit(background, (bkg.sx, bkg.sy))

        badsprites.draw(screen)
        allsprites.draw(screen)
        
        pygame.display.flip()
        if pygame.sprite.spritecollide(ned, badsprites, True):
            game_over = True
            do = False

########################## END MAIN #############################
if game_over:
    screen.blit(background, (bkg.sx, bkg.sy))
    label.message = "Game Over..."
    allsprites.update()
    allsprites.draw(screen)
    pygame.display.flip()
    pygame.time.wait(2000)
    
pygame.display.quit()
