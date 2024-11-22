from __future__ import annotations
import sys
import pygame
import control.inputField
import settings
from game_master import level


class Game:
    FONT: pygame.font.Font = None

    def __init__(self):
        pygame.init()
        Game.FONT = pygame.font.SysFont('microsoftyaheiui', 16)
        self.__running = True
        self.screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
        pygame.display.set_caption(settings.TITLE)
        self.init()
        self.clock = pygame.time.Clock()
        self.level = level.Level(self.screen)

    def init(self):
        pygame.key.stop_text_input()
        """fileManager.loading_item()
        fileManager.loading_game_surfaces()"""

    def item(self):
        pass

    def game(self):
        pass

    @property
    def running(self):
        return self.__running

    @running.setter
    def running(self, running):
        self.__running = running

    def run(self):
        text = control.inputField.InputField((100, 100), (300, 50), "666", (0, 0, 0), (255, 255, 255), (127, 127, 127))
        while self.__running:
            event: pygame.event.Event | None = None
            self.screen.fill((255, 255, 255))
            for event in pygame.event.get():
                print(event)
                if event.type == pygame.QUIT:
                    self.__running = False
                    pygame.quit()
                    sys.exit()
            self.screen.blit(text.action(pygame.mouse.get_pos(), event), text.rect)
            pygame.display.update()
            self.clock.tick(settings.FPS)

        self.__running = False
        pygame.quit()
        sys.exit()
