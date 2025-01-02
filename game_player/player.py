import os
import random
from typing import List
import pygame
from pytmx import TiledMap
import game_master.fileManager
import items
import settings
from game_master.gameObject import GameObject
from game_master.gameSurface import MapSprite, AttackingObj
from items import className


def n_pow(x, n):
    if n < 1:
        return 0
    if n == 1:
        return x
    return n*n_pow(x, n-1)


def s_pow(x, n, index):
    if x < n * index:
        return 0
    else:
        return 1 + s_pow(x - n * index, n, index+1)


def sort_2(nums, target):
    l = 0
    r = len(nums)
    while l < r:
        m = (l + r) // 2
        if nums[m].layer_g < target:
            l = m + 1
        else:
            r = m
    return r


def sort_1(nums, target):
    if not nums:
        return 0
    l = 0
    r = len(nums)
    while l < r:
        m = (l + r) // 2
        if nums[m].rect.bottom < target:
            l = m + 1
        else:
            r = m
    return r if r < len(nums) else len(nums) - 1


def sort_0(nums, target):
    if not nums:
        return 0
    l = 0
    r = len(nums)
    while l < r:
        m = (l + r) // 2
        if nums[m].rect.centerx < target:
            l = m + 1
        else:
            r = m

    return r if r < len(nums) else len(nums) - 1


