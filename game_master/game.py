import sys
import control.button
import game_master.gameSurface
import settings
import pygame
from game_master import level


class Game:
    def __init__(self):
        self.__game_speed = 100
        pygame.init()
        self.running = True
        self.screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
        pygame.display.set_caption(settings.TITLE)
        self.clock = pygame.time.Clock()
        self.level = level.Level(self.screen)
        self.button = control.button.Button(size=(400, 400), text="Hello!", rectInSize=(100, 100),
                                            area=game_master.gameSurface.HaveNameSurface.CENTER,
                                            fg=(0, 255, 0), bg=(0, 0, 0))

    @property
    def game_speed(self):
        return self.__game_speed

    @game_speed.setter
    def game_speed(self, game_speed):
        self.__game_speed = game_speed

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill((255, 255, 255))
            self.button.render(self.screen)

            pygame.display.update()
            self.clock.tick(settings.FPS)

        pygame.quit()
        sys.exit()

    def get_running_state(self):
        return self.running

    def set_running_state(self, running):
        self.running = running