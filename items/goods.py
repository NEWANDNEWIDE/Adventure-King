from __future__ import annotations
import pygame.image
import game_master.gameObject


class TestItem(game_master.gameObject.GameObject):
    NAME = "test"

    def __init__(self, name="test", limit=64, number=0):
        super().__init__()
        self.name = name
        self.limit = limit
        self.number = number if number <= limit else limit
        self.surface = pygame.image.load(
            r"C:\Users\10962\Desktop\Pygame-Cameras-main\graphics\player.png").convert_alpha()
        self.surface = pygame.transform.scale(self.surface, (40, 40))
        self.mask = pygame.mask.from_surface(self.surface)

    @staticmethod
    def create(number=0):
        return TestItem(number=number)


class TestItemOther(game_master.gameObject.GameObject):
    NAME = "test1"

    def __init__(self, name="test1", limit=64, number=0):
        super().__init__()
        self.name = name
        self.limit = limit
        self.number = number if number <= limit else limit
        self.surface = pygame.image.load(r"C:\Users\10962\Desktop\123\13.png").convert_alpha()
        self.surface = pygame.transform.scale(self.surface, (40, 40))
        self.mask = pygame.mask.from_surface(self.surface)

    @staticmethod
    def create(number=0):
        return TestItemOther(number=number)
