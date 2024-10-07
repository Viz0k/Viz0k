import pygame
from settings import *
from os.path import join
from Players import Player

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

        self.player = Player(self.all_objects)

    def create_bg(self):
        bg = pygame.image.load(join('UpperCut','graphics','background','boxing ring.png')).convert_alpha()
        return bg

    def run(self):
        running = True
        while running:
            dt = Clock.tick(60) /1000
            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # draw the game
            self.display_surface.blit(self.bg, (0,0))
            self.all_objects.draw(self.display_surface)

            # update the game
            self.all_objects.update(dt)

            
            pygame.display.update()
        pygame.quit()

Clock = pygame.time.Clock()

if __name__ == '__main__':
    game = Game()
    game.run()