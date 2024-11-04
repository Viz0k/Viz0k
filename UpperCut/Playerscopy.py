import pygame
from settings import *
from os.path import join

class Player(pygame.sprite.Sprite):
    def __init__(self, groups, colour, pos):
        super().__init__(groups)

        
        self.stand = pygame.image.load(join('UpperCut', 'graphics', 'players', colour + ' corner.png')).convert_alpha()
        self.image = self.stand
        self.rect = self.image.get_frect(topleft = pos)  
        self.direction = pygame.math.Vector2(0, 0)
        self.pos = pygame.math.Vector2(self.rect.topleft)  
        self.speed = 300
        self.colour = colour
        self.punch = False

        self.current_ani = []

        self.Ucolour = self.colour[0].upper()
        self.CW = self.create_graphics("CW")
        self.CJ = self.create_graphics("CJ")
        self.CU = self.create_graphics("CU")
        self.current = self.CW
        self.index = 0
        #self.walk = self.CW[self.CW_index]

        self.action = "stand"
        self.previous_action = "stand"
        self.index = 0

        # self.red_animation = []
        # self.red_animation_index = 0

    def create_graphics(self, type):
        
        tempsurf1 = pygame.image.load(join('UpperCut', 'graphics', 'players', self.Ucolour + type +'1.png')).convert_alpha()
        tempsurf2 = pygame.image.load(join('UpperCut', 'graphics', 'players', self.Ucolour + type +'2.png')).convert_alpha()
        tempsurf3 = pygame.image.load(join('UpperCut', 'graphics', 'players', self.Ucolour + type +'3.png')).convert_alpha()
        
        return [tempsurf1, tempsurf2, tempsurf3]

    def update(self, dt):
        self.boundaries()
        self.input()
        if self.action != "stand": self.animate()

        self.pos.x += self.direction.x * self.speed * dt
        self.rect.x = self.pos.x

    def boundaries(self):
        # Red player limits
        if self.colour == "red":
            
            if self.rect.right > (window_width - 130):
                self.rect.right = (window_width - 130)
                self.pos.x = self.rect.x

        # Blue player limits
        if self.colour == "blue":
            if self.rect.left < 150:
                self.rect.left = 150
                self.pos.x = self.rect.x

    def animate(self):
        self.index = self.index + 0.01
        if self.index >= len(self.current):
            self.index = 0
            if self.action in ["jab", "uppercut"]:
                self.previous_action, self.action = self.action, self.previous_action

        self.image = self.current[int(self.index)]
        self.rect = self.image.get_frect(topleft = self.pos)
        
    def input(self):
        keys = pygame.key.get_pressed()
        x_speed = round(pygame.joystick.Joystick(0).get_axis(0))

        if self.colour == "red":
            if keys[pygame.K_a] or keys[pygame.K_d]:
                self.previous_action = self.action
                self.action = "walk"
                self.current = self.CW
                if keys[pygame.K_a]: 
                    self.direction.x = -1
                else:
                    self.direction.x = 1
                
            elif keys[pygame.K_j]:
                self.previous_action = self.action
                self.action = "jab"
                self.current = self.CJ

            elif keys[pygame.K_u]:
                self.previous_action = self.action
                self.action = "uppercut"
                self.current = self.CU   
            
            else:
                self.direction.x = 0
                self.previous_action = self.action
                self.action = "stand"
                self.image = self.stand
        
        if self.colour == "blue":
            if x_speed == 1 or x_speed == -1:
                self.previous_action = self.action
                self.action = "walk"
                self.current = self.CW
                if x_speed == 1: 
                    self.direction.x = 1
                else:
                    self.direction.x = -1
                
            elif pygame.joystick.Joystick(0).get_button(0):
                self.previous_action = self.action
                self.action = "jab"
                self.current = self.CJ
            elif pygame.joystick.Joystick(0).get_button(1):
                self.previous_action = self.action
                self.action = "uppercut"
                self.current = self.CU 

            else:
                self.direction.x = 0
                self.previous_action = self.action
                self.action = "stand"
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