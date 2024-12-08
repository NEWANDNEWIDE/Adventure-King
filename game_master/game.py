from __future__ import annotations
import sys
import pygame
import map.HWmap
import settings
from game_master import fileManager


class Game:
    FONT: pygame.font.Font = None

    def __init__(self, edit=False):
        if edit:
            Game.FONT = pygame.font.SysFont('microsoftyaheiui', 16)
        else:
            pygame.init()
            Game.FONT = pygame.font.SysFont('microsoftyaheiui', 16)
            self.__running = True
            self.screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
            pygame.display.set_caption(settings.TITLE)
            self.__init()
            self.clock = pygame.time.Clock()
            self.map = map.HWmap.Map(self.screen)

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
            dt = self.clock.tick() / 1000
            self.screen.fill((255, 255, 255))
            for event in pygame.event.get():
                """print(event)"""
                if event.type == pygame.QUIT:
                    self.__running = False
                    pygame.quit()
                    sys.exit()
                self.map.event_update(event)
            self.map.update(dt)
            self.map.render()
            pygame.display.update()
        pygame.quit()
        sys.exit()
