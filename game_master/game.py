import sys
import pygame
import settings
from game_master import level
from game_master import fileManager


class Game:
    def __init__(self):
        pygame.init()
        self.FONT = pygame.font.SysFont('microsoftyaheimicrosoftyaheiui', 16)
        self.__game_speed = 100
        self.__running = True
        self.screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
        pygame.display.set_caption(settings.TITLE)
        self.init()
        self.clock = pygame.time.Clock()
        self.level = level.Level(self.screen)

    def init(self):
        fileManager.loading_item()
        fileManager.loading_game_surfaces()

    def item(self):
        pass

    def game(self):
        pass

    @property
    def game_speed(self):
        return self.__game_speed

    @game_speed.setter
    def game_speed(self, game_speed):
        self.__game_speed = game_speed

    def run(self):
        while self.__running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.__running = False
                    pygame.quit()
                    sys.exit()

            self.screen.fill((255, 255, 255))

            pygame.display.update()
            self.clock.tick(settings.FPS)

        self.__running = False
        pygame.quit()
        sys.exit()

    @property
    def running(self):
        return self.__running

    @running.setter
    def running(self, running):
        self.__running = running