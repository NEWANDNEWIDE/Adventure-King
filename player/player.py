from typing import Optional
import pygame
import game_master.gameObject
import game_master.fileManager


class Player(game_master.gameObject.GameObject):
    def __init__(self):
        super().__init__()
        self.__surface = game_master.fileManager.game_surface["player"]
        self.__mid = (self.__surface[0] - 1) // 4

        self.__vec2 = (0, 0)
        self.__rect = (400, 300)

        self.health = 100
        self.attack = 5
        self.attack_speed = 1
        self.critical_strike_chance = 5
        self.critical_strike_damage = 1.5
        self.reach_distance = 1

    def move(self):
        pass


class Bag:
    def __init__(self, rect, offset, w, h):
        self.__bag: Optional[game_master.gameObject.WoodenSword, int] = [0 for _ in range(36)]
        self.__surface: pygame.Surface = game_master.fileManager.game_surface["bag"]
        self.__temp: pygame.Surface = game_master.fileManager.game_surface["bag"]
        self.__rect = rect
        self.__offset = offset
        self.x = rect[0] + offset[0]
        self.y = rect[1] + offset[1]
        self.w = w
        self.h = h
        self.__state = 0
        self.__full = 0
        self.__selected = 0
        self.__selected_obj = 0

    def selected(self, pos):
        """
        state是背包的打开状态，1为打开，x，y分别是背包左上角的格子的位置，w, h是格子的宽高
        :param pos: 当鼠标点击时的位置
        :return: None
        """
        if self.__state:
            if self.x < pos[0] < self.x + self.__temp.width and self.y < pos[1] < self.y + self.__temp.height:
                pos[0] -= self.x
                pos[1] -= self.y
                pos[0] //= self.w
                pos[1] //= self.h
                index = pos[1] * 9 + pos[0]
                if not self.__selected:
                    if self.__bag[index]:
                        self.__selected = 1
                        self.__selected_obj = self.__bag[index]
                        self.__bag[index] = 0
                else:
                    if self.__bag[index]:
                        self.__selected = 1
                        t = self.__selected_obj
                        self.__selected_obj = self.__bag[index]
                        self.__bag[index] = t
                    else:
                        self.__bag[index] = self.__selected_obj
                        self.__selected = 0
                        self.__selected_obj = 0
            else:
                if self.__selected:
                    self.out(self.__selected_obj)
                    self.__selected = 0
                    self.__selected_obj = 0

    def put(self, obj):
        if not self.__full:
            first = -1
            for i in range(36):
                if self.__bag[i]:
                    if self.__bag[i].name == obj.name and self.__bag[i].limit >= obj.number + self.__bag[i].number:
                        self.__bag[i].number += obj.number
                        return
                else:
                    if first == -1:
                        first = i
            if 0 <= first <= 35:
                self.__bag[first] = obj
            else:
                self.__full = 1

    def out(self, obj):
        pass

    def render(self, rect):
        self.__surface.blit(self.__temp)
        if self.__selected_obj:
            self.__surface.blit(self.__selected_obj.surface, rect)
        for i in range(36):
            if self.__bag[i]:
                self.__surface.blit(self.__bag[i].surface, (self.x + i * self.w, self.y + i * self.h))
        return self.__surface
