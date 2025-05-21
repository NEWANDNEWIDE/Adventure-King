import os.path
import pygame
import settings
from game_master.gameObject import GameObject


# 武器
class CrimsonBlade(GameObject):
    NAME = "crimson_blade"

    def __init__(self, name="crimson_blade", limit=1, number=1):
        super().__init__()
        self.attribute = self.attribute.copy()

        self.name = name
        self.limit = limit
        self.number = number if number <= limit else limit
        self.real_name = "浅红之刃"

        self.attacked = 200
        self.attack_speed = 1
        self.reach_distance = 50

        path = os.path.join(settings.WEAPON, "weapon1")
        self.action = 1
        self.action_surface = {}
        self.action_mask = {}
        self.action_index = 0
        self.surf = 0
        self.index = 0
        self.state = "static_right"

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

        self.surface = self.action_surface["static_left"][0].copy()
        self.surf = self.action_surface["static_left"][0].copy()
        max_v = max(self.surface.width, self.surface.height)
        max_v = 40 / max_v
        self.surface = pygame.transform.scale(self.surface, (self.surface.width * max_v, self.surface.height * max_v)).convert_alpha()
        self.mask = pygame.mask.from_surface(self.surface)

    @staticmethod
    def create(number=0):
        return CrimsonBlade(number=number)

    def attack(self, dt, state, a_s):
        state = state.split('_')
        if state[1] == "right":
            if state[0] == "attack":
                t = state[0] + '_' + state[1]
            else:
                t = "static_" + state[1]
        else:
            if state[0] == "attack":
                t = state[0] + '_' + "left"
            else:
                t = "static_left"
        if self.state != t:
            self.state = t
            self.action_index = 0
        l = len(self.action_surface[self.state])
        self.action_index += dt * a_s * l
        if self.action_index >= l:
            self.action_index = 0
        self.surf = self.action_surface[self.state][int(self.action_index)]

    def update(self, dt):
        l = len(self.action_surface["static_left"])
        self.index += dt * l
        if self.index >= l:
            self.index = 0
        self.surface = self.action_surface["static_left"][int(self.index)]
        max_v = max(self.surface.width, self.surface.height)
        max_v = 40 / max_v
        self.surface = pygame.transform.scale(self.surface,
                                              (self.surface.width * max_v, self.surface.height * max_v)).convert_alpha()


class Sword(GameObject):
    NAME = "sword"

    def __init__(self, name="sword", limit=1, number=1):
        super().__init__()
        self.attribute = self.attribute.copy()

        self.name = name
        self.limit = limit
        self.number = number if number <= limit else limit
        self.real_name = "长剑"

        self.attacked = 30
        self.reach_distance = 40

        path = os.path.join(settings.WEAPON, "weapon2")
        self.action = 0
        self.action_surface = {}
        self.action_mask = {}
        self.action_index = 0
        self.surf = 0
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
        self.attribute = self.attribute.copy()

        self.name = name
        self.limit = limit
        self.number = number if number <= limit else limit
        self.real_name = "短刃"

        self.attacked = 30

        path = os.path.join(settings.WEAPON, "weapon3")
        self.action = 0
        self.action_surface = {}
        self.action_mask = {}
        self.action_index = 0
        self.surf = 0
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