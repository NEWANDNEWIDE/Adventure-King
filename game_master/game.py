import sys
import control.button
import game_master.gameSurface
import settings
import pygame
from game_master import level


class Game:
    def __init__(self):
        self.__event = pygame.event.get()
        self.__game_speed = 100
        pygame.init()
        self.__running = True
        self.screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
        pygame.display.set_caption(settings.TITLE)
        self.clock = pygame.time.Clock()
        self.level = level.Level(self.screen)
        self.init()
        self.button = control.button.Button(size=(400, 400), text="Hello!", rectInSize=(100, 100),
                                            area=game_master.gameSurface.HaveNameSurface.CENTER,
                                            fg=(0, 255, 0), bg=(0, 0, 0))

    def init(self):
        pass

    def item(self):
        pass

    def game(self):
        pass

    @property
    def event(self):
        return self.__event

    @event.setter
    def event(self, event):
        self.__event = event

    @property
    def game_speed(self):
        return self.__game_speed

    @game_speed.setter
    def game_speed(self, game_speed):
        self.__game_speed = game_speed

    def run(self):
        while self.__running:
            for self.__event in pygame.event.get():
                if self.__event.type == pygame.QUIT:
                    self.__running = False
                    pygame.quit()
                    sys.exit()

            self.screen.fill((255, 255, 255))
            self.button.render(self.screen)

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