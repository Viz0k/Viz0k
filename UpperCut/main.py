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

        # sprite group setup
        self.all_objects = pygame.sprite.Group()

        # instantiate player objects
        self.red  = Player(self.all_objects, "red", (1000, 460))
        self.blue = Player(self.all_objects, "blue", (150, 460))

    def create_bg(self):
        bg = pygame.image.load(join('UpperCut','graphics','background','boxing ring.png')).convert_alpha()
        return bg

    def health_display(self):
        # Define font and size
        font = pygame.font.Font(None, 36)

        # Create the text surfaces for red and blue health
        red_label = font.render("Red Health:", True, (255, 255, 255))
        red_health = font.render(str(self.red.health), True, (255, 255, 255))
        blue_label = font.render("Blue Health:", True, (255, 255, 255))
        blue_health = font.render(str(self.blue.health), True, (255, 255, 255))

        # Display red and blue health text in the top corners
        self.display_surface.blit(red_label, (window_width - 150, 10))
        self.display_surface.blit(red_health, (window_width - 150, 40))
        self.display_surface.blit(blue_label, (20, 10))
        self.display_surface.blit(blue_health, (20, 40))

    def run(self):
        running = True
        last_time = time.time()
        while running:
            
            # delta time
            dt = time.time() - last_time
            last_time = time.time()

            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # update the game
            self.all_objects.update(dt, self.red, self.blue)

            # draw the game
            self.display_surface.blit(self.bg, (0,0))
            self.health_display()
            self.all_objects.draw(self.display_surface)
           
            pygame.display.update()
        pygame.quit()

Clock = pygame.time.Clock()

if __name__ == '__main__':
    game = Game()
    game.run()