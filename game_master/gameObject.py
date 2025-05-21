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
    def __init__(self, pos, name, collision, *groups):
        super().__init__(*groups)
        self.collision:pygame.sprite.Group = collision
        self.layer_g = 2

        self.dead = 0

        self.__surface = {}

        self.attribute = GameObject().copy()
        self.attribute.rect = pos
        self.attribute.move_speed = 100
        self.attribute.name = name

        self.attribute_now = self.attribute.copy()
        self.loss_exp = 100

        self.h_n = self.attribute_now.copy().health
        self.s_n = self.attribute_now.copy().shield
        self.can_be_attack = 1

        self.attack_group = None
        self.attack_box = None

        self.vec2 = [0, 0]

        self.index = 0
        self.move_state = ""
        self.attacking = 0

        self.setup(name, pos)

        self.image = self.__surface[self.move_state][self.index]
        self.rect = self.image.get_rect(center=pos)
        self.hitbox = self.rect.copy().inflate(-self.rect.width / 5, -self.rect.height / 2)

        self.time = 3000
        self.stand = 1
        self.start = pygame.time.get_ticks()

        self.chouhengjuli = 0

        self.damage_a = -1
        self.damage_t = 1

    @property
    def surface(self):
        return self.__surface

    @surface.setter
    def surface(self, surface):
        self.__surface = surface

    def setup(self, name: str, pos):
        path = os.path.join(settings.NPC_V, name)
        for n in os.listdir(path):
            t = os.path.join(path, n)
            temp = []
            for i in os.listdir(t):
                temp.append(pygame.image.load(os.path.join(t, i)).convert_alpha())
            self.__surface[n] = temp
        self.move_state = "stand_back"

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
            self.move_state = "walk_back" if self.vec2[1] == 1 else "walk_front"

    def move(self, dt):
        self.attribute_now.move_speed = self.attribute.move_speed
        self.attribute.rect[0] += self.vec2[0] * self.attribute.move_speed * dt
        self.attribute.rect[1] += self.vec2[1] * self.attribute.move_speed * dt
        self.rect.center = self.attribute.rect
        self.hitbox.center = self.rect.center

    def action_attack(self, dt):
        l = len(self.__surface[self.move_state])
        self.index += dt * l * self.attribute_now.attack_speed
        if self.index >= l:
            self.attacking = 0
            self.index = 0
            self.move_state = "stand_" + self.move_state.split('_')[1]
            self.attack_group.remove(self.attack_box)
            self.attack_box = None
            self.attack_group = None
            return
        self.image = self.__surface[self.move_state][int(self.index)]

    def move_action(self, dt):
        if not self.vec2[0] and not self.vec2[1]:
            self.move_state = "stand_" + self.move_state.split('_')[1]
        l = len(self.__surface[self.move_state])
        if self.move_state[:5] == "stand":
            self.index += dt * l
        else:
            self.index += dt * l * self.attribute_now.move_speed / 100
        if self.index >= l:
            self.index = 0
        self.image = self.__surface[self.move_state][int(self.index)]

    def action(self, rect_other, group):
        if self.attacking:
            return
        if -self.image.width * 2 / 3 <= rect_other.centerx - self.rect.centerx <= self.image.width * 2 / 3 and -self.image.height * 2 / 3 <= rect_other.centery - self.rect.centery <= self.image.height * 2 / 3:
            if not self.attacking:
                self.attacking = 1
                self.move_state = "attack_" + self.move_state.split('_')[1]
                self.index = 0
                self.vec2 = [0, 0]
                self.attack(group)
        elif -self.chouhengjuli <= rect_other.centerx - self.rect.centerx <= self.chouhengjuli and -self.chouhengjuli <= rect_other.centery - self.rect.centery <= self.chouhengjuli:
            if rect_other.centerx - self.rect.centerx == 0:
                self.vec2[0] = 0
            else:
                self.vec2[0] = 1 if rect_other.centerx - self.rect.centerx > 0 else -1
                self.move_state = "walk_right" if self.vec2[0] == 1 else "walk_left"
            if rect_other.centery - self.rect.centery == 0:
                self.vec2[1] = 0
            else:
                self.vec2[1] = 1 if rect_other.centery - self.rect.centery > 0 else -1
                self.move_state = "walk_back" if self.vec2[1] == 1 else "walk_front"
        else:
            self.random_move()

    def attack(self, group):
        pass

    def use(self):
        pass

    def dying(self, dt):
        l = len(self.__surface[self.move_state])
        self.index += dt * l
        if self.index >= l:
            return self
        self.image = self.__surface[self.move_state][int(self.index)]

    def update_collision(self):
        for sprite in self.collision.sprites():
            if hasattr(sprite, "hitbox"):
                if self.hitbox.colliderect(sprite.hitbox):
                    if self.vec2[0] == -1:
                        self.hitbox.left = sprite.hitbox.right
                        self.rect.centerx = self.hitbox.centerx
                        self.attribute.rect[0] = self.hitbox.centerx
                    elif self.vec2[0] == 1:
                        self.hitbox.right = sprite.hitbox.left
                        self.rect.centerx = self.hitbox.centerx
                        self.attribute.rect[0] = self.hitbox.centerx
                    elif self.vec2[1] == -1:
                        self.hitbox.top = sprite.hitbox.bottom
                        self.rect.centery = self.hitbox.centery
                        self.attribute.rect[1] = self.hitbox.centery
                    elif self.vec2[1] == 1:
                        self.hitbox.bottom = sprite.hitbox.top
                        self.rect.centery = self.hitbox.centery
                        self.attribute.rect[1] = self.hitbox.centery
            else:
                if self.hitbox.colliderect(sprite.rect):
                    if self.vec2[0] < 0:
                        self.hitbox.left = sprite.rect.right
                        self.rect.centerx = self.hitbox.centerx
                        self.attribute.rect[0] = self.hitbox.centerx
                    elif self.vec2[0] > 0:
                        self.hitbox.right = sprite.rect.left
                        self.rect.centerx = self.hitbox.centerx
                        self.attribute.rect[0] = self.hitbox.centerx
                    elif self.vec2[1] < 0:
                        self.hitbox.top = sprite.rect.bottom
                        self.rect.centery = self.hitbox.centery
                        self.attribute.rect[1] = self.hitbox.centery
                    elif self.vec2[1] > 0:
                        self.hitbox.bottom = sprite.rect.top
                        self.rect.centery = self.hitbox.centery
                        self.attribute.rect[1] = self.hitbox.centery

    def update_attribute(self):
        if self.dead:
            return
        elif self.h_n <= 0 and not self.dead:
            self.dead = 1
            self.index = 0
            self.vec2 = [0, 0]
            self.move_state = "dead_" + self.move_state.split("_")[1]
        else:
            self.attribute_now = self.attribute.copy()

    def update(self, dt, group=None, rect: pygame.Rect = None):
        self.update_attribute()
        if not self.dead:
            if self.chouhengjuli:
                self.action(rect, group)
            else:
                self.random_move()
            if self.attacking:
                self.action_attack(dt)
            else:
                self.move_action(dt)
            self.move(dt)
            self.update_collision()
            return 0
        else:
            self.update_collision()
            return self.dying(dt)


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

    @attribute.setter
    def attribute(self, a):
        self.__attribute = a

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

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            self.attacked *= other
            self.move_speed *= other
            self.critical_strike_chance *= other
            self.critical_strike_damage *= other
            self.reach_distance *= other
            self.defense *= other
            self.health *= other
            self.shield *= other
            self.attack_speed *= other
        return self

    @staticmethod
    def create():
        return GameObject().copy()

    def attack(self, dt, state, a_s):
        pass

    def use(self):
        pass

    def copy(self):
        return GameObject(self.attribute.copy())
