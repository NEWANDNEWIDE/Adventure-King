import os
import pygame
import game_master.gameObject
import settings


class Npc1(game_master.gameObject.GameNpc):
    def __init__(self, pos, name, *groups):
        super().__init__(pos, "npc1", *groups)
        self.name = name


class Npc2(game_master.gameObject.GameNpc):
    def __init__(self, pos, name, *groups):
        super().__init__(pos, "npc2", *groups)
        self.name = name


class Wizard(game_master.gameObject.GameNpc):
    def __init__(self, pos, name, *groups):
        super().__init__(pos, "wizard", *groups)
        self.name = name

    def setup(self, name: str):
        path = os.path.join(settings.NPC_W, name)
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