import pygame
from settings import *
from os.path import join

class Player(pygame.sprite.Sprite):
    def __init___(self,groups):
        super().__init__(groups)

        #player images
        self.PRed = pygame.image.load(join('UpperCut','graphics', 'players', 'red corner.png')).convert_alpha()
        self.PBlue = pygame.image.load(join('UpperCut','graphics', 'players', 'blue corner.png')).convert_alpha()

        # player rects
        self.Red_rect = self.PRed.get_frect(topleft = (1000, 460))
        self.Blue_rect = self.PBlue.get_frect(topleft = (150, 460))

        # player direction
        self.Blue_speed = 150
        self.Red_speed = 150
        self.Blue_direction = pygame.math.Vector2(0, 0)
        self.Red_direction = pygame.math.Vector2(0, 0)