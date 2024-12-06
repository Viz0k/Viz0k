import pygame, sys, time
from settings import *
from os.path import join
from Playerscopy import Player

pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

class Game:
    def __init__(self):

        # general setup
        pygame.init()
        self.display_surface = pygame.display.set_mode((window_width, window_height))
        pygame.display.set_caption('UPPERCUT')

        #background
        self.bg = self.create_bg()

        # font
        self.font = pygame.font.Font(None, 36)

        # sprite group setup
        self.all_objects = pygame.sprite.Group()

        # instantiate player objects
        self.red  = Player(self.all_objects, "red", (1000, 460))
        self.blue = Player(self.all_objects, "blue", (150, 460))

        # Match start time
        self.start_time = pygame.time.get_ticks()

    def create_bg(self):
        bg = pygame.image.load(join('UpperCut','graphics','background','boxing ring.png')).convert_alpha()
        return bg

    def health_display(self):
        # Create the text surfaces for red and blue health
        red_label = self.font.render("Red Health:", True, (255, 255, 255))
        red_health = self.font.render(str(self.red.health), True, (255, 255, 255))
        blue_label = self.font.render("Blue Health:", True, (255, 255, 255))
        blue_health = self.font.render(str(self.blue.health), True, (255, 255, 255))

        # Display red and blue health text in the top corners
        self.display_surface.blit(red_label, (window_width - 150, 10))
        self.display_surface.blit(red_health, (window_width - 150, 40))
        self.display_surface.blit(blue_label, (20, 10))
        self.display_surface.blit(blue_health, (20, 40))
    
    def restart(self):
        # Display restart message
        restart_text = self.font.render("Press 'R' to restart", True, (225, 225, 225))

        if self.blue.health == 0 or self.red.health == 0:
            self.display_surface.blit(restart_text, (window_width / 2 - 100, 60))
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                # Reset both players
                self.red.reset((1000, 460))  
                self.blue.reset((150, 460))  

    def timer(self, start_time):
        # Calculate elapsed time in seconds
        elapsed_time = int((pygame.time.get_ticks() - start_time) / 1000)
        timer_text = self.font.render(f"Time: {elapsed_time}s", True, (255, 255, 255))
        return timer_text

    def run(self):
        running = True
        last_time = time.time()
        
        while running:
            # Delta time
            dt = time.time() - last_time
            last_time = time.time()

            # Event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Update the game
            self.all_objects.update(dt, self.red, self.blue)

            # Draw the game
            self.display_surface.blit(self.bg, (0, 0))

            # Update and display the timer
            timer_text = self.timer(self.start_time)
            if self.red.health == 0 or self.blue.health == 0:
                self.display_surface.blit
            else:
                self.display_surface.blit(timer_text, (window_width / 2 - 50, 20))

            self.health_display()
            self.restart()
            self.all_objects.draw(self.display_surface)

            pygame.display.update()
        pygame.quit()


Clock = pygame.time.Clock()

if __name__ == '__main__':
    game = Game()
    game.run()