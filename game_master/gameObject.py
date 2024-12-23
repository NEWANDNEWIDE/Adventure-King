from __future__ import annotations
import os
import random
import pygame.time
import settings

ATTRIBUTE = ("Health", "Shield", "Attack",
             "Defense", "Move_speed", "Attack_speed",
             "Critical_strike_chance", "Critical_strike_damage", "Reach_distance")


# 所有游戏npc的基类
class GameNpc(pygame.sprite.Sprite):
    def __init__(self, pos, group, name="player"):
        super().__init__(group)

        path = os.path.join(settings.GAMEPATH, name)
        self.__surface = {}
        self.__masks = {}

        for name in os.listdir(path):
            t = os.path.join(path, name)
            temp = []
            mask = []
            for i in os.listdir(t):
                temp.append(pygame.image.load(os.path.join(t, i)))
                mask.append(pygame.mask.from_surface(pygame.image.load(os.path.join(t, i))))
            self.__surface[name] = temp
            self.__masks[name] = mask

        self.attribute = GameObject().copy()
        self.attribute.rect = pos
        self.attribute.move_speed = 100
        self.attribute.name = name

        self.vec2 = [0, 0]

        self.index = 0
        self.move_state = "down_idle"
        self.image = self.__surface[self.move_state][self.index]
        self.mask = self.__masks[self.move_state][self.index]
        self.rect = self.image.get_rect(center=pos)

        self.time = 1000
        self.stand = 1
        self.start = pygame.time.get_ticks()

        self.chouhengjuli = 200

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
            self.move_state = "right" if self.vec2[0] == 1 else "left"
        if self.vec2[1]:
            self.move_state = "down" if self.vec2[1] == 1 else "up"

    def move(self, dt):
        self.attribute.rect[0] += self.vec2[0] * self.attribute.move_speed * dt
        self.attribute.rect[1] += self.vec2[1] * self.attribute.move_speed * dt
        self.rect.center = self.attribute.rect

    def move_action(self, dt):
        if not self.vec2[0] and not self.vec2[1] and len(self.move_state) < 6:
            self.move_state += "_idle"
        l = len(self.__surface[self.move_state])
        self.index += dt * l
        if self.index >= l:
            self.index = 0
        self.image = self.__surface[self.move_state][int(self.index)]
        self.mask = self.__masks[self.move_state][int(self.index)]

    def action(self, rect):
        if -self.image.width // 2 <= rect.centerx - self.rect.centerx <= self.image.width // 2 and -self.image.height // 2 <= rect.centery - self.rect.centery <= self.image.height // 2:
            self.vec2 = [0, 0]
        elif -self.chouhengjuli <= rect.centerx - self.rect.centerx <= self.chouhengjuli and -self.chouhengjuli <= rect.centery - self.rect.centery <= self.chouhengjuli:
            if rect.centerx - self.rect.centerx == 0:
                self.vec2[0] = 0
            else:
                self.vec2[0] = 1 if rect.centerx - self.rect.centerx > 0 else -1
                self.move_state = "right" if self.vec2[0] == 1 else "left"
            if rect.centery - self.rect.centery == 0:
                self.vec2[1] = 0
            else:
                self.vec2[1] = 1 if rect.centery - self.rect.centery > 0 else -1
                self.move_state = "down" if self.vec2[1] == 1 else "up"
        else:
            self.random_move()

    def attack(self):
        pass

    def use(self):
        pass

    def update(self, dt, rect:pygame.Rect=None):
        if rect:
            self.action(rect)
        else:
            self.random_move()
        self.move_action(dt)
        self.move(dt)


class GameObject:
    def __init__(self, attribute: list = [0, 0, 0, 0, 0, 0, 0, 0, 0]):
        self.__name = ""
        self.__attribute = attribute
        self.__number = 0
        self.__limit = 1
        # 是否可以穿上
        self.dressed = 0
        # 位置
        self.rect = [-1, -1]
        self.time = 300
        self.vec2 = [0, 0]

    @property
    def attribute(self):
        return self.__attribute

    @property
    def number(self):
        return self.__number

    @number.setter
    def number(self, number):
        self.__number = number

    @property
    def limit(self):
        return self.__limit

    @limit.setter
    def limit(self, limit):
        self.__limit = limit

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def health(self):
        return self.__attribute[0]

    @health.setter
    def health(self, health):
        self.__attribute[0] = health

    @property
    def shield(self):
        return self.__attribute[1]

    @shield.setter
    def shield(self, shield):
        self.__attribute[1] = shield

    @property
    def attacked(self):
        return self.__attribute[2]

    @attacked.setter
    def attacked(self, attacked):
        self.__attribute[2] = attacked

    @property
    def defense(self):
        return self.__attribute[3]

    @defense.setter
    def defense(self, defense):
        self.__attribute[3] = defense

    @property
    def move_speed(self):
        return self.__attribute[4]

    @move_speed.setter
    def move_speed(self, move_speed):
        self.__attribute[4] = move_speed

    @property
    def attack_speed(self):
        return self.__attribute[5]

    @attack_speed.setter
    def attack_speed(self, attack_speed):
        self.__attribute[5] = attack_speed

    @property
    def critical_strike_chance(self):
        return self.__attribute[6]

    @critical_strike_chance.setter
    def critical_strike_chance(self, critical_strike_chance):
        self.__attribute[6] = critical_strike_chance

    @property
    def critical_strike_damage(self):
        return self.__attribute[7]

    @critical_strike_damage.setter
    def critical_strike_damage(self, critical_strike_damage):
        self.__attribute[7] = critical_strike_damage

    @property
    def reach_distance(self):
        return self.__attribute[8]

    @reach_distance.setter
    def reach_distance(self, reach_distance):
        self.__attribute[8] = reach_distance

    def __add__(self, other):
        if isinstance(other, GameObject):
            self.attacked += other.attacked
            self.move_speed += other.move_speed
            self.critical_strike_chance += other.critical_strike_chance
            self.critical_strike_damage += other.critical_strike_damage
            self.reach_distance += other.reach_distance
            self.defense += other.defense
            self.health += other.health
            self.shield += other.shield
            self.attack_speed += other.attack_speed
        return self

    def __sub__(self, other):
        if isinstance(other, GameObject):
            self.attacked -= other.attacked
            self.move_speed -= other.move_speed
            self.critical_strike_chance -= other.critical_strike_chance
            self.critical_strike_damage -= other.critical_strike_damage
            self.reach_distance -= other.reach_distance
            self.defense -= other.defense
            self.health -= other.health
            self.shield -= other.shield
            self.attack_speed -= other.attack_speed
        return self

    @staticmethod
    def create():
        return GameObject().copy()

    def attack(self):
        pass

    def use(self):
        pass

    def copy(self):
        return GameObject(self.attribute.copy())