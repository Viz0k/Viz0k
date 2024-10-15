import pygame
from settings import *
from os.path import join

class Player(pygame.sprite.Sprite):
    def __init__(self, groups, colour, pos):
        super().__init__(groups)

        self.image = pygame.image.load(join('UpperCut', 'graphics', 'players', colour + ' corner.png')).convert_alpha()
        self.rect = self.image.get_frect(topleft = pos)  
        self.direction = pygame.math.Vector2(0, 0)
        self.pos = pygame.math.Vector2(self.rect.topleft)  
        self.speed = 300
        self.colour = colour

        self.Ucolour = self.colour[0].upper()
        self.CW1 = pygame.image.load(join('UpperCut', 'graphics', 'players', self.Ucolour + 'CW1.png'))
        self.CW2 = pygame.image.load(join('UpperCut', 'graphics', 'players', self.Ucolour + 'CW2.png'))
        self.CW = [self.CW1, self.CW2]
        self.CW_index = 0
        self.walk = self.CW[self.CW_index]


    def update(self, dt):
        self.boundaries()
        self.input()

        self.pos.x += self.direction.x * self.speed * dt
        self.rect.x = self.pos.x

    def boundaries(self):
        # Red player limits
        if self.colour == "red":
            if self.rect.right > (window_width - 130):
                self.rect.right = (window_width - 130)

        # Blue player limits
        if self.colour == "blue":
            if self.rect.left < 150:
                self.rect.left = 150

    def input(self):
        keys = pygame.key.get_pressed()

        if self.colour == "red":
            if keys[pygame.K_a]:
                self.direction.x = -1
                if self.CW_index >= len(self.CW):
                    self.CW_index = 0
                self.image = self.walk[int(self.CW_index)]
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

    def animation(self):
        pass