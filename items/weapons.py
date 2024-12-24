import os.path
import pygame
import settings
from game_master.gameObject import GameObject


# 武器
class CrimsonBlade(GameObject):
    NAME = "crimson_blade"

    def __init__(self, name="crimson_blade", limit=1, number=1):
        super().__init__()
        self.name = name
        self.limit = limit
        self.number = number if number <= limit else limit
        self.real_name = "浅红之刃"

        self.attacked = 200
        self.attack_speed = 1

        path = os.path.join(settings.WEAPON, "weapon1")
        self.action_surface = {}
        self.action_mask = {}
        self.action_index = 0
        self.state = "static"

        for a in os.listdir(path):
            path_a = os.path.join(path, a)
            temp = []
            temp1 = []
            for b in os.listdir(path_a):
                t = pygame.image.load(os.path.join(path_a, b)).convert_alpha()
                temp.append(t)
                temp1.append(pygame.mask.from_surface(t))
            self.action_surface[a] = temp
            self.action_mask[a] = temp1

        self.surface = self.action_surface["attack_left"][0].copy()
        max_v = max(self.surface.width, self.surface.height)
        max_v = 40 / max_v
        self.surface = pygame.transform.scale(self.surface, (self.surface.width * max_v, self.surface.height * max_v)).convert_alpha()
        self.mask = pygame.mask.from_surface(self.surface)

    @staticmethod
    def create(number=0):
        return CrimsonBlade(number=number)


class Sword(GameObject):
    NAME = "sword"

    def __init__(self, name="sword", limit=1, number=1):
        super().__init__()
        self.name = name
        self.limit = limit
        self.number = number if number <= limit else limit
        self.real_name = "长剑"

        self.attacked = 30

        path = os.path.join(settings.WEAPON, "weapon2")
        self.action_surface = {}
        self.action_mask = {}
        self.action_index = 0
        self.state = "static"

        for a in os.listdir(path):
            path_a = os.path.join(path, a)
            temp = []
            temp1 = []
            for b in os.listdir(path_a):
                t = pygame.image.load(os.path.join(path_a, b)).convert_alpha()
                temp.append(t)
                temp1.append(pygame.mask.from_surface(t))
            self.action_surface[a] = temp
            self.action_mask[a] = temp1

        self.surface = self.action_surface["attack_left"][0].copy()
        max_v = max(self.surface.width, self.surface.height)
        max_v = 40 / max_v
        self.surface = pygame.transform.scale(self.surface,
                                              (self.surface.width * max_v, self.surface.height * max_v)).convert_alpha()
        self.mask = pygame.mask.from_surface(self.surface)

    @staticmethod
    def create(number=0):
        return Sword(number=number)


class Blades(GameObject):
    NAME = "blades"

    def __init__(self, name="blades", limit=1, number=1):
        super().__init__()
        self.name = name
        self.limit = limit
        self.number = number if number <= limit else limit
        self.real_name = "长刃"

        self.attacked = 30

        path = os.path.join(settings.WEAPON, "weapon3")
        self.action_surface = {}
        self.action_mask = {}
        self.action_index = 0
        self.state = "static"

        for a in os.listdir(path):
            path_a = os.path.join(path, a)
            temp = []
            temp1 = []
            for b in os.listdir(path_a):
                t = pygame.image.load(os.path.join(path_a, b)).convert_alpha()
                temp.append(t)
                temp1.append(pygame.mask.from_surface(t))
            self.action_surface[a] = temp
            self.action_mask[a] = temp1

        self.surface = self.action_surface["attack_left"][0].copy()
        max_v = max(self.surface.width, self.surface.height)
        max_v = 40 / max_v
        self.surface = pygame.transform.scale(self.surface,
                                              (self.surface.width * max_v, self.surface.height * max_v)).convert_alpha()
        self.mask = pygame.mask.from_surface(self.surface)

    @staticmethod
    def create(number=1):
        return Blades(number=number)