class CameraGroup(pygame.sprite.Group):
    def __init__(self, surface, tmx: TiledMap, *groups):
        super().__init__()
        self.__display = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()
        self.__surface = surface
        self.__tmx_group = [[], []]
        self.player_index = [0, -1]
        self.obj = self.sprites()

        self.h_w = settings.WIDTH // 2
        self.h_h = settings.HEIGHT // 2

        self.ground_rect = self.__surface.get_rect(topleft=(0, 0))

        self.tmx: TiledMap = tmx

        self.setup(*groups)

    def setup(self, *groups):
        if self.tmx:
            i = 0
            temp = []
            if self.__surface.width < 2000:
                for layer in ["ground", "collision"]:
                    for x, y, surf in self.tmx.get_layer_by_name(layer).tiles():
                        if surf:
                            if i == 0:
                                self.__surface.blit(surf, (self.tmx.tilewidth * x, self.tmx.tileheight * y))
                                temp.append(MapSprite((self.tmx.tilewidth * x, self.tmx.tileheight * y), surf, 1))
                            else:
                                temp.append(MapSprite((self.tmx.tilewidth * x, self.tmx.tileheight * y), surf, 2, *groups))
                    i += 1
            else:
                for layer in ["ground", "middle", "no_collision", "collision"]:
                    for x, y, surf in self.tmx.get_layer_by_name(layer).tiles():
                        if surf:
                            if i <= 1:
                                self.__surface.blit(surf, (self.tmx.tilewidth * x, self.tmx.tileheight * y))
                                temp.append(MapSprite((self.tmx.tilewidth * x, self.tmx.tileheight * y), surf, 1))
                            elif i == 2:
                                temp.append(MapSprite((self.tmx.tilewidth * x, self.tmx.tileheight * y), surf, 2))
                            else:
                                temp.append(MapSprite((self.tmx.tilewidth * x, self.tmx.tileheight * y), surf, 2, *groups))
                    i += 1
            temp.sort(key=lambda r: r.layer_g)
            m = sort_2(temp, 2)
            t1 = temp[:m]
            t2 = temp[m:]
            self.__tmx_group = [t1, t2]

    def center_target_camera(self, target):
        self.offset.x = target.centerx - self.h_w
        self.offset.y = target.centery - self.h_h

    def custom_draw(self, rect_other, dt):

        self.center_target_camera(rect_other)

        ground_offset = self.ground_rect.topleft - self.offset
        self.__display.blit(self.__surface, ground_offset)

        # active elements
        i = 0
        t = self.obj[self.player_index[0]]
        for sprite in self.__tmx_group[1]:
            if -620 <= rect_other.centerx - sprite.rect.centerx <= 620 and -470 <= rect_other.centery - sprite.rect.centery <= 470:
                if self.player_index[0] + i <= self.player_index[1]:
                    if sprite.rect.bottom > t.rect.bottom:
                        offset_pos = t.rect.center - self.offset
                        rect = t.image.get_rect(center=offset_pos)
                        self.__display.blit(t.image, rect)
                        if t.damage_a >= 0:
                            t.damage_t -= dt
                            font = game_master.game.Game.FONT.render(f"-{t.damage_a}" if t.damage_a else "0", True, (0, 0, 0))
                            rect_font = font.get_rect(center=rect.center)
                            rect_font.bottom = rect.top
                            self.__display.blit(font, rect_font)
                            if t.damage_t <= 0:
                                t.damage_a = -1
                                t.damage_t = 1
                        i += 1
                        if self.player_index[0] + i <= self.player_index[1]:
                            t = self.obj[self.player_index[0] + i]
                            while self.player_index[0] + i <= self.player_index[1] and (-620 > rect_other.centerx - t.rect.centerx or rect_other.centerx - t.rect.centerx > 620):
                                i += 1
                                if self.player_index[0] + i <= self.player_index[1]:
                                    t = self.obj[self.player_index[0] + i]
                        offset_pos = sprite.rect.center - self.offset
                        rect = sprite.image.get_rect(center=offset_pos)
                        self.__display.blit(sprite.image, rect)
                    else:
                        offset_pos = sprite.rect.center - self.offset
                        rect = sprite.image.get_rect(center=offset_pos)
                        self.__display.blit(sprite.image, rect)
                else:
                    offset_pos = sprite.rect.center - self.offset
                    rect = sprite.image.get_rect(center=offset_pos)
                    self.__display.blit(sprite.image, rect)
        while self.player_index[0] + i <= self.player_index[1]:
            offset_pos = t.rect.center - self.offset
            rect = t.image.get_rect(center=offset_pos)
            self.__display.blit(t.image, rect)
            if t.damage_a >= 0:
                t.damage_t -= dt
                font = game_master.game.Game.FONT.render(f"-{t.damage_a}" if t.damage_a else "0", True, (0, 0, 0))
                rect_font = font.get_rect(center=rect.center)
                rect_font.bottom = rect.top
                self.__display.blit(font, rect_font)
                if t.damage_t <= 0:
                    t.damage_a = -1
                    t.damage_t = 1
            i += 1
            if self.player_index[0] + i <= self.player_index[1]:
                t = self.obj[self.player_index[0] + i]

    def update(self, bottom):
        self.obj = self.sprites()
        self.obj.sort(key=lambda sprite: sprite.rect.bottom)
        self.player_index[0] = sort_1(self.obj, bottom - 470)
        self.player_index[1] = self.player_index[0] + sort_1(self.obj[self.player_index[0]:], bottom + 470)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, collision, boss_collision, *groups):
        super().__init__(*groups)
        self.boss = 0
        self.collision = collision
        self.boss_collision = boss_collision
        self.layer_g = 2

        self.__surface = {}

        for n in os.listdir(settings.PLAYER):
            d = {}

            path = os.path.join(settings.PLAYER, n)

            for name in os.listdir(path):
                t = os.path.join(path, name)
                temp = []
                for i in os.listdir(t):
                    temp.append(pygame.image.load(os.path.join(t, i)))
                d[name] = temp

            self.__surface[n] = d

        self.__vec2 = [0, 0]
        self.dead = 0

        # 是否打开合成台
        self.sys_state = 0
        # 是否奔跑
        self.run = 0
        self.attacking = 0
        # 闪避
        self.shanbi = 0
        self.shanbi_state = 0
        self.dir = [0, 0]

        self.index = 0
        self.player_state = "player1"
        self.move_state = "stand_back"
        self.image = self.__surface[self.player_state][self.move_state][self.index]

        self.spawn_point = pos
        self.boss_spawn_point = [562, 362]
        self.rect = self.image.get_rect(center=pos)
        self.hitbox = self.rect.copy().inflate(-self.rect.width / 5, -self.rect.height / 2)

        # 头 胸 腿 靴
        self.armor = [0, 0, 0, 0]

        self.w = self.image.width
        self.h = self.image.height
        self.bag = Bag()

        self.attribute = GameObject().copy()
        self.attribute.rect = pos
        self.attribute.name = "player"
        self.attribute.health = 200
        self.attribute.shield = 100
        self.attribute.attacked = 5
        self.attribute.attack_speed = 1
        self.attribute.critical_strike_chance = 0.05
        self.attribute.critical_strike_damage = 1.5
        self.attribute.reach_distance = 1
        self.attribute.move_speed = 200

        self.attribute_now = self.attribute.copy()

        self.level_a = GameObject().copy()
        self.level_a.health = 10
        self.level_a.attacked = 2
        self.level_a.defense = 1

        self.level = 1

        self.level_exp = 20000

        self.exp = 100

        self.level = s_pow(self.level_exp, self.exp, 1) + 1
        self.attribute_now = (self.attribute.copy() + self.level_a.copy() * (self.level - 1)).copy()
        self.h_n = self.attribute_now.copy().health
        self.s_n = self.attribute_now.copy().shield

        self.attack_box = None
        self.attack_group = None

        self.damage_a = -1
        self.damage_t = 1

    @property
    def vec2(self):
        return self.__vec2

    @vec2.setter
    def vec2(self, vec2):
        self.__vec2 = vec2

    def attack(self, group):
        self.attack_group = group
        r = random.random()
        damage = self.attribute_now.attacked
        if r < self.attribute_now.critical_strike_chance:
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
        self.attack_box = AttackingObj(damage, pos, "player", -1, group, rect=self.image.get_rect(center=pos).copy().inflate(self.attribute_now.reach_distance, self.attribute_now.reach_distance))

    def use(self):
        if self.bag.bag[self.bag.selection_box]:
            self.bag.bag[self.bag.selection_box].use()

    def input(self):
        if not self.attacking:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_d] and not self.vec2[1]:
                self.__vec2[0] = 1
                self.move_state = "walk_right"
            elif keys[pygame.K_a] and not self.vec2[1]:
                self.__vec2[0] = -1
                self.move_state = "walk_left"
            else:
                self.__vec2[0] = 0
            if keys[pygame.K_s] and not self.vec2[0]:
                self.__vec2[1] = 1
                self.move_state = "walk_back"
            elif keys[pygame.K_w] and not self.vec2[0]:
                self.__vec2[1] = -1
                self.move_state = "walk_front"
            else:
                self.__vec2[1] = 0

    def action_attack(self, dt):
        if self.bag.bag[self.bag.selection_box]:
            self.bag.bag[self.bag.selection_box].attack(dt)
        l = len(self.__surface[self.player_state][self.move_state])
        self.index += dt * l * self.attribute_now.attack_speed * 2
        if self.index >= l:
            self.attacking = 0
            self.index = 0
            if not self.vec2[0] and not self.vec2[1]:
                self.move_state = "stand_" + self.move_state.split('_')[1]
            else:
                self.move_state = "walk_" + self.move_state.split('_')[1]
            self.attack_group.remove(self.attack_box)
            self.attack_box = None
            self.attack_group = None
            return
        self.image = self.__surface[self.player_state][self.move_state][int(self.index)]

    def action(self, dt):
        if not self.vec2[0] and not self.vec2[1]:
            self.move_state = "stand_" + self.move_state.split('_')[1]
        l = len(self.__surface[self.player_state][self.move_state])
        self.index += dt * l * self.attribute_now.move_speed / 100
        if self.index >= l:
            self.index = 0
        self.image = self.__surface[self.player_state][self.move_state][int(self.index)]

    def move(self, dt):
        self.input()
        if self.attacking:
            self.action_attack(dt)
        else:
            self.action(dt)
        if not self.run and not self.shanbi_state:
            self.attribute.rect[0] += self.vec2[0] * self.attribute_now.move_speed * dt
            self.attribute.rect[1] += self.vec2[1] * self.attribute_now.move_speed * dt
        elif self.shanbi_state:
            if self.shanbi > 0:
                self.attribute_now.move_speed += self.attribute.move_speed * 9
                self.attribute.rect[0] += self.dir[0] * self.attribute_now.move_speed * dt
                self.attribute.rect[1] += self.dir[1] * self.attribute_now.move_speed * dt
                self.shanbi -= dt
            else:
                self.shanbi = -1.0
                self.shanbi_state = 0
                self.dir = [0, 0]
        else:
            self.attribute_now.move_speed += self.attribute.move_speed
            self.attribute.rect[0] += self.vec2[0] * self.attribute_now.move_speed * dt
            self.attribute.rect[1] += self.vec2[1] * self.attribute_now.move_speed * dt
        self.rect.center = self.attribute.rect
        self.hitbox.center = self.rect.center
        if not self.shanbi_state and self.shanbi < 0:
            self.shanbi += dt

    def dying(self, dt):
        l = len(self.__surface[self.player_state][self.move_state])
        self.index += dt * l
        if self.index >= l:
            self.index = 0
            self.dead = 0
            self.move_state = "stand_back"
            return 1
        self.image = self.__surface[self.player_state][self.move_state][int(self.index)]
        return 0

    def update_collision(self):
        if self.boss:
            for sprite in self.boss_collision.sprites():
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
        else:
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
            self.move_state = "dead"
        else:
            self.attribute_now = self.attribute.copy()
            self.level = s_pow(self.level_exp, self.exp, 1) + 1
            self.attribute_now = (self.attribute.copy() + self.level_a.copy() * (self.level - 1)).copy()
            if self.bag.bag[self.bag.selection_box]:
                self.attribute_now += self.bag.bag[self.bag.selection_box].copy()
            if self.h_n > self.attribute_now.health:
                self.h_n = self.attribute_now.health
            if self.s_n > self.attribute_now.shield:
                self.s_n = self.attribute_now.shield

    def update_dressed(self):
        if self.bag.bag[self.bag.selection_box]:
            if self.bag.bag[self.bag.selection_box].name == "sword":
                self.player_state = "player2"
            elif self.bag.bag[self.bag.selection_box].name == "blades":
                self.player_state = "player3"
            else:
                self.player_state = "player1"
        else:
            self.player_state = "player1"
        if self.bag.dressed_state:
            self.bag.dressed_state = 0
            for a in self.armor:
                self.attribute -= a
            for a in range(4):
                self.attribute += self.bag.bag[a]

    def update(self, dt):
        self.update_attribute()
        if not self.dead:
            self.move(dt)
            self.bag.update(self.image, dt)
            self.update_dressed()
            if self.sys_state:
                self.sys_state.update()
            self.update_collision()
            return 0
        else:
            self.update_collision()
            return self.dying(dt)


