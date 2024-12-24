import os
import random

import pygame
import game_master
import settings


class Boss(game_master.gameObject.GameNpc):
    def __init__(self, pos, name, *groups):
        super().__init__(pos, "boss", *groups)
        self.name = name


class Crazy(Boss):
    def __init__(self, pos, *groups):
        super().__init__(pos, "crazy", *groups)

    def setup(self, name: str):
        path = os.path.join(settings.MONSTER, name)
        for n in os.listdir(path):
            t = os.path.join(path, n)
            temp = []
            for i in os.listdir(t):
                temp.append(pygame.image.load(os.path.join(t, i)).convert_alpha())
            self.surface[n] = temp
        self.move_state = "stand_left"

    def random_move(self):
        if self.stand:
            if pygame.time.get_ticks() - self.start >= self.time:
                self.stand = 0
                self.start = 0
        elif not self.start:
            self.vec2[0] = random.randint(-1, 1)
            if self.vec2[0]:
                self.vec2[1] = 0
            else:
                self.vec2[1] = random.randint(-1, 1)
            self.start = pygame.time.get_ticks()
        else:
            if pygame.time.get_ticks() - self.start >= self.time:
                self.vec2 = [0, 0]
                self.start = pygame.time.get_ticks()
                self.stand = 1
        if self.vec2[0]:
            self.move_state = "walk_right" if self.vec2[0] == 1 else "walk_left"
        if self.vec2[1]:
            t = self.move_state.split('_')
            self.move_state = "walk_" + t[1]

    def action(self, rect):
        if -self.image.width // 2 <= rect.centerx - self.rect.centerx <= self.image.width // 2 and -self.image.height // 2 <= rect.centery - self.rect.centery <= self.image.height // 2:
            self.vec2 = [0, 0]
        elif -self.chouhengjuli <= rect.centerx - self.rect.centerx <= self.chouhengjuli and -self.chouhengjuli <= rect.centery - self.rect.centery <= self.chouhengjuli:
            if rect.centerx - self.rect.centerx == 0:
                self.vec2[0] = 0
            else:
                self.vec2[0] = 1 if rect.centerx - self.rect.centerx > 0 else -1
                self.move_state = "walk_right" if self.vec2[0] == 1 else "walk_left"
            if rect.centery - self.rect.centery == 0:
                self.vec2[1] = 0
            else:
                self.vec2[1] = 1 if rect.centery - self.rect.centery > 0 else -1
                t = self.move_state.split('_')
                self.move_state = "walk_" + t[1]
        else:
            self.random_move()

    def attack(self):
        pass