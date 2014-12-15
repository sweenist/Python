spr_big = "NedINS.bmp"
spr_arr = "NedArrow.bmp"
import pygame
from pygame.locals import *
from sys import exit

class Selection_Boxes(object):
    def __init__(self):
        self.selection = 1
        self.ColBack = (255,190,10)
        self.image = pygame.image.load(spr_arr)
        trans = self.image.get_at((0,0))
        self.image.set_colorkey(trans)
        self.rect = self.image.get_rect()
        self.rect.center = (150, 150)
        self.sel_font = pygame.font.Font("AbbeyME.ttf", 30)
        
    def update(self):
        if self.selection == 1:
            inc = 0
            self.selCol1 = (90,10,255)
            self.selCol2 = self.selCol3 = (10,10,10)
        elif self.selection == 2:
            inc = 81
            self.selCol2 = (90,10,255)
            self.selCol1 = self.selCol3 = (10,10,10)
        elif self.selection == 3:
            inc = 162
            self.selCol3 = (90,10,255)
            self.selCol2 = self.selCol1 = (10,10,10)


        self.sel1 = self.sel_font.render("PLAY GaME", True, self.selCol1)
        self.sel2 = self.sel_font.render("HoW TO PLAY", True, self.selCol2)
        self.sel3 = self.sel_font.render("EXIT", True, self.selCol3)

        pygame.draw.rect(screen, self.ColBack, (123, 123+ inc, 394, 67))
        screen.blit(self.sel1, (170, 145))
        screen.blit(self.sel2, (170, 230))
        screen.blit(self.sel3, (170, 307))
        screen.blit(self.image, (130, 140 +inc))

def instructions_show():
    page = 1
    inst_font = pygame.font.SysFont("trebuchetms", 24)
    inLabel, w = [], []
    done = False
    while True:
        if not done:
            if page == 1:
                instructions_text = ("How to play",
                                     "Ned's A-MAZ-ing Adventure",
                                     "",
                                     "Ned is on a quest to eat pie.",
                                     "However, Ned has to go through",
                                     "a series of mazes to get some",
                                     "pie to eat.",
                                     "Ned needs your help to skillfully",
                                     "manouvre through these beastly labyrinths!"
                                     )
            elif page == 2:
                instructions_text = ("How to play",
                                     "Ned's A-MAZ-ing Adventure",
                                     "",
                                     "ARROW KEYS move Ned in all directions",
                                     "   (or at least 8 different ones)",
                                     "CAPSLOCK makes Ned run!",
                                     "   If you hold SHIFT, ALT, or CTRL",
                                     "   while CAPSLOCK is on, Ned will walk",
                                     "",
                                     "ESCAPE exits the game"
                                     )

            for line in instructions_text:
                testLab = inst_font.render(line, True, (0,0,0))
                w.append(testLab.get_width())
                inLabel.append(testLab)
                done = True

        for e in pygame.event.get():
            if e.type == KEYDOWN:
                page +=1
                done = False
                w = []
                inLabel = []
                if page == 3:
                    return
            if e.type == MOUSEBUTTONDOWN:
                page +=1
                done = False
                w = []
                inLabel = []
                if page == 3:
                    return                

        pygame.draw.rect(screen, (0,0,0), (100, 100, 440, 280),3)
        pygame.draw.rect(screen, (255,255,255), (103, 103, 434, 274))

        for i in range(len(inLabel)):
            screen.blit(inLabel[i], (320 - (w[i]/2), 116 +(i*25)))

        pygame.display.update()
    

def draw_border():
    _x = screen.get_size()[0]
    _y = screen.get_size()[1]
    r, g, b = 127, 127, 180
    for i in xrange(120):
        pygame.draw.rect(screen, (r+i, g+i, min(b+i, 255)), (i, i, _x-(i*2), _y-(i*2)), 1)
    for i in range(3):
        pygame.draw.rect(screen, (0,0,0), (120,120+(i*81), 400, 73), 5)
    
        

pygame.init()
screen = pygame.display.set_mode((640, 480), 0, 32)
pygame.display.set_caption("Ned's A-MAZE-ing Adventure")

background = pygame.Surface(screen.get_size())
titlepic= pygame.image.load(spr_big)
titlepic.set_colorkey((255,255,255))

title_font = pygame.font.Font("AbbeyME.ttf", 60)
title_title = title_font.render("Ned's Maze Game", True, (0,0,0))

background.fill((255, 255, 255))
pygame.display.set_caption("Ned's Maze Game! -2008-")
def play():
    arrow = Selection_Boxes()
    mselect = False
    
    while True:
        for e in pygame.event.get():
            if e.type == QUIT:
                pygame.quit()
                exit()
            if e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    pygame.quit()
                    exit()
                if e.key == K_UP:
                    arrow.selection -=1
                    if arrow.selection == 0:
                        arrow.selection = 3
                elif e.key == K_DOWN:
                    arrow.selection +=1
                    if arrow.selection == 4:
                        arrow.selection = 1
                elif e.key ==K_RETURN:
                    if arrow.selection == 1:
                        return
                    elif arrow.selection ==2:
                        instructions_show()
                    elif arrow.selection == 3:
                        pygame.quit()
                        exit()

        x, y = pygame.mouse.get_pos()
        if x in range(120, 520):
            if y in range(120, 193):
                arrow.selection =1
                mselect = True
            elif y in range(201, 274):
                arrow.selection = 2
                mselect = True
            elif y in range(282, 347):
                arrow.selection = 3
                mselect = True
            else:
                arrow.selection = arrow.selection
                mselect = False
        else:
            mselect = False
        

        if pygame.mouse.get_pressed()[0] == 1 and mselect ==True:
            if arrow.selection == 1:
                return
            elif arrow.selection ==2:
                instructions_show()
            elif arrow.selection == 3:
                pygame.quit()
                exit()
            
            


        screen.blit(background, (0,0))
        draw_border()
        arrow.update()
        screen.blit(titlepic, (0,10))
        screen.blit(title_title, (90, 48))

        pygame.display.update()

if __name__ == "__main__": play()
            