class State:
    def __init__(self):
        self.display = pygame.image.load("res/item/lifebar4.png").convert_alpha()
        self.life_bar = pygame.image.load("res/item/lifebar1.png").convert_alpha()
        self.life_bar = pygame.transform.scale(self.life_bar, (self.life_bar.width * 2, self.life_bar.height))
        self.life_bar_w = self.life_bar.width - 14 * 2
        self.life_bar_h = self.life_bar.height - 12
        self.health = pygame.image.load("res/item/health.png").convert_alpha()
        self.health = pygame.transform.scale(self.health, (self.life_bar.height / self.health.height * self.health.width, self.life_bar.height))
        self.shield = pygame.image.load("res/item/sheild.png").convert_alpha()
        self.shield = pygame.transform.scale(self.shield, (self.life_bar.height / self.shield.height * self.shield.width, self.life_bar.height))
        self.xp = pygame.image.load("res/item/xp.png").convert_alpha()
        self.xp = pygame.transform.scale(self.xp, (self.life_bar.height / self.xp.height * self.xp.width, self.life_bar.height))
        self.w = max(self.shield.width, self.health.width, self.xp.width)
        self.display = pygame.transform.scale(self.display, (self.life_bar.width + self.w + 5, self.life_bar.height * 5 + 10))

    def render(self, player: Player):
        level_t = f"Lv.{player.level}: {player.attribute.name}"
        level_f = pygame.font.Font(settings.FONT, 20)
        level_t = level_f.render(level_t, True, (0, 0, 0))
        self.display.blit(level_t, (5, 10))
        self.display.blit(self.health, (0, self.life_bar.height * 2))
        self.display.blit(self.shield, (0, self.life_bar.height * 3))
        self.display.blit(self.xp, (0, self.life_bar.height * 4))
        p = player.h_n / player.attribute_now.health
        font = game_master.game.Game.FONT.render(f"{int(player.h_n)}/{int(player.attribute_now.health)}", True, (0, 0, 0))
        if self.life_bar_w * p >= 1:
            surface = pygame.Surface((self.life_bar_w * p, self.life_bar_h))
            surface.fill((255, 0, 0))
            self.display.blit(self.life_bar, (self.w, self.life_bar.height * 2))
            self.display.blit(surface, (self.w + 7 * 2, self.life_bar.height * 2 + 6))
            self.display.blit(font, font.get_rect(center=(self.life_bar.width * 0.5 + self.w, self.life_bar.height * 2.5)))
        else:
            font = game_master.game.Game.FONT.render(f"{0}/{int(player.attribute_now.health)}", True,
                                                     (0, 0, 0))
            self.display.blit(self.life_bar, (self.w, self.life_bar.height * 2))
            self.display.blit(font, font.get_rect(center=(self.life_bar.width * 0.5 + self.w, self.life_bar.height * 2.5)))
        if player.attribute_now.shield:
            p = player.s_n / player.attribute_now.shield
            font = game_master.game.Game.FONT.render(f"{int(player.s_n)}/{int(player.attribute_now.shield)}", True, (0, 0, 0))
            if self.life_bar_w * p >= 1:
                surface = pygame.Surface((self.life_bar_w * p, self.life_bar_h))
                surface.fill((0, 0, 255))
                self.display.blit(self.life_bar, (self.w, self.life_bar.height * 3))
                self.display.blit(surface, (self.w + 7 * 2, self.life_bar.height * 3 + 6))
                self.display.blit(font, font.get_rect(center=(self.life_bar.width * 0.5 + self.w, self.life_bar.height * 3.5)))
            else:
                font = game_master.game.Game.FONT.render(f"{0}/{int(player.attribute_now.shield)}", True, (0, 0, 0))
                self.display.blit(self.life_bar, (self.w, self.life_bar.height * 3))
                self.display.blit(font, font.get_rect(center=(self.life_bar.width * 0.5 + self.w, self.life_bar.height * 3.5)))
        else:
            font = game_master.game.Game.FONT.render(f"{0}/{0}", True, (0, 0, 0))
            self.display.blit(self.life_bar, (self.w, self.life_bar.height * 3))
            self.display.blit(font, font.get_rect(center=(self.life_bar.width * 0.5 + self.w, self.life_bar.height * 3.5)))
        p = (player.level_exp - n_pow(player.exp, player.level-1)) / (player.exp * player.level)
        font = game_master.game.Game.FONT.render(f"{player.level_exp - n_pow(player.exp, player.level-1)}/{player.exp * player.level}", True, (0, 0, 0))
        if self.life_bar_w * p >= 1:
            surface = pygame.Surface((self.life_bar_w * p, self.life_bar_h))
            surface.fill((0, 255, 0))
            self.display.blit(self.life_bar, (self.w, self.life_bar.height * 4))
            self.display.blit(surface, (self.w + 7 * 2, self.life_bar.height * 4 + 6))
            self.display.blit(font, font.get_rect(center=(self.life_bar.width * 0.5 + self.w, self.life_bar.height * 4.5)))
        else:
            font = game_master.game.Game.FONT.render(f"{0}/{player.exp * player.level}", True, (0, 0, 0))
            self.display.blit(self.life_bar, (self.w, self.life_bar.height * 4))
            self.display.blit(font, font.get_rect(center=(self.life_bar.width * 0.5 + self.w, self.life_bar.height * 4.5)))
        pygame.display.get_surface().blit(self.display)


