from __future__ import annotations
import sys
import pygame
import settings
from game_master import level, fileManager


class Game:
    FONT: pygame.font.Font = None

    def __init__(self):
        pygame.init()
        Game.FONT = pygame.font.SysFont('microsoftyaheiui', 16)
        self.__running = True
        self.screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
        pygame.display.set_caption(settings.TITLE)
        self.__init()
        self.clock = pygame.time.Clock()
        self.level = level.Level(self.screen)

    def __init(self):
        pygame.key.stop_text_input()
        fileManager.loading_item()
        fileManager.loading_game_surfaces()

    def __event(self, event):
        pass

    @property
    def running(self):
        return self.__running

    @running.setter
    def running(self, running):
        self.__running = running

    def run(self):
        while self.__running:
            event: pygame.event.Event | None = None
            self.screen.fill((255, 255, 255))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.__running = False
                    pygame.quit()
                    sys.exit()

            pygame.display.update()
            self.clock.tick(settings.FPS)

        pygame.quit()
        sys.exit()
