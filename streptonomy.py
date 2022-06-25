import pygame
import sys
from pygame.locals import *



clock = pygame.time.Clock()
screen = pygame.display.set_mode((1920,1080))

background = pygame.image.load("assets/art/fondo_1er_plano.png")
laberinto = pygame.image.load("assets/art/fondo.png")

surface = pygame.Surface((3840, 2160))

streptonomy = pygame.image.load("assets/art/streptonomy.png")
screen.blit(streptonomy, pygame.mouse.get_pos())
pygame.display.set_caption('streptonomy - Flash Act 2022')

#configuracion
pygame.mouse.set_visible(0)


while True:

    clock.tick(60)
    screen.blit(background, (0,0))
    screen.blit(laberinto, (0,0))
    screen.blit(streptonomy, pygame.mouse.get_pos())

    # screen.update(pygame.mouse.get_pos())

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            #click event
            pass

    pygame.display.update()
