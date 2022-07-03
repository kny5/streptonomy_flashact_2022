import pygame
import sys
from pygame.locals import *
import cv2
from pygame import mixer
from chapin_engine.collide import Grid, collision_points
from chapin_engine.controller import controller_scroll, controller_angle

#inits
pygame.init()
mixer.init()


#Window setup
scenario_scale = 2
game_display = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
game_display_window = pygame.display.get_surface().get_size()


#Load assets
scenario_img = pygame.image.load("assets/art/fondo_1er_plano.png")
game_display_size = tuple(map( lambda p: scenario_scale*p, scenario_img.get_size()))
labyrinth_img = pygame.image.load("assets/art/fondo_collision.png")
#labyrinth_img_scaled = pygame.transform.scale(labyrinth_img,labyrinth_img.get_size())
labyrinth_img_scaled = pygame.transform.scale(labyrinth_img, game_display_size)
main_character = [pygame.image.load("assets/art/bacteria/avanzar/avanzar/loop_avanzar_" + str(num) + ".png") for num in range(0,24)]


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
while gaming:
    clock.tick(game_FPS)
    #images to display
    game_display.blit(scenario_img, (0,0))
    game_display.blit(labyrinth_img_scaled, controller_scroll(pygame.mouse.get_pos(), game_display_window, labyrinth_img_scaled.get_size()))
    mouse_angle = controller_angle(pygame.mouse.get_pos(), game_display_window)

    main_character_rotated = pygame.transform.rotate(main_character[0], mouse_angle)
    main_character_centre = (pygame.mouse.get_pos()[0] - main_character_rotated.get_rect()[2]*0.5, pygame.mouse.get_pos()[1] - main_character_rotated.get_rect()[3]*0.5)
    print("0")
    #print(pygame.mouse.get_pos(), main_character_centre, main_character_rotated.get_rect())
    game_display.blit(main_character_rotated, main_character_centre)
    pygame.display.update()
    for event in pygame.event.get():
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_ESCAPE:
                gaming = False
                break
