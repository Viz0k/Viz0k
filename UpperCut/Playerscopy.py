import pygame
from settings import *
from os.path import join

attacks = ['jab', 'uppercut']

class Player(pygame.sprite.Sprite):
    # The Player class handles the actions and interactions of the boxing game characters.
    # It includes movement, collisions, animations, and health tracking.
    def __init__(self, groups, colour, pos):
        super().__init__(groups)

        self.stand = pygame.image.load(join('UpperCut', 'graphics', 'players', colour + ' corner.png')).convert_alpha()
        self.image = self.stand
        self.rect = self.image.get_frect(topleft=pos)  
        self.direction = pygame.math.Vector2(0, 0)
        self.pos = pygame.math.Vector2(self.rect.topleft)  
        self.speed = 300
        self.colour = colour
        self.punch = False
        self.health = 100

        self.current_ani = []

        self.Ucolour = self.colour[0].upper()
        self.CW = self.create_graphics("CW")
        self.CJ = self.create_graphics("CJ")
        self.CU = self.create_graphics("CU")
        self.current = self.CW
        self.index = 0

        self.action = "stand"
        self.previous_action = "stand"
        self.index = 0

    def create_graphics(self, type):
        # adds all of the graphics and returns them as a array
        tempsurf1 = pygame.image.load(join('UpperCut', 'graphics', 'players', self.Ucolour + type + '1.png')).convert_alpha()
        tempsurf2 = pygame.image.load(join('UpperCut', 'graphics', 'players', self.Ucolour + type + '2.png')).convert_alpha()
        tempsurf3 = pygame.image.load(join('UpperCut', 'graphics', 'players', self.Ucolour + type + '3.png')).convert_alpha()
        return [tempsurf1, tempsurf2, tempsurf3]

    def update(self, dt, red, blue):
        self.boundaries(red, blue)
        self.input()
        self.collisions(red, blue)
        if self.action != "stand":
            self.animate()

        self.pos.x += self.direction.x * self.speed * dt
        self.rect.x = self.pos.x

    def boundaries(self, red, blue):
        # stops plays from leaving the boundaries of the ring and going past eachother
        if self.colour == "red":
            if self.rect.right > (window_width - 130):
                self.rect.right = (window_width - 130)
                self.pos.x = self.rect.x
            elif self.rect.left <= blue.rect.right:
                self.rect.left = blue.rect.right
                self.pos.x = self.rect.x

        if self.colour == "blue":
            if self.rect.left < 150:
                self.rect.left = 150
                self.pos.x = self.rect.x
            elif self.rect.right >= red.rect.left:
                self.rect.right = red.rect.left
                self.pos.x = self.rect.x

    def collisions(self, red, blue):
        # does all of the player attacks and collisions while making them only take damage when its a specific frame
        if self.rect.colliderect(self.rect):
            if red.action in attacks and self.colour == 'red' and red.punch is True:
                print('-10')
                blue.health -= 10
                print("blue health is: ", blue.health)
            elif blue.action in attacks and self.colour == 'blue' and blue.punch is True:
                print('-10')
                red.health -= 10
                print("red health is: ", red.health)       

    def animate(self):
        # function to animate the player objects to make the game smoother and more fluent
        if self.action in attacks and self.index == 0:
            self.punch = True
        if self.index > 0:
            self.punch = False
        self.index += 0.01
        if self.index >= len(self.current):
            self.index = 0
            if self.action in attacks:
                self.previous_action, self.action = self.action, self.previous_action

        self.image = self.current[int(self.index)]
        self.rect = self.image.get_frect(topleft=self.pos)

    def input(self):
        # gets player inputs from both controller and keyboard adn converts them into viewable actions 
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
                self.index = 0

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
