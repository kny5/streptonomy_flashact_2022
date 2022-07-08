import pygame
import sys
from pygame.locals import *
import cv2
from pygame import mixer
from chapin_engine.collide import Grid, collide, line_segment, path
from chapin_engine.controller import controller_scroll, controller_angle, count_x, count_y
import random
import pygame.gfxdraw
import time
import copy


#inits
pygame.init()
mixer.init()
pygame.font.init()


#Window setup
scenario_scale = 2
game_display = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
game_display_window = pygame.display.get_surface().get_size()


def write(text, size, location,color=(255,255,255)):
    font = pygame.font.Font(None,size)
    game_display.blit(font.render(text, True, color), location)


#Load assets
scenario_img = pygame.image.load("assets/art/fondo_1er_plano.png")
grid = Grid('assets/art/fondo.png', scenario_scale, debug=True)
labyrinth_img = pygame.image.load("assets/art/fondo_collision_grid.png")
fog_img = pygame.image.load("assets/art/focus.png")
frame_img = pygame.image.load("assets/art/frame.png")
game_display_size = (labyrinth_img.get_size()[1]*scenario_scale, labyrinth_img.get_size()[0]*scenario_scale)
labyrinth_img_scaled = pygame.transform.scale2x(labyrinth_img)
#main_character = [pygame.image.load("assets/art/bacteria/avanzar/avanzar/loop_avanzar_" + str(num) + ".png") for num in range(0,24)]


#load other sprites
leaf_img = pygame.image.load("assets/art/objects/hoja2.png")
nitro_img = pygame.image.load("assets/art/objects/nitrogeno.png")
root_img_1 = pygame.image.load("assets/art/objects/planta2.png")
root_img_2 = pygame.image.load("assets/art/objects/planta2.png")
root_img_3 = pygame.image.load("assets/art/objects/planta2.png")


#load start menu assets
welcome_bg_img = pygame.image.load("assets/inicio/fondo-1080.png")
welcome_logos_img = pygame.image.load("assets/inicio/conjunto-1080.png")
welcome_title_img = pygame.image.load("assets/inicio/logo_inicio_00000.png")


#load mediafiles
mixer.music.load("assets/audio/poema.mp3")


#Global variables
clock = pygame.time.Clock()


#Splash and welcome loop
game_FPS = 50
welcoming = True
while welcoming:
    clock.tick(game_FPS)
    game_display.blit(welcome_bg_img, (0,0))
    game_display.blit(welcome_logos_img, (0,0))
    game_display.blit(welcome_title_img, (0,0))
    game_display.blit(frame_img, (0,0))

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
        game_display.blit(frame_img, (0,0))
        pygame.display.update()
    except AttributeError:
        mixer.music.stop()
        break


def sampling_path_points():
    return random.sample(grid.path_points, 1)[0]

def drawCircleArc(screen,color,center,radius,startDeg,endDeg,thickness):
    (x,y) = center
    rect = (x-radius,y-radius,radius*2,radius*2)
    pygame.draw.arc(screen,color,rect,startDeg,endDeg,thickness)


#Game Loop
print("Range here"*90)
print(grid.shape)
gaming = True
animation_step = 0
nitro_score = 0
chinampa_score = 0
pick_up = None
setup = True
timer = 0
switch = False


class Tapita(pygame.sprite.Sprite):
    g = .1
    def __init__(self, pos, screen):
        super().__init__()
        self.image = pygame.image.load("assets/art/objects/tapa_blur.png")
        self.rect = self.image.get_rect(center=pos)
        self.pos_y = pos[1] - 100
        self.speed_y = 0
        self.screen = screen
        self.pos_x = self.rand_x()
        self.speed_x = 0

    @staticmethod
    def rand_x():
        return random.randrange(10,grid.shape[0], 50)

    def update(self, scroll_pos):
        self.speed_y += self.g
        self.pos_y += self.speed_y
        self.rect.y = self.pos_y+scroll_pos[1]
        self.rect.x = self.pos_x+scroll_pos[0]

        if self.pos_y > grid.shape[1]*scenario_scale:
            self.kill()



class Nitro(pygame.sprite.Sprite):
    def __init__(self, screen):
        super().__init__()
        self.image = pygame.image.load("assets/art/objects/nitrogeno.png")
        self.pos_y = self.rand_y()
        self.speed_y = 0
        self.screen = screen
        self.pos_x = self.rand_x()
        self.speed_x = 0
        self.rect = self.image.get_rect(center=(self.pos_x, self.pos_y))

    @staticmethod
    def rand_x():
        return random.randrange(10,grid.shape[0], 50)

    @staticmethod
    def rand_y():
        return random.randrange(10,grid.shape[1], 50)

    def update(self, scroll_pos):
        self.rect.x = self.pos_x+scroll_pos[0]
        self.rect.y = self.pos_y+scroll_pos[1]



