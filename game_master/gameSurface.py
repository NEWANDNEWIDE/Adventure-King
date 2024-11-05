from __future__ import annotations
from os import PathLike
from typing import Union, IO, Sequence
import pygame
from pygame import Surface


class HaveNameSurface(Surface):
    TOPLEFT = None
    CENTER = 0
    TOPRIGHT = 1
    BOTTOMLEFT = 2
    BOTTOMRIGHT = 3
    MIDTOP = 4
    MIDLEFT = 5
    MIDBOTTOM = 6
    MIDRIGHT = 7

    def __init__(self,
                 size: tuple[int, int] = (0, 0),
                 flags: int = 0,
                 depth: int = 0,
                 masks: int | str | Sequence[int] | None = None,
                 rect=(0, 0),
                 area: int = None,
                 name=None,
                 surface: Surface = None):
        if surface:
            super().__init__(size=size, flags=flags, surface=surface)
        if depth != 0:
            if masks != 0:
                super().__init__(size, flags, depth, masks)
            else:
                super().__init__(size, flags, depth)
        elif masks != 0:
            super().__init__(size, flags, masks=masks)
        else:
            super().__init__(size, flags)
        self.__name = name
        self.__rect = rect
        self.rect(area)

    def rect(self, area=None) -> None:
        if area == 0:
            self.get_rect(center=self.rect)
        elif area == 1:
            self.get_rect(topright=self.rect)
        elif area == 2:
            self.get_rect(bottomleft=self.rect)
        elif area == 3:
            self.get_rect(bottomright=self.rect)
        elif area == 4:
            self.get_rect(midtop=self.rect)
        elif area == 5:
            self.get_rect(midleft=self.rect)
        elif area == 6:
            self.get_rect(midbottom=self.rect)
        elif area == 7:
            self.get_rect(midright=self.rect)
        else:
            self.get_rect(topleft=self.rect)

    def topleft(self):
        self.get_rect(topleft=self.rect)

    def center(self):
        self.get_rect(center=self.rect)

    def topright(self):
        self.get_rect(topright=self.rect)

    def bottomleft(self):
        self.get_rect(bottomleft=self.rect)

    def bottomright(self):
        self.get_rect(bottomright=self.rect)

    def midtop(self):
        self.get_rect(midtop=self.rect)

    def midleft(self):
        self.get_rect(midleft=self.rect)

    def midbottom(self):
        self.get_rect(midbottom=self.rect)

    def midright(self):
        self.get_rect(midright=self.rect)

    @staticmethod
    def load(file: Union[str, bytes, PathLike[str], PathLike[bytes], IO[bytes], IO[str]],
             namehint: str = "", name: str = None) -> HaveNameSurface:
        s = HaveNameSurface(surface=pygame.image.load(file, namehint))
        s.name = name
        return s

    def convert_alpha(self) -> HaveNameSurface:
        super().convert_alpha()
        return self

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name


def clean(button_list, name):
    for i in range(1, button_list[0]):
        if button_list[i][1] == name:
            del button_list[i]
            button_list[0] -= 1
