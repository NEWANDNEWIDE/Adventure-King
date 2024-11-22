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
        self.__selected = 0
        self.__selected_obj = 0

    def selected(self, pos):
        if self.__state:
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
            return self.render(pos)

    def put(self, obj):
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

    def render(self, rect):
        self.__surface.blit(self.__temp)
        if self.__selected_obj:
            self.__surface.blit(self.__selected_obj.surface, rect)
        for i in range(36):
            if self.__bag[i]:
                self.__surface.blit(self.__bag[i].surface, (self.x + i * 20, self.y + i * 20))
        return self.__surface