class Main_character_sprite_obj(pygame.sprite.Sprite):
    sprites = [pygame.image.load("assets/art/bacteria/avanzar/avanzar/loop_avanzar_" + str(num) + ".png") for num in range(0,24)]

    @staticmethod
    def sprite_gen(step):
        return Main_character_sprite_obj.sprites[step]

    def __init__(self):
        super().__init__()
        self.health = 100

    def update(self, mouse, step):
        self.image = pygame.transform.rotate(Main_character_sprite_obj.sprite_gen(step), mouse.angle)
        self.rect = self.image.get_bounding_rect()
        self.image = self.image.subsurface(self.rect)
        self.rect.center = (mouse.x, mouse.y)
        print(self.rect)


class Mouse():
    saved_positions = []
    def __init__(self, mouse_pos, game_display):
        self.pos = mouse_pos
        self.x = mouse_pos[0]
        self.y = mouse_pos[1]
        self.angle = controller_angle(self.pos, game_display)

    def relative_position(self, scroll_translation):
         return (int(- scroll_translation[0] + self.x), int(- scroll_translation[1] + self.y))

    def save_pos(self):
        if len(mouse.saved_positions) >= 10:
            self.saved_positions.pop(0)
        self.saved_positions.append(self.pos)

light_blue = (7,207,246,75)
orange = (255, 95, 31, 50)

falling = pygame.sprite.Group()
nitros = pygame.sprite.Group()
bacterias = pygame.sprite.Group()

SCROLL = [0,0]
switch = False
#Game loop
while gaming:
    color = light_blue
    clock.tick(game_FPS)
    mouse = Mouse(pygame.mouse.get_pos(), game_display_window)
    mouse.save_pos()

    #images to display
    game_display.blit(scenario_img, (0,0))

    if setup:
        pygame.mouse.set_visible(0)
        sample_position = sampling_path_points()
        main_character = Main_character_sprite_obj()
        scroll_translation = (0,0)
        for nit in range(100):
            nitros.add(Nitro(game_display))
        setup = False

    if animation_step >= len(Main_character_sprite_obj.sprites):
        animation_step = 0

    if switch:
        scroll_translation = controller_scroll(mouse.pos, game_display_window, (labyrinth_img_scaled.get_size()[0],labyrinth_img_scaled.get_size()[1]))
        SCROLL = copy.copy(scroll_translation)
    else:
        scroll_translation = copy.copy(SCROLL)
        switch = True

    MOUSE_REL = mouse.relative_position(scroll_translation)
    CHECK_RGBA = labyrinth_img_scaled.get_at(MOUSE_REL)[3]

    if CHECK_RGBA == 255:
        switch = False
        color = orange
        main_character.health -= 0.01


    game_display.blit(labyrinth_img_scaled, scroll_translation)
    #circles
    nitro_position = (scroll_translation[0] - 75*0.5 + sample_position[0], scroll_translation[1] - 95*0.5 + sample_position[1] )

    nitro_collide = collide(nitro_position, mouse.pos)

    pygame.draw.aaline(game_display, (239, 1, 149, 255), mouse.pos, line_segment(mouse, nitro_position), 1)

    bacterias.add(main_character)
    main_character.update(mouse, animation_step)

    #pygame.sprite.spritecollideany(main_character, nitros)

    for __r in range(50, 100):
        pygame.gfxdraw.pie(game_display, mouse.x, mouse.y, __r, 0, int(-360/main_character.health), color)

    #uitexts
    #write("pointer: " + str(main_character_centre), 20, mouse.pos)
    #write("Nitrogeno: " + str(round(nitro_score)), 50, (100,100))
    #write("Chinampa power: " + str(round(chinampa_score)), 50, (500,100))
    #write("Nitro_position: " + str(sample_position), 50, (200,200))

    #roots
    game_display.blit(root_img_1, (scroll_translation[0]+2000*2, scroll_translation[1]))
    game_display.blit(root_img_2, (scroll_translation[0]+2300*2, scroll_translation[1]))
    game_display.blit(root_img_3, (scroll_translation[0]+3400*2, scroll_translation[1]))



    if not nitro_collide and not pick_up:
        game_display.blit(nitro_img, nitro_position)
        write("NH3", 100, (nitro_position[0], nitro_position[1]+100))

    else:
        game_display.blit(nitro_img, mouse.pos)
        nitro_score += 0.005
        pick_up = True

    root_collide = collide((scroll_translation[0]+2100*2+100, scroll_translation[1]), mouse.pos)

    if root_collide and pick_up:
        chinampa_score += 0.2

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                gaming = False
                break
            if event.key == pygame.K_RETURN:
                sample_position = sampling_path_points()
            #if event.type == pygame.MOUSEBUTTONDOWN:
                pick_up = False

    if timer >= 900:
        timer = 0
        falling.add(Tapita((scroll_translation), game_display))

    falling.update(scroll_translation)
    falling.draw(game_display)

    nitros.update(scroll_translation)
    nitros.draw(game_display)
    bacterias.draw(game_display)

    game_display.blit(fog_img, (mouse.x -2050, mouse.y - 2050))
    animation_step += 1
    timer += 1

    pygame.display.update()
