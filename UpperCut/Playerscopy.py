import pygame
from settings import *
from os.path import join

class Player(pygame.sprite.Sprite):
    def __init__(self, groups, colour, pos):
        super().__init__(groups)

        self.image = pygame.image.load(join('UpperCut', 'graphics', 'players', colour + ' corner.png')).convert_alpha()
        self.stand = pygame.image.load(join('UpperCut', 'graphics', 'players', colour + ' corner.png')).convert_alpha()
        self.rect = self.image.get_frect(topleft = pos)  
        self.direction = pygame.math.Vector2(0, 0)
        self.pos = pygame.math.Vector2(self.rect.topleft)  
        self.speed = 300
        self.colour = colour
        self.punch = False

        self.current_ani = []

        self.Ucolour = self.colour[0].upper()
        self.CW1 = pygame.image.load(join('UpperCut', 'graphics', 'players', self.Ucolour + 'CW1.png')).convert_alpha()
        self.CW2 = pygame.image.load(join('UpperCut', 'graphics', 'players', self.Ucolour + 'CW2.png')).convert_alpha()
        self.CW = [self.CW1, self.CW2]
        self.CW_index = 0

        self.CJ1 = pygame.image.load(join('UpperCut', 'graphics', 'players', self.Ucolour + 'CJ1.png')).convert_alpha()
        self.CJ2 = pygame.image.load(join('UpperCut', 'graphics', 'players', self.Ucolour + 'CJ2.png')).convert_alpha()
        self.CJ = [self.CJ1, self.CJ2, self.stand]
        self.CJ_index = 0

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
                self.walk()
            elif keys[pygame.K_d]:
                self.direction.x = 1
                self.walk()
            elif keys[pygame.K_e] and not self.punch:
                print('e pressed')
                self.punch = True
                self.jab()
                # self.jab()
                # if self.CJ_index >= len(self.CJ):
                #     self.CJ_index = 0
            else:
                self.direction.x = 0
                self.image = self.stand
        
        if self.colour == "blue":
            x_speed = round(pygame.joystick.Joystick(0).get_axis(0))
            if x_speed == 1:
                self.direction.x = 1
                self.walk()
            elif x_speed == -1:
                self.direction.x = -1
                self.walk()
            else:
                self.direction.x = 0
                self.image = self.stand

    def walk(self):
        self.CW_index = self.CW_index + 0.03
        if self.CW_index >= len(self.CW):
            self.CW_index = 0
        self.image = self.CW[int(self.CW_index)]
    
    def jab(self):
        # for item in self.CJ:
        #     self.current_ani.append(item)
        # for i in self.current_ani:
        #     self.image = self.current_ani

        while self.punch == True:
            self.CJ_index = self.CJ_index + 0.01
            if self.CJ_index < len(self.CJ):
                self.image = self.CJ[int(self.CJ_index)]
            elif self.CJ_index >= len(self.CJ):
                self.CJ_index = 0
                self.punch = False

        # if self.punch == True:
        #     self.image = self.CJ1
        #     self.image = self.CJ2
        #     self.image = self.stand
        #     self.punch = False