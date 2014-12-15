##################################
#   Test Collide Rect for Maze   #
##################################
import pygame
from pygame.locals import *

pygame.init()
class Maze(object):
    def __init__(self):
        self.walls = []
        self.floors = []
        self.array = []
        self.get_map()
        self.get_walls()
        self.get_floors()
        self.dx = 0
        self.dy = 0

    def get_map(self, f = 'map001.txt'):
        fp = open(f)
        x, y = fp.readline().split(',')
        self.ax, self.ay = int(x), int(y)
        for line in fp: self.array.append(line.split(','))
        fp.close()
        for a in self.array:
            for b in range(len(a)):
                a[b] = int(a[b])

    def get_floors(self):
        for i in range(self.ay):
            for j in range(self.ax):
                if self.array[i][j] == 0:
                    fl = Floor(j*40, i*40)
                    self.floors.append(fl)
        self.floorGroup = pygame.sprite.Group(self.floors)

    def get_walls(self):
        for i in range(self.ay):
            for j in range(self.ax):
                if self.array[i][j] == 1:
                    fl = Block(j*40, i*40)
                    self.walls.append(fl)
        self.wallGroup = pygame.sprite.Group(self.walls)
    
    def update(self):
        self.floorGroup.update()
        self.wallGroup.update()

    def draw(self):
        self.floorGroup.draw(background)
        self.wallGroup.draw(background)
        
class Block(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('MazeBlock6.gif')
        self.x = x
        self.y = y
        self.rect = (self.x, self.y, 40, 40)

    def update(self):
        self.x -= m.dx
        self.y -= m.dy
        self.rect = Rect(self.x, self.y, 40, 40)
        
    def draw(self):
        background.blit(self.image, (self.x, self.y))
        

class Floor(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('MazeFloor5.gif')
        self.x = x
        self.y = y
        self.rect = (self.x, self.y, 40,40)

    def update(self):
        self.x -= m.dx
        self.y -= m.dy
        self.rect = Rect(self.x, self.y, 40, 40)
        
    def draw(self):
        background.blit(self.image, (x*40, y*40))
    
class Spike(pygame.sprite.Sprite):
    def __init__(self, x, y, _dir = 'south', speed = 4):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('npc_spike2.gif')
        self.x = x
        self.y = y
        t_col = self.image.get_at((0,0))
        self.image.set_colorkey(t_col)
        self.rect = Rect(self.x, self.y, 36, 36)
        self.dir = _dir
        self.D = {'north': (0,-speed), 'south':(0,speed), 'east':(speed,0), 'west':(-speed,0)}

    def update(self):
        oldx, oldy = self.x, self.y
        self.x += self.D[self.dir][0] + m.dx
        self.y += self.D[self.dir][1] + m.dy
        if pygame.sprite.spritecollide(self, m.wallGroup, False):
            self.oppose()
            self.x = oldx + self.D[self.dir][0] + m.dx
            self.y = oldy + self.D[self.dir][1] + m.dy
        self.rect = Rect(self.x, self.y, 36,36)
        #self.draw()

    def draw(self):
        background.blit(self.image, (self.x, self.y))

    def oppose(self):
        if self.dir == 'north':
            self.dir = 'south'
        elif self.dir == 'south':
            self.dir = 'north'
        if self.dir == 'east':
            self.dir = 'west'
        elif self.dir == 'west':
            self.dir = 'east'

def load_map():
    fp = open('map001.txt')
    array = []
    #first line of file pointer and edit
    array_x, array_y = fp.readline().split(',')
    array_size = [int(array_x), int(array_y)]
    #rest of lines in file
    for line in fp:
        array.append(line.split(','))
    fp.close()
    #now intergerize array
    for y in range(array_size[1]):
        for x in range(array_size[0]):
            array[y][x] = int(array[y][x])
    return array_size, array

def q():
    pygame.quit()

array_size, array = load_map()
array_xy = (array_size[0]*40, array_size[1] *40)
screen = pygame.display.set_mode((640,480))
pygame.display.set_caption("Testing Collisions")
background = pygame.Surface(array_xy)

spike = Spike(42,42)
spike1 = Spike(442, 322, 'north')
spike2 = Spike(202, 42, 'east', 5)
m=Maze()
enemies = pygame.sprite.Group(spike, spike1, spike2)

if __name__ == "__main__":
    done = False
    bx, by = 0, 0
    while not done:
        m.update()
        enemies.update()
        m.draw()
        enemies.draw(background)
        screen.blit(background, (bx, by))
        pygame.display.update()
        m.dx, m.dy = 0, 0
        
        for e in pygame.event.get():
            if e.type == KEYDOWN:
                if e.key == 27:
                    q()
                    done = True

        k = pygame.key.get_pressed()
        if k[273]:
            by -= 2
        elif k[274]:
            by += 2
        elif k[275]:
            bx += 2
        elif k[276]:
            bx -= 2
            
            

        
        
    
