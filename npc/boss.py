import os
import random
import pygame
import game_master
import settings
from game_master.gameSurface import AttackingObj


class Boss(game_master.gameObject.GameNpc):
    def __init__(self, pos, name, collision, *groups):
        super().__init__(pos, "boss", collision, *groups)
        self.name = name


class Crazy(Boss):
    def __init__(self, pos, collision, *groups):
        super().__init__(pos, "crazy", collision, *groups)
        self.attribute.health = 1000000
        self.attribute.attacked = 2000
        self.attribute.attack_speed = 1
        self.attribute.move_speed = 400
        self.attribute.defense = 1000
        self.attribute.critical_strike_damage = 5
        self.attribute.critical_strike_chance = 1
        self.attribute_now = self.attribute.copy()
        self.h_n = self.attribute_now.health
        self.chouhengjuli = 2000

    def setup(self, name: str, pos):
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

    def action(self, rect, group):
        if self.attacking:
            return
        if -self.image.width - 50 <= rect.centerx - self.rect.centerx <= self.image.width + 50 and -self.image.height - 50 <= rect.centery - self.rect.centery <= self.image.height + 50:
            if not self.attacking:
                r = f"{random.randint(1, 2)}_"
                self.attacking = 1
                self.move_state = "attack" + r + self.move_state.split('_')[1]
                self.index = 0
                self.vec2 = [0, 0]
                self.attack(group)
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

    def attack(self, group):
        self.attack_group = group
        r = random.random()
        damage = self.attribute_now.attacked
        if r < self.attribute_now.critical_strike_chance:
            damage *= self.attribute_now.critical_strike_damage
        t = self.move_state.split('_')[1]
        if t == "right":
            pos = self.rect.right, self.rect.centery
        else:
            pos = self.rect.left, self.rect.centery
        self.attack_box = AttackingObj(damage, pos, "monster", -1, group, rect=self.image.get_rect(center=pos).copy().inflate(60, 60))