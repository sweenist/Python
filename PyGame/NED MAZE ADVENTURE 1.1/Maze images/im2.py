import os, sys
import pygame
from pygame.locals import *
from pygame.color import THECOLORS as C
import random
pygame.font.init()

board_file_D = {'Blue': ["MazeBlock1.gif", "MazeFloor1.gif"],
                'Green': ["MazeBlock2.gif", "MazeFloor2.gif"],
                'Red': ["MazeBlock3.gif", "MazeFloor3.gif"],
                'Purple': ["MazeBlock4.gif", "MazeFloor4.gif"],
                'Yellow': ["MazeBlock5.gif", "MazeFloor5.gif"],
                'Grey': ["MazeBlock6.gif", "MazeFloor6.gif"],
                }
class Level():
    def __init__(self, lev = 1):
        self.lev = str(lev)
        self.mapfile = "00"+self.lev+".map"
        self.maplist = []
        self.npcfile = "00"+self.lev+".npc"
        self.npclist = []

    def load(self):
        mf = open(self.mapfile)
        mapx, mapy = mf.readline().split(',')
        mapx, mapy = int(mapx), int(mapy)
        for line in mf:
            array = line.strip('\n')
            self.maplist.append(array.split(','))
        mf.close()
        for i in range(mapy):
            for j in range(mapx):
                self.maplist[i][j] = int(self.maplist[i][j])
        self.mapX = mapx
        self.mapY = mapy

        nf = open(self.npcfile)
        for line in nf:
            x, y, d, w, s = line.split(',')
            x, y, w, s = int(x), int (y), int(w), int(s)
            self.npclist.append(x, y, d, w, s)
        nf.close

level = Level()
level.load()

        
######################################################
#   Background drawing and setup                     #
######################################################
class Field(object):
    def __init__(self):
        #pointers
        self.index = 0
        self.move = False
        self.move_D = {'none':(0,0), 'up':(0,20), 'down': (0,-20),
                       'right': (-20,0), 'left':(20,0)
                       }
        #dimensional variables
        self.x, self.y, self.array = get_maze()
        self.pos_xy = [0,0]
        self.dx, self.dy = 0, 0
        #image setup
        ##########update to accomodate separate background sprites
        self.walls = []
        self.floors = []
        self.get_blocks()
        
        self.draw()
        self.rect = ((self.dx, self.dy), background.get_size())
        self.corner_x = self.rect[1][0]
        self.corner_y = self.rect[1][1]
        self.max_x = screen.get_width() - self.corner_x
        self.max_y = screen.get_height() - self.corner_y - 40
        self.stat = StatusBar()

    def get_blocks(self):
        for i in range(self.y):
            for j in range(self.x):
                if self.array[i][j] == 0:
                    fl = Floor(j*40 + self.dx, i*40 + self.dy)
                    self.floors.append(fl)
                elif self.array[i][j] == 1:
                    w = Block(j*40 + self.dx, i*40 + self.dy)
                    self.walls.append(w)
        self.wallGroup = pygame.sprite.Group(self.walls)
        self.floorGroup= pygame.sprite.Group(self.floors)
                        
    
    def update(self, key = 'none'):
        self.key = key
        if self.key != 'none': self.move = True
        #check both x and y components of screen movement
        if self.pos_xy[0] <= 0 and self.pos_xy[0] >= self.max_x:
            self.pos_xy[0] += self.move_D[self.key][0]
            if self.pos_xy[0] > 0:
                self.pos_xy[0] = 0
                self.move = False
            if self.pos_xy[0] < self.max_x:
                self.pos_xy[0] = self.max_x
                self.move = False
        if self.pos_xy[1] <= 0 and self.pos_xy[1] >= self.max_y:
            self.pos_xy[1] += self.move_D[self.key][1]
            if self.pos_xy[1] > 0:
                self.pos_xy[1] = 0
                self.move = False
            if self.pos_xy[1] < self.max_y:
                self.pos_xy[1] = self.max_y
                self.move = False
        if self.move:   #update the list of background rectangles
            self.dx, self.dy = self.move_D[self.key][0], self.move_D[self.key][1]
            self.floorGroup.update()
            self.wallGroup.update()
            print self.pos_xy, self.dx, self.dy, "\n"

        self.draw()                
        #Call other background drawings
        enemies.update()
        ned.update()
        self.stat.update()
        self._show()
        self.move = False

    def draw(self):
        self.floorGroup.draw(background)
        self.wallGroup.draw(background)
        self._show()

    def _show(self):
        font = pygame.font.SysFont('arial', 16)
        show = font.render(str(self.pos_xy), True, C['black'])
        
        background.blit(show, (20, (screen.get_height()-20)))
        
