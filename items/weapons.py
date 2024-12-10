import pygame
import game_master
from game_master.gameObject import GameObject


# 武器
class WoodenSword(GameObject):
    NAME = "wooden-sword"

    def __init__(self, name="wooden-sword", limit=1, number=0):
        super().__init__()
        self.name = name
        self.limit = limit
        self.number = number
        self.attack = 20
        self.reach_distance = 1
        self.surface = game_master.fileManager.game_surface[name]
        self.__sleep = 1000 // (self.attack_speed * (self.surface[0] - 2))
        self.__mid = (self.surface[0] - 1) // 2 + 1

    @staticmethod
    def create(number=0):
        return WoodenSword(number=number)

    def left_attack(self, surface: pygame.surface.Surface):
        for i in range(2, self.__mid):
            surface.blit(self.surface[i], (400, 300))
            pygame.time.delay(self.__sleep)
        surface.blit(self.surface[1], (400, 300))

    def right_attack(self, surface: pygame.surface.Surface):
        for i in range(self.__mid + 1, self.surface[0]):
            surface.blit(self.surface[i], (400, 300))
            pygame.time.delay(self.__sleep)
        surface.blit(self.surface[1], (400, 300))


class StoneSword(WoodenSword):
    NAME = "stone-sword"

    def __init__(self):
        super().__init__("stone-sword")
        self.attack += 20

    @staticmethod
    def create(number=0):
        return WoodenSword(number=number)


class GoldenSword(WoodenSword):
    NAME = "golden-sword"

    def __init__(self):
        super().__init__("golden-sword")
        self.attack += 30

    @staticmethod
    def create(number=0):
        return WoodenSword(number=number)


class IronSword(WoodenSword):
    NAME = "iron-sword"

    def __init__(self):
        super().__init__("iron-sword")
        self.attack += 40

    @staticmethod
    def create(number=0):
        return WoodenSword(number=number)


class DiamondSword(WoodenSword):
    NAME = "diamond-sword"

    def __init__(self):
        super().__init__("diamond-sword")
        self.attack += 60

    @staticmethod
    def create(number=0):
        return WoodenSword(number=number)