class Bag:
    def __init__(self):
        # 背包是否打开
        self.__state = 0
        # 合成书是否打开
        self.__book_state = 0
        # 合成书界面
        self.__book_ground = pygame.Surface((142, 410))
        # 盔甲变化
        self.__dressed_state = 1
        # 物品栏位置
        self.__inventory_rect = ((1200 - 422) / 2, 900 - 64)
        # 背包位置
        self.__rect = ((1200 - 458) / 2, (900 - 410) / 2)
        # 位置
        self.__book_rect = (self.rect[0] - 142, self.rect[1])
        # 物品栏大小
        self.__inventory = pygame.Surface((422, 44))
        # 背包大小
        self.__background = pygame.Surface((458, 410))
        # 人物框大小
        self.__role_box = pygame.Surface((100, 166))
        # 保存每个格子的surface
        self.__frame = [pygame.Surface((40, 40)) for _ in range(49)]
        # 保存格子的状态, 用于判断是否改变
        self.__frame_state = [0 for _ in range(49)]
        # 保存合成格中物品之前存储的索引
        self.__synthesis = [0 for _ in range(4)]
        # 箭头
        self.arrowhead = pygame.Surface((40, 40))  # game_master.fileManager.game_surface["arrowhead"]
        self.arrowhead.blit(pygame.image.load("res/dir.png").convert_alpha())
        # 颜色, 偏移量
        self.offset = 2
        self.offset_rect = 20
        self.bg = (196, 196, 196)
        self.fg = (138, 138, 138)
        self.sg = (16, 1, 16, 225)
        self.time = 0
        # 保存背包物品和空余数, 0-3是盔甲格子, 4-33是背包格子, 34-43是物品栏格子, 44-47是合成格子, 48是合成的物品格子
        self.__bag = [0 for _ in range(49)]
        self.__free = 40
        self.remaining_quantity = []
        # 物品栏选择框
        self.__box = pygame.Surface((44, 44))
        self.__selection_box = 34
        # 鼠标选择
        self.selection_offset = [0, 0]
        self.selection = 0
        self.selection_index = -1
        self.selection_state = 1
        self.selection_frame = 0
        # 初始化格子
        for i in range(49):
            self.__frame[i].fill(self.fg)
        self.__role_box.fill((0, 0, 0))
        self.__inventory.fill(self.bg)
        self.__box.fill((0, 0, 0))
        self.setup()

    @property
    def state(self):
        return self.__state

    @property
    def book_state(self):
        return self.__book_state

    @property
    def dressed_state(self):
        return self.__dressed_state

    @dressed_state.setter
    def dressed_state(self, ds):
        self.__dressed_state = ds

    @property
    def frame_state(self):
        return self.__frame_state

    @frame_state.setter
    def frame_state(self, frame_state):
        self.__frame_state = frame_state

    @property
    def background(self):
        return self.__background

    @background.setter
    def background(self, background):
        self.__background = background

    @property
    def inventory(self):
        return self.__inventory

    @inventory.setter
    def inventory(self, inventory):
        self.__inventory = inventory

    @property
    def bag(self):
        return self.__bag

    @bag.setter
    def bag(self, bag):
        self.__bag = bag

    @property
    def selection_box(self):
        return self.__selection_box

    @selection_box.setter
    def selection_box(self, sb):
        self.__selection_box = sb

    @property
    def inventory_rect(self):
        return self.__inventory_rect

    @property
    def rect(self):
        return self.__rect

    @property
    def frame(self):
        return self.__frame

    @frame.setter
    def frame(self, frame):
        self.__frame = frame

    def setup(self, index=None):
        # 在index不为None的情况下为更新格子
        if not index:
            self.__background.fill(self.bg)
            self.__book_ground.fill(self.bg)
            self.__inventory.blit(self.__box, (42 * (self.__selection_box - 34), 0))
            for i in range(4):
                self.__background.blit(self.__frame[i], (self.offset_rect, self.offset_rect + (self.offset + 40) * i))
                self.__background.blit(self.__frame[44 + i], (272 + (self.offset + 40) * (i % 2),
                                                              self.offset_rect + self.offset + 40 + (
                                                                      self.offset + 40) * (i // 2)))
            self.__background.blit(self.__role_box, (self.offset_rect * 2 + 40, self.offset_rect))
            self.__background.blit(self.arrowhead, (356, 83))
            self.__background.blit(self.__frame[-1], (398, 83))
            for i in range(30):
                self.__background.blit(self.__frame[4 + i],
                                       (20 + (self.offset + 40) * (i % 10), 206 + (self.offset + 40) * (i // 10)))
            for i in range(10):
                self.__background.blit(self.__frame[34 + i], (20 + (self.offset + 40) * i, 350))
                self.__inventory.blit(self.__frame[34 + i], (2 + (self.offset + 40) * i, 2))
        else:
            for i in index:
                if 0 <= i <= 3:
                    self.__background.blit(self.__frame[i],
                                           (self.offset_rect, self.offset_rect + (self.offset + 40) * i))
                elif 4 <= i <= 33:
                    i -= 4
                    self.__background.blit(self.__frame[4 + i],
                                           (20 + (self.offset + 40) * (i % 10),
                                            206 + (self.offset + 40) * (i // 10)))
                elif 34 <= i <= 43:
                    i -= 34
                    self.__background.blit(self.__frame[34 + i], (20 + (self.offset + 40) * i, 350))
                    self.__inventory.blit(self.__frame[34 + i], (2 + (self.offset + 40) * i, 2))
                elif 44 <= i <= 47:
                    i -= 44
                    self.__background.blit(self.__frame[44 + i], (272 + (self.offset + 40) * (i % 2),
                                                                  self.offset_rect + self.offset + 40 + (
                                                                          self.offset + 40) * (i // 2)))
            if index[-1] >= 44:
                self.__background.blit(self.__frame[-1], (398, 83))

    def open(self):
        self.__state = 1

    def close(self):
        self.__state = 0
        if self.selection_index != -1:
            if self.selection_index == 48:
                t = self.selection
                self.selection = 0
                self.selection_index = -1
                self.selection_offset = [0, 0]
                if not self.put(t):
                    return self.out(obj=t)
            elif self.__bag[self.selection_index]:
                t = self.__bag[self.selection_index]
                n = t.number + self.selection.number
                if t.name == self.selection.name and t.limit >= n:
                    t.number = n
                    self.selection = 0
                    self.selection_index = -1
                    self.selection_offset = [0, 0]
                else:
                    t = self.selection
                    self.selection = 0
                    self.selection_index = -1
                    self.selection_offset = [0, 0]
                    if not self.put(t):
                        return self.out(obj=t)
            else:
                self.__frame_state[self.selection_index] = 1
                self.__bag[self.selection_index] = self.selection
                self.selection = 0
                self.selection_index = -1
                self.selection_offset = [0, 0]
        for i in range(4):
            if self.__synthesis[i]:
                if self.__synthesis[i] == 48:
                    t, n = self.__bag[44 + i], self.__synthesis[i]
                    self.__bag[44 + i] = 0
                    self.__synthesis[i] = 0
                    self.remaining_quantity = self.synthesis()
                    if not self.put(t):
                        return self.out(n)
                elif self.__bag[self.__synthesis[i]]:
                    t = self.__bag[self.__synthesis[i]]
                    n = t.number + self.__bag[44 + i].number
                    if t.name == self.__bag[44 + i].name and t.limit >= n:
                        t.number = n
                        self.__frame_state[self.__synthesis[i]] = 1
                        self.__frame_state[44 + i] = 1
                        self.__bag[44 + i] = 0
                        self.__synthesis[i] = 0
                        self.remaining_quantity = self.synthesis()
                    else:
                        t, n = self.__bag[44 + i], self.__synthesis[i]
                        self.__bag[44 + i] = 0
                        self.__synthesis[i] = 0
                        self.remaining_quantity = self.synthesis()
                        if not self.put(t):
                            return self.out(n)
                else:
                    self.__frame_state[self.__synthesis[i]] = 1
                    self.__frame_state[44 + i] = 1
                    self.__bag[self.__synthesis[i]] = self.__bag[44 + i]
                    self.__bag[44 + i] = 0
                    self.__synthesis[i] = 0
                    self.remaining_quantity = self.synthesis()
        return 0

    def use(self):
        if self.__bag[self.__selection_box]:
            self.__bag[self.__selection_box].use()

    def selected(self, pos: List[int], state, syn=0):
        pos = list(pos)
        pos[0] -= self.__rect[0]
        pos[1] -= self.__rect[1]
        if syn:
            if pos[0] < 0 or pos[0] > 458 or pos[1] < 0 or pos[1] > 410:
                if self.selection_index != -1:
                    t = self.out(obj=self.selection)
                    self.selection_index = -1
                    self.selection = 0
                    self.selection_offset = [0, 0]
                    self.selection_state = 1
                    return t
            elif 20 <= pos[0] <= 438:
                if 206 <= pos[1] <= 330:
                    pos[0] -= 20
                    pos[1] -= 206
                    i, j = 0, 0
                    for i in range(3):
                        pos[1] -= 40
                        if pos[1] <= 0:
                            if pos[0] >= 0:
                                for j in range(10):
                                    pos[0] -= 40
                                    if pos[0] <= 0:
                                        break
                                    elif 0 < pos[0] < 2:
                                        return
                                    pos[0] -= 2
                            break
                        elif 0 < pos[1] < 2:
                            return
                        pos[1] -= 2
                    i = 4 + i * 10 + j
                    if self.selection_index == -1:
                        if self.__bag[i]:
                            self.selection_offset = [pos[0] + 40, pos[1] + 40]
                            self.selection_index = i
                            self.selection_state = 1
                            self.__frame_state[i] = 1
                            if state == pygame.BUTTON_LEFT or self.__bag[i].number == 1:
                                self.selection = self.__bag[i]
                                self.__bag[i] = 0
                            elif state == pygame.BUTTON_RIGHT:
                                mid = self.__bag[i].number // 2
                                self.__bag[i].number -= mid
                                self.selection = className.GOODS[self.__bag[i].NAME](mid)
                    else:
                        if self.__bag[i]:
                            if self.selection.name != self.__bag[i].name or self.__bag[i].limit == self.__bag[i].number:
                                self.selection_index = i
                                t = self.selection
                                self.selection = self.__bag[i]
                                self.__bag[i] = t
                            else:
                                if state == pygame.BUTTON_LEFT or self.selection.number == 1:
                                    t = self.selection.number + self.__bag[i].number
                                    if t <= self.__bag[i].limit:
                                        self.__bag[i].number = t
                                        self.selection = 0
                                        self.selection_index = -1
                                        self.selection_offset = 0
                                    else:
                                        t -= self.__bag[i].limit
                                        self.__bag[i].number = self.__bag[i].limit
                                        self.selection.number = t
                                elif state == pygame.BUTTON_RIGHT:
                                    t = 1 + self.__bag[i].number
                                    if t <= self.__bag[i].limit:
                                        self.__bag[i].number = t
                                        self.selection.number -= 1
                                    else:
                                        t = self.__bag[i].limit - self.__bag[i].number
                                        self.__bag[i].number = self.__bag[i].limit
                                        self.selection.number -= t
                        else:
                            if state == pygame.BUTTON_LEFT or self.selection.number == 1:
                                self.__bag[i] = self.selection
                                self.selection_offset = [0, 0]
                                self.selection_index = -1
                                self.selection = 0
                            elif state == pygame.BUTTON_RIGHT:
                                self.__bag[i] = className.GOODS[self.selection.NAME](1)
                                self.selection.number -= 1
                        self.selection_state = 1
                        self.__frame_state[i] = 1
                elif 350 <= pos[1] <= 390:
                    pos[0] -= 20
                    i = 0
                    for i in range(10):
                        pos[0] -= 40
                        if pos[0] <= 0:
                            break
                        elif 0 < pos[0] < 2:
                            return
                        pos[0] -= 2
                    i = 34 + i
                    if self.selection_index == -1:
                        if self.__bag[i]:
                            self.selection_offset = [pos[0] + 40, pos[1] - 350]
                            self.selection_index = i
                            self.selection_state = 1
                            self.__frame_state[i] = 1
                            if state == pygame.BUTTON_LEFT or self.__bag[i].number == 1:
                                self.selection = self.__bag[i]
                                self.__bag[i] = 0
                            elif state == pygame.BUTTON_RIGHT:
                                mid = self.__bag[i].number // 2
                                self.__bag[i].number -= mid
                                self.selection = className.GOODS[self.__bag[i].NAME](mid)
                    else:
                        if self.__bag[i]:
                            if self.selection.name != self.__bag[i].name or self.__bag[i].limit == self.__bag[i].number:
                                self.selection_index = i
                                t = self.selection
                                self.selection = self.__bag[i]
                                self.__bag[i] = t
                            else:
                                if state == pygame.BUTTON_LEFT or self.selection.number == 1:
                                    t = self.selection.number + self.__bag[i].number
                                    if t <= self.__bag[i].limit:
                                        self.__bag[i].number = t
                                        self.selection = 0
                                        self.selection_index = -1
                                        self.selection_offset = 0
                                    else:
                                        t -= self.__bag[i].limit
                                        self.__bag[i].number = self.__bag[i].limit
                                        self.selection.number = t
                                elif state == pygame.BUTTON_RIGHT:
                                    t = 1 + self.__bag[i].number
                                    if t <= self.__bag[i].limit:
                                        self.__bag[i].number = t
                                        self.selection.number -= 1
                                    else:
                                        t = self.__bag[i].limit - self.__bag[i].number
                                        self.__bag[i].number = self.__bag[i].limit
                                        self.selection.number -= t
                        else:
                            if state == pygame.BUTTON_LEFT or self.selection.number == 1:
                                self.__bag[i] = self.selection
                                self.selection_offset = [0, 0]
                                self.selection_index = -1
                                self.selection = 0
                            elif state == pygame.BUTTON_RIGHT:
                                self.__bag[i] = className.GOODS[self.selection.NAME](1)
                                self.selection.number -= 1
                        self.selection_state = 1
                        self.__frame_state[i] = 1
        elif pos[0] < 0 or pos[0] > 458 or pos[1] < 0 or pos[1] > 410:
            if self.selection_index != -1:
                t = self.out(obj=self.selection)
                self.selection_index = -1
                self.selection = 0
                self.selection_offset = [0, 0]
                self.selection_state = 1
                return t
        elif 20 <= pos[0] <= 60 and 20 <= pos[1] <= 186:
            print(222)
            pos[1] -= 20
            i = 0
            for i in range(4):
                pos[1] -= 40
                if pos[1] <= 0:
                    break
                elif 0 < pos[1] < 2:
                    return
                pos[1] -= 2
            if self.selection_index == -1:
                if self.__bag[i]:
                    self.selection_offset = [pos[0] - 20, pos[1] + 40]
                    self.selection_index = i
                    self.selection = self.__bag[i]
                    self.__bag[i] = 0
                    self.__frame_state[i] = 1
                    self.selection_state = 1
                    self.__dressed_state = 1
            else:
                if self.selection.dressed:
                    if self.__bag[i]:
                        self.selection_index = i
                        t = self.selection
                        self.selection = self.__bag[i]
                        self.__bag[i] = t
                    else:
                        self.__bag[i] = self.selection
                        self.selection_offset = [0, 0]
                        self.selection_index = -1
                        self.selection = 0
                    self.selection_state = 1
                    self.__frame_state[i] = 1
                    self.__dressed_state = 1
        elif 272 <= pos[0] <= 356 and 62 <= pos[1] <= 144:
            print(333)
            pos[0] -= 272
            pos[1] -= 62
            i, j = 0, 0
            for i in range(2):
                pos[1] -= 40
                if pos[1] <= 0:
                    if pos[0] >= 0:
                        for j in range(2):
                            pos[0] -= 40
                            if pos[0] <= 0:
                                break
                            elif 0 < pos[0] < 2:
                                return
                            pos[0] -= 2
                    break
                elif 0 < pos[1] < 2:
                    return
                pos[1] -= 2
            k = i
            i = 44 + i * 2 + j
            if self.selection_index == -1:
                if self.__bag[i]:
                    self.selection_offset = [pos[0] + 40, pos[1] + 40]
                    self.selection_index = self.__synthesis[k * 2 + j]
                    if state == pygame.BUTTON_LEFT or self.__bag[i].number == 1:
                        self.selection = self.__bag[i]
                        self.__synthesis[k * 2 + j] = 0
                        self.__bag[i] = 0
                    elif state == pygame.BUTTON_RIGHT:
                        mid = self.__bag[i].number // 2
                        self.selection = className.GOODS[self.__bag[i].NAME](mid)
                        self.__bag[i].number -= mid
                    self.__frame_state[i] = 1
                    self.selection_state = 1
                    self.remaining_quantity = self.synthesis()
            else:
                if self.__bag[i]:
                    if self.selection.name != self.__bag[i].name or self.__bag[i].number == self.__bag[i].limit:
                        n = self.__synthesis[k * 2 + j]
                        self.__synthesis[k * 2 + j] = self.selection_index
                        self.selection_index = n
                        t = self.selection
                        self.selection = self.__bag[i]
                        self.__bag[i] = t
                    elif state == pygame.BUTTON_LEFT:
                        t = self.selection.number + self.__bag[i].number
                        if self.__bag[i].limit >= t:
                            self.__bag[i].number = t
                            self.selection = 0
                            self.selection_index = -1
                        else:
                            t -= self.__bag[i].limit
                            self.__bag[i].number = self.__bag[i].limit
                            self.selection.number = t
                    elif state == pygame.BUTTON_RIGHT:
                        t = 1 + self.__bag[i].number
                        if self.__bag[i].limit >= t:
                            self.__bag[i].number = t
                            self.selection.number -= 1
                        else:
                            t = self.__bag[i].limit - self.__bag[i].number
                            self.__bag[i].number = self.__bag[i].limit
                            self.selection.number -= t
                else:
                    if state == pygame.BUTTON_LEFT or self.selection.number == 1:
                        self.__bag[i] = self.selection
                        self.__synthesis[k * 2 + j] = self.selection_index
                        self.selection_offset = [0, 0]
                        self.selection_index = -1
                        self.selection = 0
                    elif state == pygame.BUTTON_RIGHT:
                        self.__bag[i] = className.GOODS[self.selection.NAME](1)
                        self.__synthesis[k * 2 + j] = self.selection_index
                        self.selection.number -= 1
                self.selection_state = 1
                self.__frame_state[i] = 1
                self.remaining_quantity = self.synthesis()
        elif 398 <= pos[0] <= 438 and 83 <= pos[1] <= 123:
            print(444)
            if self.__bag[48]:
                if self.selection_index == -1:
                    self.selection_offset = [pos[0] - 398, pos[1] - 83]
                    self.selection_index = 48
                    self.selection_state = 1
                    if state == pygame.BUTTON_LEFT:
                        self.selection = className.GOODS[self.__bag[48].NAME](self.remaining_quantity[-2])
                        self.remaining_quantity[-1] -= 1
                        for i in range(len(self.remaining_quantity) - 2):
                            self.__bag[self.remaining_quantity[i][1]].number -= self.remaining_quantity[i][0]
                            if not self.__bag[self.remaining_quantity[i][1]].number:
                                self.__bag[self.remaining_quantity[i][1]] = 0
                                self.__synthesis[self.remaining_quantity[i][1] - 44] = 0
                            self.__frame_state[self.remaining_quantity[i][1]] = 1
                        if not self.remaining_quantity[-1]:
                            self.remaining_quantity = self.synthesis()
                    elif state == pygame.BUTTON_RIGHT:
                        if self.__bag[48].limit >= self.remaining_quantity[-2] * self.remaining_quantity[-1]:
                            self.selection = self.__bag[48]
                            self.selection.number = self.remaining_quantity[-2] * self.remaining_quantity[-1]
                        else:
                            self.selection = className.GOODS[self.__bag[48].NAME](self.__bag[48].limit)
                            t = self.remaining_quantity[-2] * self.remaining_quantity[-1] - self.__bag[48].limit
                            group = t // self.__bag[48].limit
                            t -= group * self.__bag[48].limit
                            for i in range(group):
                                self.put(className.GOODS[self.__bag[48].NAME](self.__bag[48].limit))
                            if t:
                                self.put(className.GOODS[self.__bag[48].NAME](t))
                        self.__bag[48] = 0
                        self.__frame_state[48] = 1
                        for i in range(len(self.remaining_quantity) - 2):
                            self.__bag[self.remaining_quantity[i][1]].number -= self.remaining_quantity[i][0] * \
                                                                                self.remaining_quantity[-1]
                            if not self.__bag[self.remaining_quantity[i][1]].number:
                                self.__bag[self.remaining_quantity[i][1]] = 0
                                self.__synthesis[self.remaining_quantity[i][1] - 44] = 0
                            self.__frame_state[self.remaining_quantity[i][1]] = 1
                        self.remaining_quantity = self.synthesis()
                elif self.selection.name == self.__bag[48].name and self.__bag[48].number != self.__bag[48].limit:
                    if state == pygame.BUTTON_LEFT and self.selection.number + self.remaining_quantity[-2] <= self.selection.limit:
                        self.selection.number += self.remaining_quantity[-2]
                        self.selection_state = 1
                        self.remaining_quantity[-1] -= 1
                        for i in range(len(self.remaining_quantity) - 2):
                            self.__bag[self.remaining_quantity[i][1]].number -= self.remaining_quantity[i][0]
                            if not self.__bag[self.remaining_quantity[i][1]].number:
                                self.__bag[self.remaining_quantity[i][1]] = 0
                                self.__synthesis[self.remaining_quantity[i][1] - 44] = 0
                            self.__frame_state[self.remaining_quantity[i][1]] = 1
                        if not self.remaining_quantity[-1]:
                            self.remaining_quantity = self.synthesis()
                    elif state == pygame.BUTTON_RIGHT:
                        if self.selection.limit - self.selection.number >= self.remaining_quantity[-2] * \
                                self.remaining_quantity[-1]:
                            self.selection.number += self.remaining_quantity[-2] * self.remaining_quantity[-1]
                        else:
                            t = self.remaining_quantity[-2] * self.remaining_quantity[
                                -1] - self.selection.limit + self.selection.number
                            self.selection.number = self.selection.limit
                            group = t // self.selection.limit
                            t -= group * self.selection.limit
                            for i in range(group):
                                self.put(className.GOODS[self.selection.NAME](self.selection.limit))
                            if t:
                                self.put(className.GOODS[self.selection.NAME](t))
                        self.selection_state = 1
                        self.__bag[48] = 0
                        self.__frame_state[48] = 1
                        for i in range(len(self.remaining_quantity) - 2):
                            self.__bag[self.remaining_quantity[i][1]].number -= self.remaining_quantity[i][0] * \
                                                                                self.remaining_quantity[-1]
                            if not self.__bag[self.remaining_quantity[i][1]].number:
                                self.__bag[self.remaining_quantity[i][1]] = 0
                                self.__synthesis[self.remaining_quantity[i][1] - 44] = 0
                            self.__frame_state[self.remaining_quantity[i][1]] = 1
                        self.remaining_quantity = self.synthesis()
        elif 20 <= pos[0] <= 438:
            if 206 <= pos[1] <= 330:
                print(1)
                pos[0] -= 20
                pos[1] -= 206
                i, j = 0, 0
                for i in range(3):
                    pos[1] -= 40
                    if pos[1] <= 0:
                        if pos[0] >= 0:
                            for j in range(10):
                                pos[0] -= 40
                                if pos[0] <= 0:
                                    break
                                elif 0 < pos[0] < 2:
                                    return
                                pos[0] -= 2
                        break
                    elif 0 < pos[1] < 2:
                        return
                    pos[1] -= 2
                i = 4 + i * 10 + j
                if self.selection_index == -1:
                    if self.__bag[i]:
                        self.selection_offset = [pos[0] + 40, pos[1] + 40]
                        self.selection_index = i
                        self.selection_state = 1
                        self.__frame_state[i] = 1
                        if state == pygame.BUTTON_LEFT or self.__bag[i].number == 1:
                            self.selection = self.__bag[i]
                            self.__bag[i] = 0
                        elif state == pygame.BUTTON_RIGHT:
                            mid = self.__bag[i].number // 2
                            self.__bag[i].number -= mid
                            self.selection = className.GOODS[self.__bag[i].NAME](mid)
                else:
                    if self.__bag[i]:
                        if self.selection.name != self.__bag[i].name or self.__bag[i].limit == self.__bag[i].number:
                            self.selection_index = i
                            t = self.selection
                            self.selection = self.__bag[i]
                            self.__bag[i] = t
                        else:
                            if state == pygame.BUTTON_LEFT or self.selection.number == 1:
                                t = self.selection.number + self.__bag[i].number
                                if t <= self.__bag[i].limit:
                                    self.__bag[i].number = t
                                    self.selection = 0
                                    self.selection_index = -1
                                    self.selection_offset = 0
                                else:
                                    t -= self.__bag[i].limit
                                    self.__bag[i].number = self.__bag[i].limit
                                    self.selection.number = t
                            elif state == pygame.BUTTON_RIGHT:
                                t = 1 + self.__bag[i].number
                                if t <= self.__bag[i].limit:
                                    self.__bag[i].number = t
                                    self.selection.number -= 1
                                else:
                                    t = self.__bag[i].limit - self.__bag[i].number
                                    self.__bag[i].number = self.__bag[i].limit
                                    self.selection.number -= t
                    else:
                        if state == pygame.BUTTON_LEFT or self.selection.number == 1:
                            self.__bag[i] = self.selection
                            self.selection_offset = [0, 0]
                            self.selection_index = -1
                            self.selection = 0
                        elif state == pygame.BUTTON_RIGHT:
                            self.__bag[i] = className.GOODS[self.selection.NAME](1)
                            self.selection.number -= 1
                    self.selection_state = 1
                    self.__frame_state[i] = 1
            elif 350 <= pos[1] <= 390:
                print(2)
                pos[0] -= 20
                i = 0
                for i in range(10):
                    pos[0] -= 40
                    if pos[0] <= 0:
                        break
                    elif 0 < pos[0] < 2:
                        return
                    pos[0] -= 2
                i = 34 + i
                if self.selection_index == -1:
                    if self.__bag[i]:
                        self.selection_offset = [pos[0] + 40, pos[1] - 350]
                        self.selection_index = i
                        self.selection_state = 1
                        self.__frame_state[i] = 1
                        if state == pygame.BUTTON_LEFT or self.__bag[i].number == 1:
                            self.selection = self.__bag[i]
                            self.__bag[i] = 0
                        elif state == pygame.BUTTON_RIGHT:
                            mid = self.__bag[i].number // 2
                            self.__bag[i].number -= mid
                            self.selection = className.GOODS[self.__bag[i].NAME](mid)
                else:
                    if self.__bag[i]:
                        if self.selection.name != self.__bag[i].name or self.__bag[i].limit == self.__bag[i].number:
                            self.selection_index = i
                            t = self.selection
                            self.selection = self.__bag[i]
                            self.__bag[i] = t
                        else:
                            if state == pygame.BUTTON_LEFT or self.selection.number == 1:
                                t = self.selection.number + self.__bag[i].number
                                if t <= self.__bag[i].limit:
                                    self.__bag[i].number = t
                                    self.selection = 0
                                    self.selection_index = -1
                                    self.selection_offset = 0
                                else:
                                    t -= self.__bag[i].limit
                                    self.__bag[i].number = self.__bag[i].limit
                                    self.selection.number = t
                            elif state == pygame.BUTTON_RIGHT:
                                t = 1 + self.__bag[i].number
                                if t <= self.__bag[i].limit:
                                    self.__bag[i].number = t
                                    self.selection.number -= 1
                                else:
                                    t = self.__bag[i].limit - self.__bag[i].number
                                    self.__bag[i].number = self.__bag[i].limit
                                    self.selection.number -= t
                    else:
                        if state == pygame.BUTTON_LEFT or self.selection.number == 1:
                            self.__bag[i] = self.selection
                            self.selection_offset = [0, 0]
                            self.selection_index = -1
                            self.selection = 0
                        elif state == pygame.BUTTON_RIGHT:
                            self.__bag[i] = className.GOODS[self.selection.NAME](1)
                            self.selection.number -= 1
                    self.selection_state = 1
                    self.__frame_state[i] = 1

    def get_message(self, pos: List[int], syn=0):
        pos = list(pos)
        offset = pos.copy()
        pos[0] -= self.__rect[0]
        pos[1] -= self.__rect[1]
        if syn:
            if 20 <= pos[0] <= 438:
                if 206 <= pos[1] <= 330:
                    pos[0] -= 20
                    pos[1] -= 206
                    i, j = 0, 0
                    for i in range(3):
                        pos[1] -= 40
                        if pos[1] <= 0:
                            if pos[0] >= 0:
                                for j in range(10):
                                    pos[0] -= 40
                                    if pos[0] <= 0:
                                        break
                                    elif 0 < pos[0] < 2:
                                        return
                                    pos[0] -= 2
                            break
                        elif 0 < pos[1] < 2:
                            return
                        pos[1] -= 2
                    i = 4 + i * 10 + j
                    if self.__bag[i]:
                        text = f"{self.__bag[i].name}"
                        for a in range(9):
                            text += f"\n{game_master.gameObject.ATTRIBUTE[a]}:{self.__bag[i].attribute[a]}"
                        font = game_master.game.Game.FONT.render(text, True, (255, 255, 255)).convert_alpha()
                        surf = pygame.Surface((font.width + 10, font.height + 10)).convert_alpha()
                        surf.fill(self.sg)
                        surf.blit(font, (5, 5))
                        text = f"{self.__bag[i].name}"
                        font = game_master.game.Game.FONT.render(text, True, (83, 250, 250)).convert_alpha()
                        surf.blit(font, (5, 5))
                        pygame.display.get_surface().blit(surf, offset)
                elif 350 <= pos[1] <= 390:
                    pos[0] -= 20
                    i = 0
                    for i in range(10):
                        pos[0] -= 40
                        if pos[0] <= 0:
                            break
                        elif 0 < pos[0] < 2:
                            return
                        pos[0] -= 2
                    i = 34 + i
                    if self.__bag[i]:
                        text = f"{self.__bag[i].name}"
                        for a in range(9):
                            text += f"\n{game_master.gameObject.ATTRIBUTE[a]}:{self.__bag[i].attribute[a]}"
                        font = game_master.game.Game.FONT.render(text, True, (255, 255, 255)).convert_alpha()
                        surf = pygame.Surface((font.width + 10, font.height + 10)).convert_alpha()
                        surf.fill(self.sg)
                        surf.blit(font, (5, 5))
                        text = f"{self.__bag[i].name}"
                        font = game_master.game.Game.FONT.render(text, True, (83, 250, 250)).convert_alpha()
                        surf.blit(font, (5, 5))
                        pygame.display.get_surface().blit(surf, offset)
        elif 20 <= pos[0] <= 60 and 20 <= pos[1] <= 186:
            print(222)
            pos[1] -= 20
            i = 0
            for i in range(4):
                pos[1] -= 40
                if pos[1] <= 0:
                    break
                elif 0 < pos[1] < 2:
                    return
                pos[1] -= 2
            if self.__bag[i]:
                text = f"{self.__bag[i].name}"
                for a in range(9):
                    text += f"\n{game_master.gameObject.ATTRIBUTE[a]}:{self.__bag[i].attribute[a]}"
                font = game_master.game.Game.FONT.render(text, True, (255, 255, 255)).convert_alpha()
                surf = pygame.Surface((font.width + 10, font.height + 10)).convert_alpha()
                surf.fill(self.sg)
                surf.blit(font, (5, 5))
                text = f"{self.__bag[i].name}"
                font = game_master.game.Game.FONT.render(text, True, (83, 250, 250)).convert_alpha()
                surf.blit(font, (5, 5))
                pygame.display.get_surface().blit(surf, offset)
        elif 272 <= pos[0] <= 356 and 62 <= pos[1] <= 144:
            print(333)
            pos[0] -= 272
            pos[1] -= 62
            i, j = 0, 0
            for i in range(2):
                pos[1] -= 40
                if pos[1] <= 0:
                    if pos[0] >= 0:
                        for j in range(2):
                            pos[0] -= 40
                            if pos[0] <= 0:
                                break
                            elif 0 < pos[0] < 2:
                                return
                            pos[0] -= 2
                    break
                elif 0 < pos[1] < 2:
                    return
                pos[1] -= 2
            i = 44 + i * 2 + j
            if self.__bag[i]:
                text = f"{self.__bag[i].name}"
                for a in range(9):
                    text += f"\n{game_master.gameObject.ATTRIBUTE[a]}:{self.__bag[i].attribute[a]}"
                font = game_master.game.Game.FONT.render(text, True, (255, 255, 255)).convert_alpha()
                surf = pygame.Surface((font.width + 10, font.height + 10)).convert_alpha()
                surf.fill(self.sg)
                surf.blit(font, (5, 5))
                text = f"{self.__bag[i].name}"
                font = game_master.game.Game.FONT.render(text, True, (83, 250, 250)).convert_alpha()
                surf.blit(font, (5, 5))
                pygame.display.get_surface().blit(surf, offset)
        elif 398 <= pos[0] <= 438 and 83 <= pos[1] <= 123:
            if self.__bag[48]:
                text = f"{self.__bag[48].name}"
                for a in range(9):
                    text += f"\n{game_master.gameObject.ATTRIBUTE[a]}:{self.__bag[48].attribute[a]}"
                font = game_master.game.Game.FONT.render(text, True, (255, 255, 255)).convert_alpha()
                surf = pygame.Surface((font.width + 10, font.height + 10)).convert_alpha()
                surf.fill(self.sg)
                surf.blit(font, (5, 5))
                text = f"{self.__bag[i].name}"
                font = game_master.game.Game.FONT.render(text, True, (83, 250, 250)).convert_alpha()
                surf.blit(font, (5, 5))
                pygame.display.get_surface().blit(surf, offset)
        elif 20 <= pos[0] <= 438:
            if 206 <= pos[1] <= 330:
                pos[0] -= 20
                pos[1] -= 206
                i, j = 0, 0
                for i in range(3):
                    pos[1] -= 40
                    if pos[1] <= 0:
                        if pos[0] >= 0:
                            for j in range(10):
                                pos[0] -= 40
                                if pos[0] <= 0:
                                    break
                                elif 0 < pos[0] < 2:
                                    return
                                pos[0] -= 2
                        break
                    elif 0 < pos[1] < 2:
                        return
                    pos[1] -= 2
                i = 4 + i * 10 + j
                if self.__bag[i]:
                    text = f"{self.__bag[i].name}"
                    for a in range(9):
                        text += f"\n{game_master.gameObject.ATTRIBUTE[a]}:{self.__bag[i].attribute[a]}"
                    font = game_master.game.Game.FONT.render(text, True, (255, 255, 255)).convert_alpha()
                    surf = pygame.Surface((font.width + 10, font.height + 10)).convert_alpha()
                    surf.fill(self.sg)
                    surf.blit(font, (5, 5))
                    text = f"{self.__bag[i].name}"
                    font = game_master.game.Game.FONT.render(text, True, (83, 250, 250)).convert_alpha()
                    surf.blit(font, (5, 5))
                    pygame.display.get_surface().blit(surf, offset)
            elif 350 <= pos[1] <= 390:
                pos[0] -= 20
                i = 0
                for i in range(10):
                    pos[0] -= 40
                    if pos[0] <= 0:
                        break
                    elif 0 < pos[0] < 2:
                        return
                    pos[0] -= 2
                i = 34 + i
                if self.__bag[i]:
                    text = f"{self.__bag[i].name}"
                    for a in range(9):
                        text += f"\n{game_master.gameObject.ATTRIBUTE[a]}:{self.__bag[i].attribute[a]}"
                    font = game_master.game.Game.FONT.render(text, True, (255, 255, 255)).convert_alpha()
                    surf = pygame.Surface((font.width + 10, font.height + 10)).convert_alpha()
                    surf.fill(self.sg)
                    surf.blit(font, (5, 5))
                    text = f"{self.__bag[i].name}"
                    font = game_master.game.Game.FONT.render(text, True, (83, 250, 250)).convert_alpha()
                    surf.blit(font, (5, 5))
                    pygame.display.get_surface().blit(surf, offset)

    def put(self, obj):
        for i in range(40):
            if self.bag[4 + i] and self.bag[4 + i].name == obj.name and self.bag[4 + i].limit > self.bag[4 + i].number:
                self.__frame_state[4 + i] = 1
                t = self.__bag[4 + i]
                n = t.number + obj.number
                if t.limit >= n:
                    t.number = n
                    return 1
                else:
                    obj.number -= t.limit - t.number
                    t.number = t.limit
        if self.__free:
            for i in range(40):
                if not self.__bag[4 + i]:
                    self.__bag[4 + i] = obj
                    self.__frame_state[4 + i] = 1
                    self.__free -= 1
                    return 1
        return 0

    def out(self, index=-1, obj=None):
        if obj:
            return obj
        if index != -1:
            t = self.__bag[index]
            self.__frame_state[index] = 1
            self.__bag[index] = 0
            self.__free += 1
            return t
        return 0

    def synthesis(self):
        number = []
        if self.__bag[-1]:
            self.__bag[-1] = 0
            self.__frame_state[-1] = 1
        for i in range(4):
            if self.__bag[44 + i]:
                number.append(i)
        if not number:
            return 0
        temp = []
        obj = 0
        for g in game_master.synthesis.PLAYER_SYNTHESIS_LIST:
            l = len(g) - 1
            if len(number) == l:
                state = 1
                if l == 1:
                    if g[0][0] != self.__bag[44 + number[0]].name or g[0][1] > self.__bag[44 + number[0]].number:
                        state = 0
                else:
                    if g[0][-1] == -1:
                        d = number[0] - g[0][-1]
                        for i in range(l):
                            if (d != number[i] - g[i][-1] or self.__bag[44 + number[i]].name != g[i][0] or
                                    self.__bag[44 + number[i]].number < g[i][1]):
                                state = 0
                                break
                    else:
                        for i in range(l):
                            if (number[i] != g[i][2] or self.__bag[44 + number[i]].name != g[i][0] or
                                    self.__bag[44 + number[i]].number < g[i][1]):
                                state = 0
                                break
                if state:
                    t = []
                    for i in range(l):
                        temp.append([g[i][1], number[i] + 44])
                        t.append(self.__bag[number[i] + 44].number // g[i][1])
                    temp.append(g[-1][1])
                    temp.append(min(t))
                    obj = g
                    break
        if obj:
            self.__bag[-1] = items.className.GOODS[obj[-1][0]](number=obj[-1][1])
            self.__frame_state[-1] = 1
            print(temp)
            return temp
        return 0

    def update_inventory(self):
        if self.selection_box < 34:
            self.selection_box = 43
        elif self.selection_box > 43:
            self.selection_box = 34
        self.__inventory.fill(self.bg)
        self.__inventory.blit(self.__box, (42 * (self.__selection_box - 34), 0))
        for i in range(10):
            self.__inventory.blit(self.__frame[34 + i], (2 + (self.offset + 40) * i, 2))
        self.time = 3

    def update(self, image, dt):
        self.__role_box.fill((0, 0, 0))
        max_v = min(self.__role_box.width / image.width, self.__role_box.height / image.height)
        image = pygame.transform.scale(image, (image.width * max_v, image.height * max_v))
        rect = image.get_rect(center=(self.__role_box.width / 2, self.__role_box.height / 2))
        self.__role_box.blit(image, rect)
        self.__background.blit(self.__role_box, (self.offset_rect * 2 + 40, self.offset_rect))
        if self.remaining_quantity:
            if not self.remaining_quantity[-1]:
                self.__bag[48] = 0
                self.__frame_state[48] = 1
                self.remaining_quantity = 0
        temp = []
        for i in range(49):
            if self.__bag[i]:
                if not self.__bag[i]:
                    self.__bag[i] = 0
                    self.__frame_state[i] = 1
            if self.__frame_state[i]:
                self.__frame[i].fill(self.fg)
                if self.__bag[i]:
                    # pygame.transform.scale(self.__bag[i].surface, (40, 40), self.__frame[i])
                    self.__frame[i].blit(self.__bag[i].surface)
                    if self.__bag[i].number > 1:
                        font = game_master.game.Game.FONT.render(str(self.__bag[i].number), True,
                                                                 (255, 255, 255)).convert_alpha()
                        rect = font.get_rect(bottomright=(40, 40))
                        self.__frame[i].blit(font, rect)
                self.__frame_state[i] = 0
                temp.append(i)
        self.setup(temp)
        if self.time > 0:
            self.time -= dt
        return self.__bag[:4]

    def render_selection(self):
        if self.selection_state:
            self.selection_state = 0
            if self.selection_index != -1:
                self.selection_frame = self.selection.surface.copy()
                if self.selection.number > 1:
                    font = game_master.game.Game.FONT.render(str(self.selection.number), True,
                                                             (255, 255, 255)).convert_alpha()
                    rect = font.get_rect(bottomright=(40, 40))
                    self.selection_frame.blit(font, rect)
        if self.selection_index != -1:
            pos = pygame.mouse.get_pos()
            pygame.display.get_surface().blit(self.selection_frame, (
                pos[0] - self.selection_offset[0], pos[1] - self.selection_offset[1]))

    def render_inventory(self):
        pygame.display.get_surface().blit(self.__inventory, self.__inventory_rect)
        if self.time > 0 and self.__bag[self.__selection_box]:
            font = game_master.game.Game.FONT.render(f"{self.__bag[self.__selection_box].name}", True, (83, 250, 250)).convert_alpha()
            surf = pygame.Surface((font.width+10, font.height+10)).convert_alpha()
            if self.time < 2.55:
                surf.set_alpha(round(self.time * 100))
            surf.fill(self.sg)
            surf.blit(font, (5, 5))
            rect = self.__inventory_rect[0] + self.inventory.width / 2, self.__inventory_rect[1] - 50 - surf.height / 2
            rect = surf.get_rect(center=rect)
            pygame.display.get_surface().blit(surf, rect)

    def render(self):
        if self.__state:
            pygame.display.get_surface().blit(self.__background, self.__rect)
            if self.__book_state:
                pygame.display.get_surface().blit(self.__book_ground, self.__book_rect)
            self.get_message(list(pygame.mouse.get_pos()))
            self.render_selection()
