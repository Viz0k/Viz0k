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
        self.death = pygame.image.load(join('UpperCut', 'graphics', 'players', colour + ' death.png')).convert_alpha()

        self.image = self.stand
        self.rect = self.image.get_frect(topleft=pos)  
        self.direction = pygame.math.Vector2(0, 0)
        self.pos = pygame.math.Vector2(self.rect.topleft)  
        self.speed = 300
        self.colour = colour
        self.punch = False # detects if the character is punching to take away health
        self.health = 100

        self.animation_speed = 5 # chooses how fast the animation plays
        self.button_pressed = False # stops attacks from playing more than once
        self.attack_cooldown = 500  # Cooldown duration in milliseconds
        self.last_attack_time = 0   # Tracks the last time an attack was executed

        self.Ucolour = self.colour[0].upper()
        self.CW = self.create_graphics("CW")
        self.CJ = self.create_graphics("CJ")
        self.CU = self.create_graphics("CU")
        self.current = self.CW
        self.index = 0

        self.action = "stand" # initial action
        self.previous_action = "stand"
        self.index = 0

    def create_graphics(self, type):
        # adds all of the graphics and returns them as a array
        tempsurf1 = pygame.image.load(join('UpperCut', 'graphics', 'players', self.Ucolour + type + '1.png')).convert_alpha()
        tempsurf2 = pygame.image.load(join('UpperCut', 'graphics', 'players', self.Ucolour + type + '2.png')).convert_alpha()
        tempsurf3 = pygame.image.load(join('UpperCut', 'graphics', 'players', self.Ucolour + type + '3.png')).convert_alpha()
        return [tempsurf1, tempsurf2, tempsurf3]

    def update(self, dt, red, blue):
        self.deaths()  # Check if the player is dead
        if self.action == "dead":
            return  # Skip further updates if the player is dead

        self.boundaries(red, blue)
        self.input()
        self.collisions(red, blue)
        if self.action != "stand":
            self.animate(dt)

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
                blue.health -= 10
            elif blue.action in attacks and self.colour == 'blue' and blue.punch is True:
                red.health -= 10      

    def animate(self, dt):
        if self.action in attacks and self.index == 0:
            self.punch = True
        if self.index > 0:
            self.punch = False

        # Adjust animation speed using delta time
        self.index += self.animation_speed * dt

        if self.index >= len(self.current):  # Animation finished
            self.index = 0
            if self.action in attacks:
                # Reset the action after the attack animation completes
                self.previous_action, self.action = self.action, "stand"
                self.current = self.CW  # Set the default image for standing

        self.image = self.current[int(self.index)]
        self.rect = self.image.get_frect(topleft=self.pos)

    def input(self):
        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()

        if self.colour == "red":
            # Handle movement
            if keys[pygame.K_a] or keys[pygame.K_d]:
                self.direction.x = -1 if keys[pygame.K_a] else 1
                if self.action != "walk" and self.action == "stand":
                    self.previous_action = self.action
                    self.action = "walk"
                    self.current = self.CW
            else:
                self.direction.x = 0
                if self.action == "walk":
                    self.previous_action = self.action
                    self.action = "stand"
                    self.image = self.stand
                    self.index = 0

            # Handle attacks with cooldown
            if current_time - self.last_attack_time > self.attack_cooldown:
                if keys[pygame.K_j] and not self.button_pressed:  # Jab
                    self.button_pressed = True
                    self.previous_action = self.action
                    self.action = "jab"
                    self.current = self.CJ
                    self.index = 0
                    self.last_attack_time = current_time  # Update last attack time
                elif keys[pygame.K_u] and not self.button_pressed:  # Uppercut
                    self.button_pressed = True
                    self.previous_action = self.action
                    self.action = "uppercut"
                    self.current = self.CU
                    self.index = 0
                    self.last_attack_time = current_time  # Update last attack time

            # Reset button_pressed when attack keys are released
            if not keys[pygame.K_j] and not keys[pygame.K_u]:
                self.button_pressed = False

        if self.colour == "blue":
            # Handle movement
            x_speed = round(pygame.joystick.Joystick(0).get_axis(0))
            if x_speed == 1 or x_speed == -1:
                self.direction.x = x_speed
                if self.action != "walk" and self.action == "stand":
                    self.previous_action = self.action
                    self.action = "walk"
                    self.current = self.CW
            else:
                self.direction.x = 0
                if self.action == "walk":
                    self.previous_action = self.action
                    self.action = "stand"
                    self.image = self.stand
                    self.index = 0

            # Handle attacks with cooldown
            if current_time - self.last_attack_time > self.attack_cooldown:
                if pygame.joystick.Joystick(0).get_button(0) and not self.button_pressed:  # Jab
                    self.button_pressed = True
                    self.previous_action = self.action
                    self.action = "jab"
                    self.current = self.CJ
                    self.index = 0
                    self.last_attack_time = current_time  # Update last attack time
                elif pygame.joystick.Joystick(0).get_button(1) and not self.button_pressed:  # Uppercut
                    self.button_pressed = True
                    self.previous_action = self.action
                    self.action = "uppercut"
                    self.current = self.CU
                    self.index = 0
                    self.last_attack_time = current_time  # Update last attack time

            # Reset button_pressed when attack keys are released
            if not pygame.joystick.Joystick(0).get_button(0) and not pygame.joystick.Joystick(0).get_button(1):
                self.button_pressed = False

    def deaths(self):
        if self.health <= 0:
            # print(self.colour, 'has died')
            self.image = self.death  
            self.action = "dead"    
            self.direction.x = 0    
