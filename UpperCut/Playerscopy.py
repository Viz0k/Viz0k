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

        self.animation_speed = 5 
        self.damage_taken = False 
        self.jab_attack_cooldown = 450
        self.UC_attack_cooldown = 1500
        self.last_jab_time = 0
        self.last_UC_time = 0  

        self.Ucolour = self.colour[0].upper()
        self.CW = self.create_graphics("CW")
        self.CJ = self.create_graphics("CJ")
        self.CU = self.create_graphics("CU")
        self.current = self.CW
        self.index = 0

        self.action = "stand" # initial action
        self.previous_action = "stand"
        self.index = 0

        self.round = 1
        self.score = 0

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

        self.health_regen()
        self.boundaries(red, blue)
        self.input()
        self.collisions(red, blue)
        if self.action != "stand":
            self.animate(dt)

        self.pos.x += self.direction.x * self.speed * dt
        self.rect.x = self.pos.x

    def boundaries(self, red, blue):
        if self.colour == "red":
            if self.rect.right > (window_width - 130):
                self.rect.right = (window_width - 130)
                self.pos.x = self.rect.x
            elif self.rect.left < blue.rect.right - 10:  # Allow slight overlap
                self.rect.left = blue.rect.right - 10
                self.pos.x = self.rect.x

        if self.colour == "blue":
            if self.rect.left < 150:
                self.rect.left = 150
                self.pos.x = self.rect.x
            elif self.rect.right > red.rect.left + 10:  # Allow slight overlap
                self.rect.right = red.rect.left + 10
                self.pos.x = self.rect.x

    def collisions(self, red, blue):
        # Check collisions and apply damage based on the attacking player's state
        if self.colour == 'red' and self.rect.colliderect(blue.rect):
            if self.action == 'jab' and self.punch:
                blue.health -= 10
                red.score += 100
                self.punch = False
                self.damage_taken = True
            elif self.action == 'uppercut' and self.punch:
                blue.health -= 20
                red.score += 150
                self.punch = False
                self.damage_taken = True
        elif self.colour == 'blue' and self.rect.colliderect(red.rect):
            if self.action == 'jab' and self.punch:
                red.health -= 10
                blue.score += 100
                self.punch = False
                self.damage_taken = True
            elif self.action == 'uppercut' and self.punch:
                red.health -= 20
                blue.score += 150
                self.punch = False
                self.damage_taken = True

    def animate(self, dt):
        if self.action in attacks and self.index == 0:
            self.punch = True
        if self.index > 0:
            self.punch = False

        # Adjust animation speed using delta time
        self.index += self.animation_speed * dt

        if self.index >= len(self.current):
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

            # Handle jab with separate cooldown
            if current_time - self.last_jab_time > self.jab_attack_cooldown:
                if keys[pygame.K_j]:  # Jab - red
                    if self.action not in attacks:  # Only execute jab if not already attacking
                        self.previous_action = self.action
                        self.action = "jab"
                        self.current = self.CJ
                        self.index = 0
                        self.last_jab_time = current_time  # Update jab timer

            # Handle uppercut with separate cooldown
            if current_time - self.last_UC_time > self.UC_attack_cooldown:
                if keys[pygame.K_u]:  # Uppercut - red
                    if self.action not in attacks:  # Only execute uppercut if not already attacking
                        self.previous_action = self.action
                        self.action = "uppercut"
                        self.current = self.CU
                        self.index = 0
                        self.last_UC_time = current_time  # Update uppercut timer

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

            # Handle jab with separate cooldown
            if current_time - self.last_jab_time > self.jab_attack_cooldown:
                if pygame.joystick.Joystick(0).get_button(0):  # Jab
                    if self.action not in attacks:  # Only execute jab if not already attacking
                        self.previous_action = self.action
                        self.action = "jab"
                        self.current = self.CJ
                        self.index = 0
                        self.last_jab_time = current_time  # Update jab timer

            # Handle uppercut with separate cooldown
            if current_time - self.last_UC_time > self.UC_attack_cooldown:
                if pygame.joystick.Joystick(0).get_button(1):  # Uppercut
                    if self.action not in attacks:  # Only execute uppercut if not already attacking
                        self.previous_action = self.action
                        self.action = "uppercut"
                        self.current = self.CU
                        self.index = 0
                        self.last_UC_time = current_time  # Update uppercut timer

    def deaths(self):
        if self.health <= 0:
            # print(self.colour, 'has died')
            self.image = self.death  
            self.action = "dead"    
            self.direction.x = 0 # stops the player from moving after theyve died 
            self.health = 0 # stops the health from going into negative numbers after death
            self.rect = self.image.get_frect(midbottom=self.rect.midbottom)

    def reset(self, position):
        self.health = 100  
        self.pos = pygame.math.Vector2(position)  
        self.rect.topleft = position  
        self.image = self.stand  
        self.action = "stand"  
        self.direction = pygame.math.Vector2(0, 0)  
        self.index = 0  
        self.punch = False
        self.round += 1

    def health_regen(self):
        current_time = pygame.time.get_ticks()
        last_heal = 0
        last_regen = 0
        heal_timer = 3000
        regen_timer = 1000

        if self.damage_taken:
            print('damage taken')
            self.damage_taken = False
            if current_time - last_heal > heal_timer and self.health <= 0 and self.health >= 100:
                print('healing timer started')
                if not self.damage_taken:
                    print('still no damage')
                    if current_time - last_regen > regen_timer:
                        print('waiting second to heal')
                        self.health += 10
