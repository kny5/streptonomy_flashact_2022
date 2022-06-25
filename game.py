import pygame
import sys
from pygame.locals import *

clock = pygame.time.Clock()
screen = pygame.display.set_mode((1920,1080))

bg = pygame.image.load("images/assets/fondo_1er_plano.png")
laberinto = pygame.image.load("images/assets/fondo.png")


pygame.mouse.set_visible(0)

ship = pygame.image.load("images/assets/streptonomy.png")

screen.blit(ship, pygame.mouse.get_pos())

shot = pygame.image.load("images\shot.png")
shoot_y = 0


pygame.display.set_caption('galaxy invaders')

while True:
    clock.tick(60)
    screen.fill((255,0,0))
    screen.blit(bg, (0,0))
    screen.blit(laberinto, (0,0))
    screen.scroll(100)
    x,y = pygame.mouse.get_pos()
    screen.blit(ship, pygame.mouse.get_pos())
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            shoot_y = 500
            shoot_x = x

    if shoot_y > 0:
        screen.blit(shot, (shoot_x, shoot_y))
        shoot_y -= 10

    pygame.display.update()
