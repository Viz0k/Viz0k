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
        bg = pygame.image.load(join('UpperCut','graphics','background','boxing ring.png')).convert_alpha()

    def run(self):
        running = True
        while running:
            dt = Clock.tick(60) /1000
            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            x_speed = round(pygame.joystick.Joystick(0).get_axis(0))
            if x_speed == 1:
                self.Blue_direction.x = 2
            elif x_speed == -1:
                self.Blue_direction.x = -2
            else:
                self.Blue_direction.x = 0
            
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a]:
                self.Red_direction.x = -2
            elif keys[pygame.K_d]:
                self.Red_direction.x = 2
            else:
                self.Red_direction.x = 0

            # draw the game
            self.display_surface.blit(self.bg, (0,0))

            #player movement
            self.Blue_rect.center += self.Blue_direction * Blue_speed * dt
            if self.Blue_rect.right > self.Red_rect.left:
                self.Blue_rect.right = self.Red_rect.left
            elif self.Blue_rect.left < 150:
                self.Blue_rect.left = 150
            self.display_surface.blit(self.PBlue, self.Blue_rect)

            self.Red_rect.center += self.Red_direction * Red_speed * dt
            if self.Red_rect.left < self.Blue_rect.right:
                self.Red_rect.left = self.Blue_rect.right
            elif self.Red_rect.right > (window_width - 130):
                self.Red_rect.right = (window_width - 130)
                
            self.display_surface.blit(self.PRed, self.Red_rect)
            
            pygame.display.update()
        pygame.quit()

Clock = pygame.time.Clock()

if __name__ == '__main__':
    game = Game()
    game.run()