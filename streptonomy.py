import pygame
import sys
from pygame.locals import *
from math import atan, degrees, sqrt, pi, tan
from chapin_engine.collide import Grid, collision_points

background_scale = 4
window_size = (1920,1080)
background_size = (window_size[0]*background_scale, window_size[1]*background_scale)
streptonomy_scale = 0.9
streptonomy_size = (54*streptonomy_scale,172*streptonomy_scale)
controller_ui_txt_size = 20

clock = pygame.time.Clock()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

display_size = pygame.display.get_surface().get_size()
background = pygame.image.load("assets/art/fondo_1er_plano.png")
laberinto = pygame.transform.scale(pygame.image.load("assets/art/fondo_collision.png"), background_size)

surface = pygame.Surface(background_size)

#streptonomy = pygame.image.load("assets/art/bacteria/avanzar/avanzar/loop_avanzar_0.png")
#screen.blit(streptonomy, pygame.mouse.get_pos())
pygame.display.set_caption('streptonomy - Flash Act 2022')



#configuracion
pygame.mouse.set_visible(0)

count_x = 0
count_y = 0

pygame.font.init()
font=pygame.font.Font(None,20)


def write(text,location,color=(255,255,255)):
    screen.blit(font.render(text,True,color),location)


#animation configs
value = 0
#streptonomy_sprites = [pygame.image.load("assets/art/bacteria/avanzar/avanzar/loop_avanzar_00000.png"), pygame.image.load("assets/art/bacteria/avanzar/avanzar/loop_avanzar_00005.png"), pygame.image.load("assets/art/bacteria/avanzar/avanzar/loop_avanzar_00010.png"), pygame.image.load("assets/art/bacteria/avanzar/avanzar/loop_avanzar_00015.png"), pygame.image.load("assets/art/bacteria/avanzar/avanzar/loop_avanzar_00020.png")]

streptonomy_sprites = [pygame.image.load("assets/art/bacteria/avanzar/avanzar/loop_avanzar_" + str(num) + ".png") for num in range(0,24)]
dirt_8_sprites = [pygame.image.load("assets/art/manchas_frames_png/mancha8/8/mancha8_" + str(num) + ".png") for num in range(0,24)]


def rotate_streptonomy(sprites):
    rotated = map(lambda x: pygame.transform.rotate(x, streptonomy_angle), sprites)
    return list(rotated)


def scale_streptonomy(sprites):
    scaled = map(lambda x: pygame.transform.scale(x, streptonomy_size), sprites)
    return list(scaled)




def controller_angle(mouse_position):
    xi, yi = 0, 0
    xf, yf = mouse_position[0]-display_size[0]/2, mouse_position[1]-display_size[1]/2
    try:
        m = (yf-yi)/(xf-xi)
        dx = xi-xf
        dy = yi-yf
    except:
        m = 0
    if m >= 0:
        angle = atan(m)
    else:
        angle = pi + atan(m)
    return 90 - degrees(angle)


def controller_lenght(mouse_position):
    xi, yi = display_size[0]/2, display_size[1]/2
    xf, yf = mouse_position[0], mouse_position[1]
    return sqrt(((yf-yi)**2)+((xi-xf)**2))


def controller_scroll(mouse_position):
    global count_x, count_y
    factor = 50
    xi, yi = display_size[0]/2, display_size[1]/2
    xf, yf = mouse_position[0], mouse_position[1]
    speed = sqrt(((yf-yi)**2)+((xi-xf)**2)) / factor

    if xf > xi:
        x_sense = 1*speed
    else:
        x_sense = -1*speed
    if yf > yi:
        y_sense = 1*speed
    else:
        y_sense = -1*speed

    count_x -= x_sense
    count_y -= y_sense

    return (count_x, count_y)


game_grid = Grid('assets/art/fondo.png', debug=False)

while True:
    streptonomy_angle = controller_angle(pygame.mouse.get_pos())
    # animation
    if value >= len(streptonomy_sprites):
        value = 0

    # Storing the sprite image in an
    # image variable
    streptonomy_sprites_scaled = scale_streptonomy(streptonomy_sprites)
    streptonomy_sprites_rot = rotate_streptonomy(streptonomy_sprites_scaled)
    streptonomy_anim = streptonomy_sprites_rot[value]

    #translations
    screen.blit(background, (0,0))
    #screen.blit(laberinto, controller_scroll(pygame.mouse.get_pos()))
    screen.blit(laberinto, (0,0))
    screen.blit(streptonomy_anim, pygame.mouse.get_pos())

    #Texts
    write("pointer: " + str(pygame.mouse.get_pos()), pygame.mouse.get_pos())
    write(str((count_x, count_y)), (pygame.mouse.get_pos()[0]-50, pygame.mouse.get_pos()[1]-50))
    write("Streptonomy", (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]-20))
    write("Nitrogeno 10 gpL", (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]+150))

    #controller ui
    write(str(controller_angle(pygame.mouse.get_pos())), (display_size[0]/2,display_size[1]/2))
    write(str(controller_lenght(pygame.mouse.get_pos())), (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]+175))
    write(str(controller_scroll(pygame.mouse.get_pos())), (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]+225))

    #drawline
    #pygame.draw.line(screen, (255,255,255), pygame.mouse.get_pos(), (pygame.mouse.get_pos()[0]-50, pygame.mouse.get_pos()[1]-50))
    #pygame.draw.line(screen, (255,255,255), pygame.mouse.get_pos(), (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]+100))
    pygame.draw.line(screen, (255,255,255), pygame.mouse.get_pos(), (display_size[0]/2,display_size[1]/2), 2)
    #drawcircle
    pygame.draw.circle(screen, (255,255,255), (display_size[0]/2,display_size[1]/2), 50, 2)
    pygame.draw.circle(screen, (255,255,255), pygame.mouse.get_pos(), 100, 2)
    #drawrectangle ui
    #pygame.draw.rect(screen, (255,255,255), pygame.Rect(30, 30,display_size[1], 60))

    #collision

    pygame.draw.polygon(screen, (255,255,255),collision_points(game_grid, pygame.mouse.get_pos()), 1)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            pass

    value += 1
    pygame.display.update()
