import pygame
from pygame.locals import *
import random
import pygame.sprite

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 800
screen_height = 500

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Flappy Bird Game Window")

ground_scroll = 0
scroll_speed = 4
pipe_gap = 150
pipe_frequency = 1500
last_pipe = pygame.time.get_ticks()


bg = pygame.image.load('img/bg.png')
ground_img = pygame.image.load('img/ground.png')

new_bg_width = 800
new_bg_height = 500

new_ground_width = 800
new_ground_height = 100

bg = pygame.transform.scale(bg, (new_bg_width, new_bg_height))
ground_img = pygame.transform.scale(ground_img, (new_ground_width, new_ground_height))

class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for num in range(1, 4):
            img = pygame.image.load(f'img/bird{num}.png')
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.flap_cooldown = 5 
        self.vel = 0
        self.clicked = False
        self.alive = False 
        self.started = False  

    def update(self):
        if self.started:
            if self.alive:
                self.vel += 0.5
                if self.vel > 8:
                    self.vel = 8

                if self.rect.top < 0:
                    self.rect.top = 0
                    self.vel = 0
                if self.rect.bottom > screen_height:
                    self.rect.bottom = screen_height
                    self.vel = 0

                if self.rect.colliderect(ground_rect):
                    self.vel = 0
                    self.rect.y = ground_rect.top - self.rect.height
                    self.alive = False

                keys = pygame.key.get_pressed()
                if keys[pygame.K_UP] and not self.clicked:
                    self.clicked = True
                    self.vel = -10
                if not keys[pygame.K_UP]:
                    self.clicked = False

                self.rect.y += int(self.vel)

                self.counter += 1

                if self.counter > self.flap_cooldown:
                    self.counter = 0
                    self.index += 1
                    if self.index >= len(self.images):
                        self.index = 0
                    self.image = self.images[self.index]
        else:
            self.rect.centery = int(screen_height/2)

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/pipe.png')
        self.rect = self.image.get_rect()
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - (pipe_gap / 2)]
        if position == -1:
            self.rect.topleft = [x, y + (pipe_gap / 2)]

    def update(self):
        self.rect.x -= scroll_speed

def create_pipe():
    random_pipe_pos = random.choice([-1, 1])
    top_pipe = Pipe(screen_width, int(screen_height / 2), random_pipe_pos)
    bottom_pipe = Pipe(screen_width, int(screen_height / 2), random_pipe_pos * -1)
    return top_pipe, bottom_pipe

bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()

flappy = Bird(100, int(screen_height/2))
bird_group.add(flappy)

ground_rect = ground_img.get_rect()
ground_rect.topleft = (0, screen_height - new_ground_height)

run = True

while run:

    clock.tick(fps)
    screen.blit(bg, (0, 0))

    bird_group.draw(screen)
    bird_group.update()
    pipe_group.draw(screen)
    pipe_group.update()

    screen.blit(ground_img, (ground_scroll, screen_height - new_ground_height))

    ground_scroll -= scroll_speed
    if abs(ground_scroll) > 35:
        ground_scroll = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    if not flappy.started and keys[pygame.K_RETURN]:
        flappy.started = True
        flappy.alive = True

        if flappy.started and flappy.alive:
            if pygame.sprite.spritecollide(flappy, pipe_group, False):
                flappy.alive = False
            


    if not flappy.alive:
        font = pygame.font.Font(None, 36)
        text = font.render("Game Over. Press R to Restart", True, (255, 255, 255))
        text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2))
        screen.blit(text, text_rect)

        if keys[pygame.K_r]:
            flappy.started = False
            flappy.alive = True
            flappy.rect.center = (100, int(screen_height/2))
            flappy.vel = 0
            pipe_group.empty()  # Clear all existing pipes
            last_pipe = pygame.time.get_ticks()

    if not flappy.started:
        font = pygame.font.Font(None, 36)
        text = font.render("Press Enter to Start", True, (255, 255, 255))
        text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2))
        screen.blit(text, text_rect)

    
    if flappy.started and flappy.alive:
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_frequency:
            top_pipe, bottom_pipe = create_pipe()
            pipe_group.add(top_pipe)
            pipe_group.add(bottom_pipe)
            last_pipe = time_now

    
    for pipe in pipe_group.copy():
        if pipe.rect.right < 0:
            pipe_group.remove(pipe)

    if flappy.started and flappy.alive:
        if pygame.sprite.spritecollide(flappy, pipe_group, False):
            flappy.alive = False


    pygame.display.update()

pygame.quit()