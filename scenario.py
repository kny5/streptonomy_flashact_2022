import pygame
import sys
from pygame.locals import *
import cv2
from pygame import mixer
from chapin_engine.collide import Grid, collision_points, collide
from chapin_engine.controller import controller_scroll, controller_angle
import random

#inits
pygame.init()
mixer.init()
pygame.font.init()


#Window setup
scenario_scale = 2
game_display = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
game_display_window = pygame.display.get_surface().get_size()
print(game_display_window)


def write(text, size, location,color=(255,255,255)):
    font = pygame.font.Font(None,size)
    game_display.blit(font.render(text, True, color), location)

#Load assets
scenario_img = pygame.image.load("assets/art/fondo_1er_plano.png")
grid = Grid('assets/art/fondo.png', scenario_scale, debug=True)
labyrinth_img = pygame.image.load("assets/art/fondo_collision_grid.png")
game_display_size = (labyrinth_img.get_size()[1]*scenario_scale, labyrinth_img.get_size()[0]*scenario_scale)
labyrinth_img_scaled = pygame.transform.scale2x(labyrinth_img)
main_character = [pygame.image.load("assets/art/bacteria/avanzar/avanzar/loop_avanzar_" + str(num) + ".png") for num in range(0,24)]


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


#print(grid.path_points)
def sampling_path_points():
    return random.sample(grid.path_points, 1)[0]


#Game Loop
grid_max = max(grid.points)
gaming = True
animation_step = 0
nitro_score = 0
chinampa_score = 0
pick_up = None
setup = True
timer = 0

class Tapita(pygame.sprite.Sprite):
    g = .2
    def __init__(self, pos, screen):
        super().__init__()
        self.image = pygame.image.load("assets/art/objects/tapa.png")
        self.rect = self.image.get_rect(center=pos)
        self.pos_y = pos[1]
        self.speed_y = 0
        self.screen = screen
        self.pos_x = pos[0]
        self.speed_x = 0

    def update(self, scroll_pos):
        self.speed_y += self.g
        self.pos_y += self.speed_y
        self.rect.y = self.pos_y

        self.rect.x = self.pos_x

        if self.pos_y > self.screen.get_height():
            self.kill()  # Remove off-screen circles.

fallers = pygame.sprite.Group(Tapita((200,200),game_display))


while gaming:
    if setup:
        sample_position = sampling_path_points()
        setup = False

    clock.tick(game_FPS)

    if animation_step >= len(main_character):
        animation_step = 0

    if timer >= 200:
        timer = 0
        randomizer = (random.randrange(10,grid_max[0], 50), 0)
        fallers.add(Tapita((scroll_translation[0]+randomizer[0], scroll_translation[1]+randomizer[1]), game_display))

    #images to display
    game_display.blit(scenario_img, (0,0))

    #pygame.draw.rect(game_display, (255,255,255), pygame.Rect(0, 0, game_display_window[0], game_display_window[1]), 50)
    scroll_translation = controller_scroll(pygame.mouse.get_pos(), game_display_window, (labyrinth_img_scaled.get_size()[0],labyrinth_img_scaled.get_size()[1] ))

    game_display.blit(labyrinth_img_scaled, scroll_translation)
    mouse_angle = controller_angle(pygame.mouse.get_pos(), game_display_window)

    main_character_rotated = pygame.transform.rotate(main_character[animation_step], mouse_angle)
    main_character_centre = (pygame.mouse.get_pos()[0] - main_character_rotated.get_rect()[2]*0.5, pygame.mouse.get_pos()[1] - main_character_rotated.get_rect()[3]*0.5)
    game_display.blit(main_character_rotated, main_character_centre)

    #uitexts
    write("pointer: " + str(main_character_centre), 20, pygame.mouse.get_pos())
    write("Nitro: " + str(round(nitro_score)), 100, (100,100))
    write("Root: " + str(round(chinampa_score)), 100, (500,100))
    write("Nitro_position: " + str(sample_position), 50, (200,200))
    nitro_position = (scroll_translation[0] - 75*0.5 + sample_position[0], scroll_translation[1] - 95*0.5 + sample_position[1] )
    nitro_collide = collide(nitro_position, pygame.mouse.get_pos())
    write("NH3", 200, nitro_position)


    #circles
    #pygame.draw.circle(game_display, (255,255,255), (scroll_translation[0] + grid_max[0], scroll_translation[1] + grid_max[1]), 200, 2)
    pygame.draw.line(game_display, (255,255,255), pygame.mouse.get_pos(), nitro_position, 2)
    pygame.draw.line(game_display, (255,255,255), (0,nitro_position[1]), (grid_max[0], nitro_position[1]), 2)
    pygame.draw.line(game_display, (255,255,255), (nitro_position[0], 0), (nitro_position[0], grid_max[1]), 2)

    #roots
    game_display.blit(root_img_1, (scroll_translation[0]+2000*2, scroll_translation[1]))
    game_display.blit(root_img_2, (scroll_translation[0]+2300*2, scroll_translation[1]))
    game_display.blit(root_img_3, (scroll_translation[0]+3400*2, scroll_translation[1]))

    if not nitro_collide and not pick_up:
        game_display.blit(nitro_img, nitro_position)

    else:
        game_display.blit(nitro_img, pygame.mouse.get_pos())
        nitro_score += 0.005
        pick_up = True

    root_collide = collide((scroll_translation[0]+2000*2, scroll_translation[1]), nitro_position)

    if root_collide and pick_up:
        chinampa_score += 1

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                gaming = False
                break
            if event.key == pygame.K_RETURN:
                sample_position = sampling_path_points()
            #if event.type == pygame.MOUSEBUTTONDOWN:
                pick_up = False


    fallers.update(scroll_translation)
    fallers.draw(game_display)
    pygame.display.update()
    animation_step += 1
    timer += 1
