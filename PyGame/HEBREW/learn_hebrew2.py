import pygame
from pygame.locals import *
import os, sys
from random import randint

os.chdir("C:\\Documents and Settings\\Owner\\Desktop\\Ryan's Programming Stuff\\Sophie Games\\HEBREW")
WINSIZE=(640,480)
#screen=pygame.display.set_mode((0,0),FULLSCREEN)
screen=pygame.display.set_mode(WINSIZE)
pygame.display.set_caption("Learning Hebrew is FUN!")
background=pygame.display.get_surface()

pygame.font.init()

background.fill((250,250,250))

alefbet=["Aleph", "Bet", "Gimel", "Dalet", "He",
         "Vav", "Zayin", "Het", "Tet", "Yod", "Khaf", 
         "Khaf_Sofit", "Lamed", "Mem", "Mem_Sofit",
         "Nun", "Nun_Sofit", "Samekh", "Ayin", "Pe",
         "Pe_Sofit", "Tsade", "Tsade_Sofit", "Qoph",
         "Resh", "Shin", "Tav"
         ]

q=pygame.display.quit

class Hebrew():
    def __init__(self):
        self.names={}
        base_img=get_square_text()
        for line in open("data\\details.dat"):
            sides=line.split(':')
            rect=[]
            for i in sides[1].split(','):
                rect.append(int(i))
            self.names[sides[0]]=(rect[0],rect[1],rect[2],rect[3])
        for a in self.names:
            img=base_img.subsurface(self.names[a])
            img.set_colorkey(img.get_at((0,0)))
            setattr(self, a, img)
        
def get_square_text():
    quilt=pygame.image.load("data\\hebrewc.gif")
    return quilt

def center(attr):
    big=background.get_size()
    small = getattr(letters, attr).get_size()
    x=(big[0] - small[0])/2
    y=(big[1] - small[1])/2
    return x, y

letters=Hebrew()

def main(run=True):
    bk_drop=get_square_text()
    show=False
    index=0
    rgb=(255,255,255)
    fulscreen=0
    mf = pygame.font.SysFont('elephant', 24)
    
    while run:
        for e in pygame.event.get():
            if e.type==2:#KEYDOWN
                
                if e.key==27:
                    run=not run
                elif e.key==32:
                    rgb = (randint(0,255), randint(0,255), randint(0,255))
                    background.fill(rgb)
                    if vars().has_key('image'):
                        background.blit(getattr(letters, image),center(image))
                        background.blit(title, ( (WINSIZE[0] / 2) - (title.get_width() / 2), 305))
                else:
                    image=alefbet[index % len(alefbet)]
                    title = mf.render(image, 0, (0, 0, 0))
                    background.fill(rgb)
                    background.blit(getattr(letters, image),center(image))
                    background.blit(title, ( (WINSIZE[0] / 2) - (title.get_width() / 2), 305))
                    index+=1
                
            elif e.type==5:#MOUSEBUTTONDOWN
                print e
                
        screen.blit(background,(0,0))
        pygame.display.update()
    q()
if __name__=="__main__":main()
