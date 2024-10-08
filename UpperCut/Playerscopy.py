import pygame
from settings import *
from os.path import join

class Player(pygame.sprite.Sprite):
    def __init__(self, groups, colour, pos):
        super().__init__(groups)

        self.image = pygame.image.load(join('UpperCut', 'graphics', 'players', colour + ' corner.png')).convert_alpha()
        self.rect = self.image.get_frect(topleft=pos)  
        self.direction = pygame.math.Vector2(0, 0)
        self.pos = pygame.math.Vector2(self.rect.topleft)  
        self.speed = 150
        self.colour = colour

    def update(self, dt):
        keys = pygame.key.get_pressed()

        if self.colour == "red":
            if keys[pygame.K_a]:
                self.direction.x = -1
            elif keys[pygame.K_d]:
                self.direction.x = 1
            else:
                self.direction.x = 0
        
        if self.colour == "blue":
            x_speed = round(pygame.joystick.Joystick(0).get_axis(0))
            if x_speed == 1:
                self.direction.x = 1
            elif x_speed == -1:
                self.direction.x = -1
            else:
                self.direction.x = 0

        self.pos.x += self.direction.x * self.speed * dt
        self.rect.x = self.pos.x

        self.boundaries()

    def boundaries(self):
        # Red player limits
        if self.colour == "red":
            if self.rect.right > (window_width - 130):
                self.rect.right = (window_width - 130)

        # Blue player limits
        if self.colour == "blue":
            if self.rect.left < 150:
                self.rect.left = 150
