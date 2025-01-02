import os
import pygame
import game_master.gameObject
import settings


class Npc1(game_master.gameObject.GameNpc):
    def __init__(self, pos, name, collision, *groups):
        super().__init__(pos, "npc1", collision, *groups)
        self.name = name


class Npc2(game_master.gameObject.GameNpc):
    def __init__(self, pos, name, collision, *groups):
        super().__init__(pos, "npc2", collision, *groups)
        self.name = name


class Wizard(game_master.gameObject.GameNpc):
    def __init__(self, pos, name, collision, *groups):
        super().__init__(pos, "wizard", collision, *groups)
        self.name = name

    def setup(self, name: str, pos):
        path = os.path.join(settings.NPC_W, name)
        for n in os.listdir(path):
            t = os.path.join(path, n)
            temp = []
            for i in os.listdir(t):
                temp.append(pygame.image.load(os.path.join(t, i)).convert_alpha())
            self.surface[n] = temp
        self.move_state = "walk_back"