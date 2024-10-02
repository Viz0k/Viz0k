import pygame
from settings import *
from os.path import join

x = 150
x1 = 1000
Blue_direction = pygame.math.Vector2(0, 0)
Red_direction = pygame.math.Vector2(0, 0)

#general setup
pygame.init()
display_surface = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('UPPERCUT')
running = True
Clock = pygame.time.Clock()

#background
bg = pygame.image.load(join('graphics','background','boxing ring.png')).convert_alpha()

#player images
PRed = pygame.image.load(join('graphics', 'players', 'red corner.png')).convert_alpha()
PBlue = pygame.image.load(join('graphics', 'players', 'blue corner.png')).convert_alpha()

#player rects
Red_rect = PRed.get_frect(topleft = (x1, 460))
Blue_rect = PBlue.get_frect(topleft = (x, 460))
Blue_speed = 150
Red_speed = 150

while running:
    dt = Clock.tick(60) /1000
    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
        #     Red_direction.x = -2
        # else:
        #     Red_direction.x = 0
        # if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
        #     Blue_direction.x = 2
        # else:
        #     Blue_direction.x = 0

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        Red_direction.x = -2
    elif keys[pygame.K_d]:
        Red_direction.x = 2
    else:
        Red_direction.x = 0

    # draw the game
    display_surface.blit(bg, (0,0))

    #player movement
    Blue_rect.center += Blue_direction * Blue_speed * dt
    if Blue_rect.right > Red_rect.left:
        Blue_rect.right = Red_rect.left
    elif Blue_rect.left < 150:
        Blue_rect.left = 150
    display_surface.blit(PBlue, Blue_rect)

    Red_rect.center += Red_direction * Red_speed * dt
    if Red_rect.left < Blue_rect.right:
        Red_rect.left = Blue_rect.right
    elif Red_rect.right > (window_width - 130):
        Red_rect.right = (window_width - 130)
        
    display_surface.blit(PRed, Red_rect)
    
    pygame.display.update()

pygame.quit()