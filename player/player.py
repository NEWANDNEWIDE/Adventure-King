import random
from typing import Optional
import pygame
import game_master.gameObject
import game_master.fileManager
import settings


class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.__display = pygame.display.get_surface()
        self.__offset = [0, 0]

    def custom_draw(self, rect):
        self.__offset = rect
        self.__offset[0] -= settings.WIDTH // 2
        self.__offset[1] -= settings.HEIGHT // 2
        for s in sorted(self.sprites(), key=lambda s: s.attribute.rect[1]):
            s.attribute.rect[0] -= self.__offset[0]
            s.attribute.rect[1] -= self.__offset[1]
            self.__display.blit(s.image, s.attribute.rect)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)
        self.__surface = game_master.fileManager.game_surface["player"]
        self.__l = (self.__surface[0] - 1) // 4
        self.__vec2 = [0, 0]

        self.index = 1
        self.image = self.__surface[self.index]
        self.attribute = game_master.gameObject.GameObject()
        self.spawn_point = pos
        self.attribute.rect = pos

        # 头 胸 腿 靴
        self.armor = [0, 0, 0, 0]

        self.w = self.__surface[1].width
        self.h = self.__surface[1].height
        self.bag = Bag((100, 100), (0, 0), 20, 20)

        self.attribute.health = 100
        self.attribute.attack = 5
        self.attribute.attack_speed = 1
        self.attribute.critical_strike_chance = 0.05
        self.attribute.critical_strike_damage = 1.5
        self.attribute.reach_distance = 1

        self.attack_box = self.attribute.reach_distance * 50

    @property
    def vec2(self):
        return self.__vec2

    @vec2.setter
    def vec2(self, vec2):
        self.__vec2 = vec2

    def attack(self):
        chance = self.attribute.critical_strike_chance + self.bag.bag[self.bag.selection_box].critical_strike_chance
        damage = self.attribute.attack + self.bag.bag[self.bag.selection_box].attack
        if self.attribute.critical_strike_chance < 1:
            r = random.random()
            damage = damage * self.attribute.critical_strike_damage if chance >= r else damage
        else:
            damage = damage * self.attribute.critical_strike_damage


    def use(self):
        self.bag.bag[self.bag.selection_box].use()

    def move(self, dt):
        self.rect[0] += self.vec2[0] * self.attribute.move_speed * dt
        self.rect[1] += self.vec2[1] * self.attribute.move_speed * dt

    def update(self, dt):
        self.move(dt)


class Bag:
    def __init__(self, rect, offset, w, h):
        self.bag: Optional[game_master.gameObject.WoodenSword, int] = [0 for _ in range(36)]
        self.__free = 36
        self.__synthesis = [0 for _ in range(4)]
        self.__synthesis_index = [-1 for _ in range(4)]
        self.__armor_frame = [0 for _ in range(4)]
        self.__armor_frame_index = [-1 for _ in range(4)]
        self.__surface: pygame.Surface = game_master.fileManager.game_surface["bag"]
        self.__temp: pygame.Surface = game_master.fileManager.game_surface["bag"]
        self.__rect = rect
        self.__offset = offset
        self.selection_box = 27
        self.x = rect[0] + offset[0]
        self.y = rect[1] + offset[1]
        self.w = w
        self.h = h
        self.state = 0
        self.__full = 0
        self.__selected = 0
        self.__selected_index = -1
        self.__selected_obj = 0

    def open(self):
        self.state = 1

    def close(self):
        self.state = 0
        if self.__selected:
            t = self.__selected_obj.number + self.bag[self.__selected_index].number
            if self.bag[self.__selected_index].limit >= t:
                self.bag[self.__selected_index].number = t
            elif not self.__full:
                self.put(self.__selected_obj)
            else:
                self.out(self.__selected_obj)
            self.__selected = 0
            self.__selected_index = -1
            self.__selected_obj = 0
        for i in range(4):
            if self.__synthesis_index[i] != -1:
                t = self.__synthesis[i].number + self.bag[self.__synthesis_index].number
                if self.bag[self.__synthesis_index].limit >= t:
                    self.bag[self.__synthesis_index].number = t
                elif not self.__full:
                    self.put(self.__synthesis[i])
                else:
                    self.put(self.__synthesis[i])
                self.__synthesis_index[i] = -1
                self.__synthesis[i] = 0

    def selected(self, pos, state):
        """
        state是背包的打开状态，1为打开，x，y分别是背包左上角的格子的位置，w, h是格子的宽高
        :param pos: 当鼠标点击时的位置
        :return: None
        """
        if self.state:
            if self.x < pos[0] < self.x + self.w * 9 and self.y < pos[1] < self.y + self.h * 4:
                pos[0] -= self.x
                pos[1] -= self.y
                pos[0] //= self.w
                pos[1] //= self.h
                index = pos[1] * 9 + pos[0]
                if not self.__selected:
                    if self.bag[index]:
                        self.__selected = 1
                        self.__selected_index = index
                        self.__selected_obj = self.bag[index]
                        self.bag[index] = 0
                        self.__free += 1
                        self.__full = 0
                else:
                    if self.bag[index]:
                        self.__selected = 1
                        t = self.__selected_obj
                        self.__selected_index = index
                        self.__selected_obj = self.bag[index]
                        self.bag[index] = t
                    else:
                        if state == pygame.BUTTON_LEFT or self.bag[index].number == 1:
                            self.bag[index] = self.__selected_obj
                            self.__selected = 0
                            self.__selected_index = -1
                            self.__selected_obj = 0
                        elif state == pygame.BUTTON_RIGHT:
                            self.bag[index] = self.__selected_obj
                            self.bag[index].number = 1
                            self.__selected_obj.number -= 1
            else:
                if self.__selected:
                    if state == pygame.BUTTON_LEFT or self.__selected_obj.number == 1:
                        self.out(self.__selected_obj)
                        self.__selected = 0
                        self.__selected_index = -1
                        self.__selected_obj = 0
                    elif state == pygame.BUTTON_RIGHT:
                        self.__selected_obj.number -= 1

    def put(self, obj):
        if not self.__full:
            if not self.__free:
                self.__full = 1
                return False
            first = -1
            for i in range(36):
                if self.bag[i]:
                    if self.bag[i].name == obj.name and self.bag[i].limit >= obj.number + self.bag[i].number:
                        self.bag[i].number += obj.number
                        self.__free -= 1
                        return True
                else:
                    if first == -1:
                        first = i
            if 0 <= first <= 35:
                self.bag[first] = obj
                self.__free -= 1
                return True
            else:
                self.__full = 1
                return False
        return False

    def out(self, obj):
        pass

    def update(self, rect):
        self.__surface.fill((0, 0, 0, 0))
        self.__surface.blit(self.__temp)
        if self.__selected_obj:
            self.__surface.blit(self.__selected_obj.surface, rect)
        for i in range(36):
            if self.bag[i]:
                self.__surface.blit(self.bag[i].surface, (self.x + i * self.w, self.y + i * self.h))
        return self.__surface

    def render(self):
        if self.state:
            return self.__surface