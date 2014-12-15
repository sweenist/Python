# -*- coding: utf-8 -*-
bkg_img = "logoback.bmp"

import pygame
from pygame.locals import *
from sys import exit

screen = pygame.display.set_mode((640,480),0,32)


background = pygame.image.load(bkg_img).convert()
pygame.font.init()
title_font = pygame.font.SysFont("Arial", 50, True, True)

def run():
    pygame.display.set_caption("THE SWEENIST Productions ©2008")
    pygame.mouse.set_visible(False)
    i = 0
    Show = True
    while Show:
        for e in pygame.event.get():
            if e.type == QUIT:
                pygame.quit()
                Show = False
                exit()
            if e.type == KEYDOWN:
                Show = False
                return
            
        titshad = title_font.render("THE SWEENIST PRESENTS:", True, (0,0,35))
        w = titshad.get_width()
        
        for i in range(30):
            screen.blit(background, (0,0))
            screen.blit(titshad, (320 - w/2 + 2, 200+2))
            tits = title_font.render("THE SWEENIST PRESENTS:", True, (225+i,150+i*3,0))
            screen.blit(tits, (320 - w/2, 200))
            pygame.display.update()
            pygame.time.wait(50)

        for i in range(220):
            screen.blit(background, (0,0))
            screen.blit(titshad, (320 - w/2 + 2, 200+2))
            tits = title_font.render("THE SWEENIST PRESENTS:", True, (255-i,max(0, 240-i*3),0))
            screen.blit(tits, (320 - w/2, 200))
            pygame.display.update()
#            pygame.time.wait(5)
       
        Show = False
        pygame.mouse.set_visible(not Show)
            
if __name__ == "__main__": run()
