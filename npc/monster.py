import os
import random

import pygame
import game_master.gameObject
import settings
from game_master.gameSurface import AttackingObj


class Goblin(game_master.gameObject.GameNpc):
    def __init__(self, pos, collision, *groups):
        super().__init__(pos, "goblin", collision, *groups)
        self.attribute.health = 100
        self.h_n = 100
        self.attribute.attacked = 20
        self.chouhengjuli = 200
        self.attribute.attack_speed = 1

    def setup(self, name: str, pos):
        path = os.path.join(settings.MONSTER, name)
        for n in os.listdir(path):
            t = os.path.join(path, n)
            temp = []
            for i in os.listdir(t):
                temp.append(pygame.image.load(os.path.join(t, i)).convert_alpha())
            self.surface[n] = temp
        self.move_state = "walk_back"

    def attack(self, group):
        self.attack_group = group
        r = random.random()
        damage = self.attribute_now.attacked
        if r <= self.attribute_now.critical_strike_chance:
            damage *= self.attribute_now.critical_strike_damage
        t = self.move_state.split('_')[1]
        if t == "right":
            pos = self.rect.right, self.rect.centery
        elif t == "left":
            pos = self.rect.left, self.rect.centery
        elif t == "front":
            pos = self.rect.centerx, self.rect.top
        else:
            pos = self.rect.centerx, self.rect.bottom
        self.attack_box = AttackingObj(damage, pos, "monster", -1, group, rect=self.image.get_rect(center=pos))

    def update_attribute(self):
        if self.dead:
            return
        elif self.h_n <= 0 and not self.dead:
            self.dead = 1
            self.index = 0
            self.vec2 = [0, 0]
            self.move_state = "dead"
        else:
            self.attribute_now = self.attribute.copy()


class Minotaur(game_master.gameObject.GameNpc):
    def __init__(self, pos, collision, name="minotaur", *groups):
        super().__init__(pos, name, collision, *groups)
        self.name = name

    def setup(self, name: str, pos):
        path = os.path.join(settings.MONSTER, name)
        for n in os.listdir(path):
            t = os.path.join(path, n)
            temp = []
            for i in os.listdir(t):
                temp.append(pygame.image.load(os.path.join(t, i)).convert_alpha())
            self.surface[n] = temp
        self.move_state = "walk_back"

    def attack(self, group):
        self.attack_group = group
        r = random.random()
        damage = self.attribute_now.attacked
        if r <= self.attribute_now.critical_strike_chance:
            damage *= self.attribute_now.critical_strike_damage
        t = self.move_state.split('_')[1]
        if t == "right":
            pos = self.rect.right, self.rect.centery
        elif t == "left":
            pos = self.rect.left, self.rect.centery
        elif t == "front":
            pos = self.rect.centerx, self.rect.top
        else:
            pos = self.rect.centerx, self.rect.bottom
        self.attack_box = AttackingObj(damage, pos, "monster", -1, group, rect=self.image.get_rect(center=pos))

    def update_attribute(self):
        if self.dead:
            return
        elif self.h_n <= 0 and not self.dead:
            self.dead = 1
            self.index = 0
            self.vec2 = [0, 0]
            self.move_state = "dead"
        else:
            self.attribute_now = self.attribute.copy()


class Sheep(game_master.gameObject.GameNpc):
    def __init__(self, pos, collision, name="sheep", *groups):
        super().__init__(pos, name, collision, *groups)
        self.name = name

    def setup(self, name: str, pos):
        path = os.path.join(settings.MONSTER, name)
        for n in os.listdir(path):
            t = os.path.join(path, n)
            temp = []
            for i in os.listdir(t):
                temp.append(pygame.image.load(os.path.join(t, i)).convert_alpha())
            self.surface[n] = temp
        self.move_state = "walk_back"

    def attack(self, group):
        self.attack_group = group
        r = random.random()
        damage = self.attribute_now.attacked
        if r <= self.attribute_now.critical_strike_chance:
            damage *= self.attribute_now.critical_strike_damage
        t = self.move_state.split('_')[1]
        if t == "right":
            pos = self.rect.right, self.rect.centery
        elif t == "left":
            pos = self.rect.left, self.rect.centery
        elif t == "front":
            pos = self.rect.centerx, self.rect.top
        else:
            pos = self.rect.centerx, self.rect.bottom
        self.attack_box = AttackingObj(damage, pos, "monster", -1, group, rect=self.image.get_rect(center=pos))

    def update_attribute(self):
        if self.dead:
            return
        elif self.h_n <= 0 and not self.dead:
            self.dead = 1
            self.index = 0
            self.vec2 = [0, 0]
            self.move_state = "dead"
        else:
            self.attribute_now = self.attribute.copy()


class Skeleton(game_master.gameObject.GameNpc):
    def __init__(self, pos, collision, name="skeleton", *groups):
        super().__init__(pos, name, collision, *groups)
        self.name = name

    def setup(self, name: str, pos):
        path = os.path.join(settings.MONSTER, name)
        for n in os.listdir(path):
            t = os.path.join(path, n)
            temp = []
            for i in os.listdir(t):
                temp.append(pygame.image.load(os.path.join(t, i)).convert_alpha())
            self.surface[n] = temp
        self.move_state = "walk_back"

    def attack(self, group):
        self.attack_group = group
        r = random.random()
        damage = self.attribute_now.attacked
        if r <= self.attribute_now.critical_strike_chance:
            damage *= self.attribute_now.critical_strike_damage
        t = self.move_state.split('_')[1]
        if t == "right":
            pos = self.rect.right, self.rect.centery
        elif t == "left":
            pos = self.rect.left, self.rect.centery
        elif t == "front":
            pos = self.rect.centerx, self.rect.top
        else:
            pos = self.rect.centerx, self.rect.bottom
        self.attack_box = AttackingObj(damage, pos, "monster", -1, group, rect=self.image.get_rect(center=pos))

    def update_attribute(self):
        if self.dead:
            return
        elif self.h_n <= 0 and not self.dead:
            self.dead = 1
            self.index = 0
            self.vec2 = [0, 0]
            self.move_state = "dead"
        else:
            self.attribute_now = self.attribute.copy()