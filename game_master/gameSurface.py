from __future__ import annotations
import pygame


class GameSurface:
    def __init__(self, surface: pygame.Surface, name: str):
        self.__surface = surface
        self.__name = name

    @property
    def surface(self):
        return self.__surface

    @surface.setter
    def surface(self, surface):
        self.__surface = surface

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name
