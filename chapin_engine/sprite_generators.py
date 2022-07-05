
import pygame


GRAVITY = .2  # Pretty low gravity.

class Circle(pygame.sprite.Sprite):

    def __init__(self, pos, screen):
        super().__init__()
        self.screen = screen
        self.image = pygame.Surface((80, 80), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (30, 90, 150), (40, 40), 40)
        self.rect = self.image.get_rect(center=pos)
        self.pos_y = pos[1]
        self.speed_y = 0

    def update(self, scroll_pos):
        self.speed_y += GRAVITY
        self.pos_y += self.speed_y
        self.rect.y = self.pos_y

        if self.pos_y > self.screen.get_height():
            self.kill()  # Remove off-screen circles.


def run_game():
    pygame.init()
    screen = pygame.display.set_mode((1270, 670))
    clock = pygame.time.Clock()
    running = True
    circles = pygame.sprite.Group(Circle((600, 0), screen))

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                circles.add(Circle(event.pos, screen))

        circles.update()

        screen.fill((10, 10, 30))
        circles.draw(screen)

        pygame.display.flip()
        clock.tick(60)


run_game()
pygame.quit()
