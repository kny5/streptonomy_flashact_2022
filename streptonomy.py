import pygame
import sys
from pygame.locals import *
from math import atan, degrees, sqrt, pi, tan


display_size = (1920, 1080)
background_size = (3840, 2160)
play_limits_max = (1300, 600)
play_limits_min = (400, 300)
#streptonomy_angle = 0
streptonomy_size = (54*0.8,172*0.8)
controller_ui_txt_size = 20

clock = pygame.time.Clock()
screen = pygame.display.set_mode(display_size)

background = pygame.image.load("assets/art/fondo_1er_plano.png")
laberinto = pygame.image.load("assets/art/fondo.png")

surface = pygame.Surface(background_size)

#streptonomy = pygame.image.load("assets/art/bacteria/avanzar/avanzar/loop_avanzar_0.png")
#screen.blit(streptonomy, pygame.mouse.get_pos())
pygame.display.set_caption('streptonomy - Flash Act 2022')



#configuracion
pygame.mouse.set_visible(0)

count_x = 0
count_y = 0

def scroll(pos):
    global count_x, count_y, play_limits_max
    scrolling = []
    if count_x < 0:
        count_x = 0
    if count_y < 0:
        count_y = 0
    if count_x > background_size[0]:
        count_x = background_size[0]
    if count_y < background_size[1]:
        count_y = background_size[1]
    if pos[0] > play_limits_max[0]:
        count_x += 1
    if pos[1] > play_limits_max[1]:
        count_y += 1
    if pos[0] < play_limits_min[0]:
        count_x -= 1
    if pos[1] < play_limits_min[1]:
        count_y -= 1
    else:
        pass
    return (-count_x, -count_y)

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
    xi, yi = display_size[0]/2, display_size[1]/2
    xf, yf = mouse_position[0], mouse_position[1]
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

def controller_scroll(controller_lenght):
    xi, yi = display_size[0]/2, display_size[1]/2
    xf, yf = mouse_position[0], mouse_position[1]

    return scrolling


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

    screen.blit(background, (0,0))
    screen.blit(laberinto, scroll(pygame.mouse.get_pos()))
    screen.blit(streptonomy_anim, pygame.mouse.get_pos())

    #Texts
    write(str(pygame.mouse.get_pos()), pygame.mouse.get_pos())
    write(str((count_x, count_y)), (pygame.mouse.get_pos()[0]-50, pygame.mouse.get_pos()[1]-50))
    write("Streptonomy", (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]-20))
    write("Nitrogeno 10 gpL", (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]+150))

    #controller ui
    write(str(controller_angle(pygame.mouse.get_pos())), (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]+200))
    write(str(controller_lenght(pygame.mouse.get_pos())), (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]+175))

    #drawline
    pygame.draw.line(screen, (255,255,255), pygame.mouse.get_pos(), (pygame.mouse.get_pos()[0]-50, pygame.mouse.get_pos()[1]-50))
    pygame.draw.line(screen, (255,255,255), pygame.mouse.get_pos(), (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]+100))
    pygame.draw.line(screen, (255,255,255), pygame.mouse.get_pos(), (display_size[0]/2,display_size[1]/2))
    #drawcircle
    pygame.draw.circle(screen, (255,255,255), (display_size[0]/2,display_size[1]/2), 50, 1)
    pygame.draw.circle(screen, (255,255,255), pygame.mouse.get_pos(), 100, 1)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            pass

    value += 1
    pygame.display.update()
