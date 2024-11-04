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
            self.all_objects.update(dt)

            # draw the game
            self.display_surface.blit(self.bg, (0,0))
            self.all_objects.draw(self.display_surface)
           
            pygame.display.update()
        pygame.quit()

Clock = pygame.time.Clock()

if __name__ == '__main__':
    game = Game()
    game.run()