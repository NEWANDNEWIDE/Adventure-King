import os
import pygame
import game_master.gameObject
import settings


class Goblin(game_master.gameObject.GameNpc):
    def __init__(self, pos, name="goblin", *groups):
        super().__init__(pos, name, *groups)
        self.name = name

    def setup(self, name: str):
        path = os.path.join(settings.MONSTER, name)
        for n in os.listdir(path):
            t = os.path.join(path, n)
            temp = []
            mask = []
            for i in os.listdir(t):
                temp.append(pygame.image.load(os.path.join(t, i)).convert_alpha())
                mask.append(pygame.mask.from_surface(pygame.image.load(os.path.join(t, i)).convert_alpha()))
            self.surface[n] = temp
            self.masks[n] = mask
        self.move_state = "walk_back"

    def attack(self):
        pass


class Minotaur(game_master.gameObject.GameNpc):
    def __init__(self, pos, name="minotaur", *groups):
        super().__init__(pos, name, *groups)
        self.name = name

    def setup(self, name: str):
        path = os.path.join(settings.MONSTER, name)
        for n in os.listdir(path):
            t = os.path.join(path, n)
            temp = []
            mask = []
            for i in os.listdir(t):
                temp.append(pygame.image.load(os.path.join(t, i)).convert_alpha())
                mask.append(pygame.mask.from_surface(pygame.image.load(os.path.join(t, i)).convert_alpha()))
            self.surface[n] = temp
            self.masks[n] = mask
        self.move_state = "walk_back"

    def attack(self):
        pass


class Sheep(game_master.gameObject.GameNpc):
    def __init__(self, pos, name="sheep", *groups):
        super().__init__(pos, name, *groups)
        self.name = name

    def setup(self, name: str):
        path = os.path.join(settings.MONSTER, name)
        for n in os.listdir(path):
            t = os.path.join(path, n)
            temp = []
            mask = []
            for i in os.listdir(t):
                temp.append(pygame.image.load(os.path.join(t, i)).convert_alpha())
                mask.append(pygame.mask.from_surface(pygame.image.load(os.path.join(t, i)).convert_alpha()))
            self.surface[n] = temp
            self.masks[n] = mask
        self.move_state = "walk_back"

    def attack(self):
        pass


class Skeleton(game_master.gameObject.GameNpc):
    def __init__(self, pos, name="skeleton", *groups):
        super().__init__(pos, name, *groups)
        self.name = name

    def setup(self, name: str):
        path = os.path.join(settings.MONSTER, name)
        for n in os.listdir(path):
            t = os.path.join(path, n)
            temp = []
            mask = []
            for i in os.listdir(t):
                temp.append(pygame.image.load(os.path.join(t, i)).convert_alpha())
                mask.append(pygame.mask.from_surface(pygame.image.load(os.path.join(t, i)).convert_alpha()))
            self.surface[n] = temp
            self.masks[n] = mask
        self.move_state = "walk_back"

    def attack(self):
        pass