class StatusBar(object):
    def __init__(self):
        self.rect = ((0,screen.get_height()-40),(screen.get_size()))
        self.surface = pygame.Surface((screen.get_width(), 40))
        self.surface.fill(C['white'])
        pygame.draw.rect(self.surface, C['black'], (1, screen.get_height()-39, screen.get_width(), 38), 1)
        self.update()

    def update(self):
        background.blit(self.surface, self.rect[0:1])

class Block(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.scheme = 'Red' #change this to be gotten from a file
        self.image = pygame.image.load(board_file_D[self.scheme][0])
        self.x = x
        self.y = y
        self.rect = (self.x, self.y, 40, 40)

    def update(self):
        self.x += bkg.dx
        self.y += bkg.dy
        self.rect = Rect(self.x, self.y, 40, 40)
        

class Floor(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.scheme = 'Red' # change this to be goten some other means
        self.image = pygame.image.load(board_file_D[self.scheme][1])
        self.x = x
        self.y = y
        self.rect = (self.x, self.y, 40,40)

    def update(self):
        self.x += bkg.dx
        self.y += bkg.dy
        self.rect = Rect(self.x, self.y, 40, 40)
        
#################################################
#           Enemy #1 - ball of spikes           #
#################################################

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
        self.dir = dr.lower().strip()
        self.D = {'north':(0,-self.S), 'east':(self.S,0), 'south':(0,self.S), 'west': (-self.S,0)}
        background.blit(self.image, (self.x, self.y))

    def update(self):
        #index indexes images; time is the delay for screen travel
        self.index += 1
        if bkg.move:    #If backround moves then...
            self.x += bkg.move_D[bkg.key][0]
            self.y += bkg.move_D[bkg.key][1]
        if self.index == 2:  #reset image index to 0 if maxvalue
            self.index = 0
        self.time += 1
        if self.time == self.time_max: # Positional move in time
            self.time = 0
            self.check_collide()
            self.x += self.D[self.dir][0]
            self.y += self.D[self.dir][1]
            self.rect = Rect(self.x, self.y, 36, 36)

        self.draw()

    def draw(self):
        self.image = self.images[self.index]
        background.blit(self.image, (self.x, self.y))

    def check_collide(self):
        #check for background collisions
        if pygame.sprite.spritecollide(self, bkg.wallGroup, False):
            self.dir = opposite(self.dir)
        for e in enemies:
            if self.rect != e.rect:
                if pygame.sprite.collide_rect(self, e):
                    self.dir = opposite(self.dir)
                    #e.dir = opposite(e.dir)

############################################
#             Main Character               #
############################################

class Player(pygame.sprite.Sprite):
    def __init__(self, iFile = "", imgRange = 1, x = 322, y = 242, end = '.gif'):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.index_max = imgRange
        for i in range(imgRange):
            image = pygame.image.load(iFile+str(i)+end)
            t = image.get_at((0,0))
            image.set_colorkey(t)
            self.images.append(image)
            
        self.image = self.images[self.index]
        print self.image.get_size()
        
        #coordinates
        self.x = x
        self.y = y
        self.rect = self.image.get_rect()
        self.move = False

    def update(self):
        if self.move:
            if self.index_max > 1:
                self.index +=1
                if self.index == self.index_max: self.index = 0
                self.move = False
        ned.draw()

    def draw(self):
        self.image = self.images[self.index]
        background.blit(self.image, (self.x, self.y))
            
        
        
            
#######################################################################
def _init_bg(filename = "001.map"):
    bg_x, bg_y = open(filename).readline().split(',')
    bg_x, bg_y = int(bg_x), int(bg_y)
    return bg_x*40, bg_y*40

def get_maze(filename = "001.map"):
    array = []
    f = open("001.map")
    _x, _y = f.readline().split(',')
    _x, _y = int(_x), int(_y)
    for l in range(_y):
        appStr = f.readline().rstrip('\n')
        array.append(appStr.split(','))
    f.close()
    for i in range(_y):
        for j in range(_x):
            array[i][j] = int(array[i][j])
    return _x, _y, array

def opposite(string):
    if string == 'north':
        return 'south'
    elif string == 'south':
        return 'north'
    elif string == 'east':
        return 'west'
    elif string == 'west':
        return 'east'

def tile_save(x, y, array, filename, ldex):
    col_list = board_file_D.keys()
    img1 = pygame.image.load(board_file_D[col_list[ldex]][0])
    img0 = pygame.image.load(board_file_D[col_list[ldex]][1])
    img = [img0, img1]
    nx, ny = 0,0
    bsurf = pygame.Surface((x*40, y*40))
    for i in xrange(y):
        for j in xrange(x):
            bsurf.blit(img[array[i][j]], ((j-nx)*40, (i-ny)*40))
    pygame.image.save(bsurf, filename + str(ldex) +".jpg")

def pq():
    pygame.display.quit()
    s = "*"*40
    print s
    print "*           Thanks for playing!        *"
    print s

def get_spikes(filename = "001.npc"):
    slist = []
    fp = open(filename)
    for line in fp:
        x, y, d, w, s = line.split(',')
        x, y, w, s = int(x), int (y), int(w), int(s)
        slist.append(SpikeBall(x, y, d, w, s))
    fp.close()
    return slist
    

screen = pygame.display.set_mode((640,480))
pygame.display.set_caption("Test to see how the new Ned Images look")
background = pygame.Surface(_init_bg())


if __name__ == "__main__":
    try:
        done = False
        bkg = Field()
        ned = Player('ned', 2)
        #Load NPCs...
        enemies = pygame.sprite.Group(get_spikes())
        clk = pygame.time.Clock()
        while not done:
            clk.tick(30)
            
            
            for e in pygame.event.get():
                if e.type == QUIT:
                    done = True
                if e.type == KEYDOWN:
                    """up = 273, down = 274, right = 275, left = 276"""
                    if e.key == 27:
                        done = True
                    if e.key == 32:
                        print bkg.pos_xy
                    if e.key == ord('s'):
                        iName = "maze"
                        tile_save(lx, ly, larray, iName, ldex)
                        print "Saved Image", iName

            k = pygame.key.get_pressed()
            if k[273]:
                bkg.update('up')
                ned.move = True
            elif k[274]:
                bkg.update('down')
                ned.move = True
            if k[275]:
                bkg.update('right')
                ned.move = True
            elif k[276]:
                bkg.update('left')
                ned.move = True

            m = pygame.mouse.get_pressed()
            if m[0]:
                mx, my = pygame.mouse.get_pos()
                mx -= bkg.pos_xy[0]
                my -= bkg.pos_xy[1]
                print mx, my
                    

            bkg.update()
            screen.blit(background, (0,0))
            pygame.display.update()
            
    except TypeError or AttributeError or IOError or NameError or IndexError, e:
        pygame.display.quit()
        print e

    pq()
