import pygame
import sys
from pygame.locals import *
import cv2
from pygame import mixer
from chapin_engine.collide import Grid, collision_points, collide
from chapin_engine.controller import controller_scroll, controller_angle

#inits
pygame.init()
mixer.init()
pygame.font.init()


#Window setup
scenario_scale = 2
game_display = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
game_display_window = pygame.display.get_surface().get_size()
#font=pygame.font.Font(None,20)


def write(text, size, location,color=(255,255,255)):
    font=pygame.font.Font(None,size)
    game_display.blit(font.render(text,True,color),location)

#Load assets
scenario_img = pygame.image.load("assets/art/fondo_1er_plano.png")
game_display_size = tuple(map( lambda p: scenario_scale*p, scenario_img.get_size()))
labyrinth_img = pygame.image.load("assets/art/fondo_collision_grid.png")
labyrinth_img_scaled = pygame.transform.scale(labyrinth_img, game_display_size)
main_character = [pygame.image.load("assets/art/bacteria/avanzar/avanzar/loop_avanzar_" + str(num) + ".png") for num in range(0,24)]

#load other sprites
leaf_img = pygame.image.load("assets/art/objects/hoja2.png")
nitro_img = pygame.image.load("assets/art/objects/nitrogeno.png")




#load start menu assets
welcome_bg_img = pygame.image.load("assets/inicio/fondo-1080.png")
welcome_logos_img = pygame.image.load("assets/inicio/conjunto-1080.png")
welcome_title_img = pygame.image.load("assets/inicio/logo_inicio_00000.png")


#load mediafiles
mixer.music.load("assets/audio/poema.mp3")


#Global variables
clock = pygame.time.Clock()


#Splash and welcome loop
game_FPS = 60
welcoming = False
while welcoming:
    clock.tick(game_FPS)
    game_display.blit(welcome_bg_img, (0,0))
    game_display.blit(welcome_logos_img, (0,0))
    game_display.blit(welcome_title_img, (0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_RETURN:
                welcoming = False
                break
    pygame.display.update()


#play video
video_FPS = 20
video = cv2.VideoCapture('assets/video/intro_master_texto.mp4')
play_intro = False

if play_intro:
    mixer.music.play()
while play_intro:
    try:
        clock.tick(video_FPS)
        play_intro, intro = video.read()
        game_display.blit(pygame.image.frombuffer(intro.tobytes(),intro.shape[1::-1],"BGR"), (0,0))
        pygame.display.update()
    except AttributeError:
        mixer.music.stop()
        break


#Game Loop
gaming = True
animation_step = 0
nitro_score = 0
while gaming:
    clock.tick(game_FPS)
    if animation_step >= len(main_character):
        animation_step = 0
    #images to display
    game_display.blit(scenario_img, (0,0))

    scroll_translation = controller_scroll(pygame.mouse.get_pos(), game_display_window, labyrinth_img_scaled.get_size())
    game_display.blit(labyrinth_img_scaled, scroll_translation)
    mouse_angle = controller_angle(pygame.mouse.get_pos(), game_display_window)

    main_character_rotated = pygame.transform.rotate(main_character[animation_step], mouse_angle)
    main_character_centre = (pygame.mouse.get_pos()[0] - main_character_rotated.get_rect()[2]*0.5, pygame.mouse.get_pos()[1] - main_character_rotated.get_rect()[3]*0.5)

    print(pygame.mouse.get_pos(), main_character_centre, main_character_rotated.get_rect())
    game_display.blit(main_character_rotated, main_character_centre)

    #uitexts
    write("pointer: " + str(pygame.mouse.get_pos()), 20, pygame.mouse.get_pos())
    write("Nitro: " + str(round(nitro_score)), 100, (100,100))

    #leaf_position = (scroll_translation[0]+250, scroll_translation[1]+250)
    nitro_position = (scroll_translation[0]+550, scroll_translation[1]+550)

    #leaf_collide = collide(leaf_position, pygame.mouse.get_pos())
    nitro_collide = collide(nitro_position, pygame.mouse.get_pos())

    if not nitro_collide:
        game_display.blit(nitro_img, nitro_position)
    else:
        game_display.blit(pygame.transform.rotate(nitro_img, animation_step), nitro_position)
        nitro_score += 0.005

    pygame.display.update()
    animation_step += 1

    for event in pygame.event.get():
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_ESCAPE:
                gaming = False
                break
