import pygame
from settings import *
from os.path import join

class Player(pygame.sprite.Sprite):
    def __init___(self,groups):
        super().__init__(groups)

        #player images
        self.red_surf = pygame.image.load(join('UpperCut','graphics', 'players', 'red corner.png')).convert_alpha()

        self.RCW1 = pygame.image.load(join('UpperCut','graphics', 'players', 'RCW1.png')).convert_alpha()
        self.RCW2 = pygame.image.load(join('UpperCut','graphics', 'players', 'RCW2.png')).convert_alpha()
        self.RCW = [self.RCW1, self.RCW2]
        self.RCW_index = 0
        self.red_walk = self.RCW[self.RCW_index]

        self.PBlue = pygame.image.load(join('UpperCut','graphics', 'players', 'blue corner.png')).convert_alpha()

        # player rects
        self.Red_rect = self.red_surf.get_frect(topleft = (1000, 460))
        self.Blue_rect = self.PBlue.get_frect(topleft = (150, 460))

        self.display_surface = pygame.display.get_surface()
        self.display_surface.blit(self.red_surf, self.Red_rect)
        self.display_surface.blit(self.PBlue, self.Blue_rect)

        # player position
        self.Blue_direction = pygame.math.Vector2(0, 0)
        self.Red_direction = pygame.math.Vector2(0, 0)
        self.RedPos = pygame.math.Vector2(self.Red_rect.center)
        self.BluePos = pygame.math.Vector2(self.Blue_rect.center)
        self.Blue_speed = 150
        self.Red_speed = 150
    
    def animation(self):
        if self.RCW_index >= len(self.RCW):
            self.RCW_index = 0
        self.red_surf = self.red_walk[int(self.RCW_index)]

    def input(self):

        # red movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.Red_direction.x = -2
        elif keys[pygame.K_d]:
            self.Red_direction.x = 2
        else:
            self.Red_direction.x = 0

        # blue movement
        x_speed = round(pygame.joystick.Joystick(0).get_axis(0))
        if x_speed == 1:
            self.Blue_direction.x = 2
        elif x_speed == -1:
            self.Blue_direction.x = -2
        else:
            self.Blue_direction.x = 0

    def boundaries(self):
        # red limits
        if self.Red_rect.left < self.Blue_rect.right:
            self.Red_rect.left = self.Blue_rect.right
        elif self.Red_rect.right > (window_width - 130):
            self.Red_rect.right = (window_width - 130)

        # blue limits
        if self.Blue_rect.right > self.Red_rect.left:
            self.Blue_rect.right = self.Red_rect.left
        elif self.Blue_rect.left < 150:
            self.Blue_rect.left = 150
    
    def update(self, dt):
        self.input()
        self.boundaries()
        self.animation()

        #player movement
        self.BluePos.x += self.Blue_direction * self.Blue_speed * dt
        self.Blue_rect.x = round(self.BluePos.x)

        self.RedPos.x += self.Red_direction * self.Red_speed * dt
        self.Red_rect.x = round(self.RedPos.x)