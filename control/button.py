from __future__ import annotations
from typing import Union
import pygame.surface
from game_master.gameSurface import HaveNameSurface


class Button:
    left = -1
    right = -2
    top = -3
    bottom = -4
    SIZE = 0x00
    RECT = 0x0F
    RIS = 0xF0
    ALL = 0xFF

    def __init__(self,
                 rect: tuple[int, int] | list[int, int] = (0, 0),
                 size: tuple[int, int] | list[int, int] = (50, 50),
                 rectInSize: tuple[int, int] | list[int, int] = (0, 0),
                 area: int = None,
                 text: str = "Button",
                 frameSize: int = 0,
                 actionColor: tuple[int, int, int] | list[int, int, int] = (127, 127, 127),
                 bg: tuple[int, int, int] | list[int, int, int] = (255, 255, 255),
                 fg: tuple[int, int, int] | list[int, int, int] = (0, 0, 0),
                 font: pygame.font.Font = None,
                 name="Button"):
        self.__state = Button.RECT
        self.__area = area
        self.__rect = rect
        self.x = self.__rect[0]
        self.y = self.__rect[1]
        self.__size = size
        self.__rectInSize = rectInSize
        self.__name = name
        self.__text = text
        self.__actionColor = actionColor
        self.__action = False
        self.frameSize = frameSize
        self.__bg = bg
        self.__fg = fg
        self.__font = font if font else pygame.font.Font()

    def __add__(self, other):
        if self.__state == Button.RECT:
            if isinstance(other, Button):
                other = other.__rect
            if isinstance(other, (list, tuple)):
                t1 = self.__rect[0]
                t2 = self.__rect[1]
                if isinstance(other[0], int):
                    t1 = self.__rect[0] + other[0]
                if isinstance(other[1], int):
                    t2 = self.__rect[1] + other[1]
                self.get_rect((t1, t2))
            elif isinstance(other, (int, float)):
                self.get_rect((self.__rect[0] + other, self.__rect[1] + other))
        elif self.__state == Button.SIZE:
            if isinstance(other, Button):
                other = other.__size
            if isinstance(other, (list, tuple)):
                t1 = self.__size[0]
                t2 = self.__size[1]
                if isinstance(other[0], int):
                    t1 = self.__size[0] + other[0]
                if isinstance(other[1], int):
                    t2 = self.__size[1] + other[1]
                self.get_size((t1, t2))
            elif isinstance(other, (int, float)):
                self.get_size((self.__size[0] + other, self.__size[1] + other))
        elif self.__state == Button.RIS:
            if isinstance(other, Button):
                other = other.__rectInSize
            if isinstance(other, (list, tuple)):
                t1 = self.__rectInSize[0]
                t2 = self.__rectInSize[1]
                if isinstance(other[0], int):
                    t1 = self.__rectInSize[0] + other[0]
                if isinstance(other[1], int):
                    t2 = self.__rectInSize[1] + other[1]
                self.get_rect_in_size((t1, t2))
            elif isinstance(other, (int, float)):
                self.get_rect_in_size((self.__rectInSize[0] + other, self.__rectInSize[1] + other))
        elif self.__state == Button.ALL:
            if isinstance(other, Button):
                self.get_rect((self.__rect[0] + other.__rect[0], self.__rect[1] + other.__rect[1]))
                self.get_size((self.__size[0] + other.__size[0], self.__size[1] + other.__size[1]))
                self.get_rect_in_size((self.__rectInSize[0] + other.__rectInSize[0],
                                       self.__rectInSize[1] + other.__rectInSize[1]))
            elif isinstance(other, (list, tuple)):
                t = [0, 0]
                if isinstance(other[0], int):
                    t[0] = other[0]
                if isinstance(other[1], int):
                    t[1] = other[1]
                self.get_rect((self.__rect[0] + t[0], self.__rect[1] + t[1]))
                self.get_size((self.__size[0] + t[0], self.__size[1] + t[1]))
                self.get_rect_in_size((self.__rectInSize[0] + t[0],
                                       self.__rectInSize[1] + t[1]))
            elif isinstance(other, (int, float)):
                self.get_rect((self.__rect[0] + other, self.__rect[1] + other))
                self.get_size((self.__size[0] + other, self.__size[1] + other))
                self.get_rect_in_size((self.__rectInSize[0] + other,
                                       self.__rectInSize[1] + other))
        return self

    def __sub__(self, other):
        if self.__state == Button.RECT:
            if isinstance(other, Button):
                other = other.__rect
            if isinstance(other, (list, tuple)):
                t1 = self.__rect[0]
                t2 = self.__rect[1]
                if isinstance(other[0], int):
                    t1 = self.__rect[0] - other[0]
                if isinstance(other[1], int):
                    t2 = self.__rect[1] - other[1]
                self.get_rect((t1, t2))
            elif isinstance(other, (int, float)):
                self.get_rect((self.__rect[0] - other, self.__rect[1] - other))
        elif self.__state == Button.SIZE:
            if isinstance(other, Button):
                other = other.__size
            if isinstance(other, (list, tuple)):
                t1 = self.__size[0]
                t2 = self.__size[1]
                if isinstance(other[0], int):
                    t1 = self.__size[0] - other[0]
                if isinstance(other[1], int):
                    t2 = self.__size[1] - other[1]
                self.get_size((t1, t2))
            elif isinstance(other, (int, float)):
                self.get_size((self.__size[0] - other, self.__size[1] - other))
        elif self.__state == Button.RIS:
            if isinstance(other, Button):
                other = other.__rectInSize
            if isinstance(other, (list, tuple)):
                t1 = self.__rectInSize[0]
                t2 = self.__rectInSize[1]
                if isinstance(other[0], int):
                    t1 = self.__rectInSize[0] - other[0]
                if isinstance(other[1], int):
                    t2 = self.__rectInSize[1] - other[1]
                self.get_rect_in_size((t1, t2))
            elif isinstance(other, (int, float)):
                self.get_rect_in_size((self.__rectInSize[0] - other, self.__rectInSize[1] - other))
        elif self.__state == Button.ALL:
            if isinstance(other, Button):
                self.get_rect((self.__rect[0] - other.__rect[0], self.__rect[1] - other.__rect[1]))
                self.get_size((self.__size[0] - other.__size[0], self.__size[1] - other.__size[1]))
                self.get_rect_in_size((self.__rectInSize[0] - other.__rectInSize[0],
                                       self.__rectInSize[1] - other.__rectInSize[1]))
            elif isinstance(other, (list, tuple)):
                t = [0, 0]
                if isinstance(other[0], int):
                    t[0] = other[0]
                if isinstance(other[1], int):
                    t[1] = other[1]
                self.get_rect((self.__rect[0] - t[0], self.__rect[1] - t[1]))
                self.get_size((self.__size[0] - t[0], self.__size[1] - t[1]))
                self.get_rect_in_size((self.__rectInSize[0] - t[0],
                                       self.__rectInSize[1] - t[1]))
            elif isinstance(other, (int, float)):
                self.get_rect((self.__rect[0] - other, self.__rect[1] - other))
                self.get_size((self.__size[0] - other, self.__size[1] - other))
                self.get_rect_in_size((self.__rectInSize[0] - other,
                                       self.__rectInSize[1] - other))
        return self

    def __mul__(self, other):
        if self.__state == Button.RECT:
            if isinstance(other, Button):
                other = other.__rect
            if isinstance(other, (list, tuple)):
                t1 = self.__rect[0]
                t2 = self.__rect[1]
                if isinstance(other[0], int):
                    t1 = self.__rect[0] * other[0]
                if isinstance(other[1], int):
                    t2 = self.__rect[1] * other[1]
                self.get_rect((t1, t2))
            elif isinstance(other, (int, float)):
                self.get_rect((self.__rect[0] * other, self.__rect[1] * other))
        elif self.__state == Button.SIZE:
            if isinstance(other, Button):
                other = other.__size
            if isinstance(other, (list, tuple)):
                t1 = self.__size[0]
                t2 = self.__size[1]
                if isinstance(other[0], int):
                    t1 = self.__size[0] * other[0]
                if isinstance(other[1], int):
                    t2 = self.__size[1] * other[1]
                self.get_size((t1, t2))
            elif isinstance(other, (int, float)):
                self.get_size((self.__size[0] * other, self.__size[1] * other))
        elif self.__state == Button.RIS:
            if isinstance(other, Button):
                other = other.__rectInSize
            if isinstance(other, (list, tuple)):
                t1 = self.__rectInSize[0]
                t2 = self.__rectInSize[1]
                if isinstance(other[0], int):
                    t1 = self.__rectInSize[0] * other[0]
                if isinstance(other[1], int):
                    t2 = self.__rectInSize[1] * other[1]
                self.get_rect_in_size((t1, t2))
            elif isinstance(other, (int, float)):
                self.get_rect_in_size((self.__rectInSize[0] * other, self.__rectInSize[1] * other))
        elif self.__state == Button.ALL:
            if isinstance(other, Button):
                self.get_rect((self.__rect[0] * other.__rect[0], self.__rect[1] * other.__rect[1]))
                self.get_size((self.__size[0] * other.__size[0], self.__size[1] * other.__size[1]))
                self.get_rect_in_size((self.__rectInSize[0] * other.__rectInSize[0],
                                       self.__rectInSize[1] * other.__rectInSize[1]))
            elif isinstance(other, (list, tuple)):
                t = [0, 0]
                if isinstance(other[0], int):
                    t[0] = other[0]
                if isinstance(other[1], int):
                    t[1] = other[1]
                self.get_rect((self.__rect[0] * t[0], self.__rect[1] * t[1]))
                self.get_size((self.__size[0] * t[0], self.__size[1] * t[1]))
                self.get_rect_in_size((self.__rectInSize[0] * t[0],
                                       self.__rectInSize[1] * t[1]))
            elif isinstance(other, (int, float)):
                self.get_rect((self.__rect[0] * other, self.__rect[1] * other))
                self.get_size((self.__size[0] * other, self.__size[1] * other))
                self.get_rect_in_size((self.__rectInSize[0] * other,
                                       self.__rectInSize[1] * other))
        return self

    def __truediv__(self, other):
        if isinstance(other, Button):
            self.get_rect((self.__rect[0] / other.__rect[0], self.__rect[1] / other.__rect[1]))
            self.get_size((self.__size[0] / other.__size[0], self.__size[1] / other.__size[1]))
            self.get_rect_in_size((self.__rectInSize[0] / other.__rectInSize[0],
                                   self.__rectInSize[1] / other.__rectInSize[1]))
        else:
            if self.__state == Button.RECT:
                if isinstance(other, Button):
                    other = other.__rect
                if isinstance(other, (list, tuple)):
                    t1 = self.__rect[0]
                    t2 = self.__rect[1]
                    if isinstance(other[0], int):
                        t1 = self.__rect[0] / other[0]
                    if isinstance(other[1], int):
                        t2 = self.__rect[1] / other[1]
                    self.get_rect((t1, t2))
                elif isinstance(other, (int, float)):
                    self.get_rect((self.__rect[0] / other, self.__rect[1] / other))
            elif self.__state == Button.SIZE:
                if isinstance(other, Button):
                    other = other.__size
                if isinstance(other, (list, tuple)):
                    t1 = self.__size[0]
                    t2 = self.__size[1]
                    if isinstance(other[0], int):
                        t1 = self.__size[0] / other[0]
                    if isinstance(other[1], int):
                        t2 = self.__size[1] / other[1]
                    self.get_size((t1, t2))
                elif isinstance(other, (int, float)):
                    self.get_size((self.__size[0] / other, self.__size[1] / other))
            elif self.__state == Button.RIS:
                if isinstance(other, Button):
                    other = other.__rectInSize
                if isinstance(other, (list, tuple)):
                    t1 = self.__rectInSize[0]
                    t2 = self.__rectInSize[1]
                    if isinstance(other[0], int):
                        t1 = self.__rectInSize[0] / other[0]
                    if isinstance(other[1], int):
                        t2 = self.__rectInSize[1] / other[1]
                    self.get_rect_in_size((t1, t2))
                elif isinstance(other, (int, float)):
                    self.get_rect_in_size((self.__rectInSize[0] / other, self.__rectInSize[1] / other))
            elif self.__state == Button.ALL:
                if isinstance(other, Button):
                    self.get_rect((self.__rect[0] / other.__rect[0], self.__rect[1] / other.__rect[1]))
                    self.get_size((self.__size[0] / other.__size[0], self.__size[1] / other.__size[1]))
                    self.get_rect_in_size((self.__rectInSize[0] / other.__rectInSize[0],
                                           self.__rectInSize[1] / other.__rectInSize[1]))
                elif isinstance(other, (list, tuple)):
                    t = [0, 0]
                    if isinstance(other[0], int):
                        t[0] = other[0]
                    if isinstance(other[1], int):
                        t[1] = other[1]
                    self.get_rect((self.__rect[0] / t[0], self.__rect[1] / t[1]))
                    self.get_size((self.__size[0] / t[0], self.__size[1] / t[1]))
                    self.get_rect_in_size((self.__rectInSize[0] / t[0],
                                           self.__rectInSize[1] / t[1]))
                elif isinstance(other, (int, float)):
                    self.get_rect((self.__rect[0] / other, self.__rect[1] / other))
                    self.get_size((self.__size[0] / other, self.__size[1] / other))
                    self.get_rect_in_size((self.__rectInSize[0] / other,
                                           self.__rectInSize[1] / other))
        return self

    def __floordiv__(self, other):
        if isinstance(other, Button):
            self.get_rect((self.__rect[0] // other.__rect[0], self.__rect[1] // other.__rect[1]))
            self.get_size((self.__size[0] // other.__size[0], self.__size[1] // other.__size[1]))
            self.get_rect_in_size((self.__rectInSize[0] // other.__rectInSize[0],
                                   self.__rectInSize[1] // other.__rectInSize[1]))
        else:
            if self.__state == Button.RECT:
                if isinstance(other, Button):
                    other = other.__rect
                if isinstance(other, (list, tuple)):
                    t1 = self.__rect[0]
                    t2 = self.__rect[1]
                    if isinstance(other[0], int):
                        t1 = self.__rect[0] // other[0]
                    if isinstance(other[1], int):
                        t2 = self.__rect[1] // other[1]
                    self.get_rect((t1, t2))
                elif isinstance(other, (int, float)):
                    self.get_rect((self.__rect[0] // other, self.__rect[1] // other))
            elif self.__state == Button.SIZE:
                if isinstance(other, Button):
                    other = other.__size
                if isinstance(other, (list, tuple)):
                    t1 = self.__size[0]
                    t2 = self.__size[1]
                    if isinstance(other[0], int):
                        t1 = self.__size[0] // other[0]
                    if isinstance(other[1], int):
                        t2 = self.__size[1] // other[1]
                    self.get_size((t1, t2))
                elif isinstance(other, (int, float)):
                    self.get_size((self.__size[0] // other, self.__size[1] // other))
            elif self.__state == Button.RIS:
                if isinstance(other, Button):
                    other = other.__rectInSize
                if isinstance(other, (list, tuple)):
                    t1 = self.__rectInSize[0]
                    t2 = self.__rectInSize[1]
                    if isinstance(other[0], int):
                        t1 = self.__rectInSize[0] // other[0]
                    if isinstance(other[1], int):
                        t2 = self.__rectInSize[1] // other[1]
                    self.get_rect_in_size((t1, t2))
                elif isinstance(other, (int, float)):
                    self.get_rect_in_size((self.__rectInSize[0] // other, self.__rectInSize[1] // other))
            elif self.__state == Button.ALL:
                if isinstance(other, Button):
                    self.get_rect((self.__rect[0] // other.__rect[0], self.__rect[1] // other.__rect[1]))
                    self.get_size((self.__size[0] // other.__size[0], self.__size[1] // other.__size[1]))
                    self.get_rect_in_size((self.__rectInSize[0] // other.__rectInSize[0],
                                           self.__rectInSize[1] // other.__rectInSize[1]))
                elif isinstance(other, (list, tuple)):
                    t = [0, 0]
                    if isinstance(other[0], int):
                        t[0] = other[0]
                    if isinstance(other[1], int):
                        t[1] = other[1]
                    self.get_rect((self.__rect[0] // t[0], self.__rect[1] // t[1]))
                    self.get_size((self.__size[0] // t[0], self.__size[1] // t[1]))
                    self.get_rect_in_size((self.__rectInSize[0] // t[0],
                                           self.__rectInSize[1] // t[1]))
                elif isinstance(other, (int, float)):
                    self.get_rect((self.__rect[0] // other, self.__rect[1] // other))
                    self.get_size((self.__size[0] // other, self.__size[1] // other))
                    self.get_rect_in_size((self.__rectInSize[0] // other,
                                           self.__rectInSize[1] // other))
        return self

    def __mod__(self, other):
        if isinstance(other, Button):
            self.get_rect((self.__rect[0] % other.__rect[0], self.__rect[1] % other.__rect[1]))
            self.get_size((self.__size[0] % other.__size[0], self.__size[1] % other.__size[1]))
            self.get_rect_in_size((self.__rectInSize[0] % other.__rectInSize[0],
                                   self.__rectInSize[1] % other.__rectInSize[1]))
        else:
            if self.__state == Button.RECT:
                if isinstance(other, Button):
                    other = other.__rect
                if isinstance(other, (list, tuple)):
                    t1 = self.__rect[0]
                    t2 = self.__rect[1]
                    if isinstance(other[0], int):
                        t1 = self.__rect[0] % other[0]
                    if isinstance(other[1], int):
                        t2 = self.__rect[1] % other[1]
                    self.get_rect((t1, t2))
                elif isinstance(other, (int, float)):
                    self.get_rect((self.__rect[0] % other, self.__rect[1] % other))
            elif self.__state == Button.SIZE:
                if isinstance(other, Button):
                    other = other.__size
                if isinstance(other, (list, tuple)):
                    t1 = self.__size[0]
                    t2 = self.__size[1]
                    if isinstance(other[0], int):
                        t1 = self.__size[0] % other[0]
                    if isinstance(other[1], int):
                        t2 = self.__size[1] % other[1]
                    self.get_size((t1, t2))
                elif isinstance(other, (int, float)):
                    self.get_size((self.__size[0] % other, self.__size[1] % other))
            elif self.__state == Button.RIS:
                if isinstance(other, Button):
                    other = other.__rectInSize
                if isinstance(other, (list, tuple)):
                    t1 = self.__rectInSize[0]
                    t2 = self.__rectInSize[1]
                    if isinstance(other[0], int):
                        t1 = self.__rectInSize[0] % other[0]
                    if isinstance(other[1], int):
                        t2 = self.__rectInSize[1] % other[1]
                    self.get_rect_in_size((t1, t2))
                elif isinstance(other, (int, float)):
                    self.get_rect_in_size((self.__rectInSize[0] % other, self.__rectInSize[1] % other))
            elif self.__state == Button.ALL:
                if isinstance(other, Button):
                    self.get_rect((self.__rect[0] % other.__rect[0], self.__rect[1] % other.__rect[1]))
                    self.get_size((self.__size[0] % other.__size[0], self.__size[1] % other.__size[1]))
                    self.get_rect_in_size((self.__rectInSize[0] % other.__rectInSize[0],
                                           self.__rectInSize[1] % other.__rectInSize[1]))
                elif isinstance(other, (list, tuple)):
                    t = [0, 0]
                    if isinstance(other[0], int):
                        t[0] = other[0]
                    if isinstance(other[1], int):
                        t[1] = other[1]
                    self.get_rect((self.__rect[0] % t[0], self.__rect[1] % t[1]))
                    self.get_size((self.__size[0] % t[0], self.__size[1] % t[1]))
                    self.get_rect_in_size((self.__rectInSize[0] % t[0],
                                           self.__rectInSize[1] % t[1]))
                elif isinstance(other, (int, float)):
                    self.get_rect((self.__rect[0] % other.__rect[0], self.__rect[1] % other.__rect[1]))
                    self.get_size((self.__size[0] % other.__size[0], self.__size[1] % other.__size[1]))
                    self.get_rect_in_size((self.__rectInSize[0] % other.__rectInSize[0],
                                           self.__rectInSize[1] % other.__rectInSize[1]))
        return self

    def __lt__(self, other):
        if isinstance(other, Button):
            return self.__rect[0] < other.__rect[0] and self.__rect[1] < other.__rect[1]
        elif isinstance(other, int):
            return self.__rect[0] < other and self.__rect[1] < other
        elif isinstance(other, (list, tuple)):
            return self.__rect[0] < other[0] and self.__rect[1] < other[1]

    def __gt__(self, other):
        if isinstance(other, Button):
            return self.__rect[0] > other.__rect[0] and self.__rect[1] < other.__rect[1]
        elif isinstance(other, int):
            return self.__rect[0] > other and self.__rect[1] > other
        elif isinstance(other, (list, tuple)):
            return self.__rect[0] > other[0] and self.__rect[1] > other[1]

    def __le__(self, other):
        if isinstance(other, Button):
            return self.__rect[0] <= other.__rect[0] and self.__rect[1] <= other.__rect[1]
        elif isinstance(other, int):
            return self.__rect[0] <= other and self.__rect[1] <= other
        elif isinstance(other, (list, tuple)):
            return self.__rect[0] <= other[0] and self.__rect[1] <= other[1]

    def __ge__(self, other):
        if isinstance(other, Button):
            return self.__rect[0] >= other.__rect[0] and self.__rect[1] >= other.__rect[1]
        elif isinstance(other, int):
            return self.__rect[0] >= other and self.__rect[1] >= other
        elif isinstance(other, (list, tuple)):
            return self.__rect[0] >= other[0] and self.__rect[1] >= other[1]

    def __eq__(self, other):
        if isinstance(other, Button):
            return self.__rect[0] == other.__rect[0] and self.__rect[1] == other.__rect[1]
        elif isinstance(other, int):
            return self.__rect[0] == other and self.__rect[1] == other
        elif isinstance(other, (list, tuple)):
            return self.__rect[0] == other[0] and self.__rect[1] == other[1]

    def __ne__(self, other):
        if isinstance(other, Button):
            return self.__rect[0] != other.__rect[0] and self.__rect[1] != other.__rect[1]
        elif isinstance(other, int):
            return self.__rect[0] != other and self.__rect[1] != other
        elif isinstance(other, (list, tuple)):
            return self.__rect[0] != other[0] and self.__rect[1] != other[1]

    def __len__(self):
        return self.__size

    @property
    def action(self):
        return self.__action

    @action.setter
    def action(self, action):
        self.__action = action

    @property
    def state(self):
        return self.__state

    @state.setter
    def state(self, state: int = 0x00):
        self.__state = state

    def size(self, func=None, *args):
        self.__state = Button.SIZE
        if func:
            func(*args)

    def rect(self, func=None, *args):
        self.__state = Button.RECT
        if func:
            func(*args)

    def rect_in_size(self, func=None, *args):
        self.__state = Button.RIS
        if func:
            func(*args)

    def all(self, func=None, *args):
        self.__state = Button.ALL
        if func:
            func(*args)

    def render(self, screen: pygame.surface.Surface, antialias: bool = True, wraplength: int = -1,
               area: int = None) -> None:
        if area:
            self.__area = area
        s = pygame.surface.Surface(self.__size)
        s.fill(self.__bg)
        if self.__area == HaveNameSurface.center:
            b = pygame.surface.Surface((self.__size[0] - 2 * self.__rectInSize[0],
                                        self.__size[1] - 2 * self.__rectInSize[1]))
            b.fill(self.__bg)
            textSurface = self.__font.render(self.__text, antialias, self.__fg, self.__bg,
                                             wraplength if wraplength >= 0 else self.__size[0] - 2 * self.__rectInSize[
                                                 0])
            b.blit(textSurface)
            s.blit(b, self.__rectInSize)
        elif self.__area == Button.left:
            b = self.__font.render(self.__text, antialias, self.__fg, self.__bg,
                                   wraplength if wraplength >= 0 else self.__size[0])
            s.blit(b, (0, self.__rectInSize[1]))
        elif self.__area == Button.right:
            if wraplength >= 0:
                b = pygame.surface.Surface((wraplength, self.__size[1] - self.__rectInSize[1]))
                b.fill(self.__bg)
                textSurface = self.__font.render(self.__text, antialias, self.__fg, self.__bg,
                                                 wraplength)
                b.blit(textSurface)
                s.blit(b, (self.__size[0] - wraplength, self.__rectInSize[1]))
            else:
                b = self.__font.render(self.__text, antialias, self.__fg, self.__bg,
                                       self.__size[0] - self.__rectInSize[0])
                s.blit(b, self.__rectInSize)
        elif self.__area == Button.top:
            b = self.__font.render(self.__text, antialias, self.__fg, self.__bg,
                                   wraplength if wraplength >= 0 else self.__size[0] - self.__rectInSize[0])
            s.blit(b, (self.__rectInSize[0], 0))
        elif self.__area == Button.bottom:
            b = self.__font.render(self.__text, antialias, self.__fg, self.__bg,
                                   wraplength if wraplength >= 0 else self.__size[0] - self.__rectInSize[0])
            b.get_rect(bottomleft=(self.__rectInSize[0], self.__size[0] - wraplength))
            s.blit(b, b.get_rect())
        else:
            b = self.__font.render(self.__text, antialias, self.__fg, self.__bg,
                                   self.__size[0] - self.__rectInSize[0])
            s.blit(b, self.__rectInSize)
        screen.blit(s, self.__rect)

    def get_font_size(self, size: int = None) -> int:
        if size:
            self.__font.set_point_size(size)
        return self.__font.get_point_size()

    def get_font_way(self, bold: bool = None, italic: bool = None, underline: bool = None,
                     strikethrough: bool = None) -> tuple[bool, bool, bool, bool]:
        if bold != None:
            self.__font.set_bold(bold)
        if italic != None:
            self.__font.set_italic(italic)
        if underline != None:
            self.__font.set_underline(underline)
        if strikethrough != None:
            self.__font.set_strikethrough(strikethrough)
        return self.__font.bold, self.__font.italic, self.__font.underline, self.__font.strikethrough

    def get_font_align(self, align: int = None) -> int:
        if align:
            self.__font.align = align
        return self.__font.align

    def get_area(self, area: int = None) -> int:
        if area:
            self.__area = area
        return self.__area

    def get_font(self, font: pygame.font.Font = None) -> pygame.font.Font:
        if font:
            self.__font = font
        return self.__font

    def get_rect(self, rect: tuple[int, int] | list[int, int] = None) -> tuple[int, int]:
        if rect:
            self.__rect = rect
        return self.__rect

    def get_size(self, size: tuple[int, int] | list[int, int] = None) -> tuple[int, int]:
        if size:
            self.__size = size
        return self.__size

    def get_rect_in_size(self, ris: tuple[int, int] | list[int, int] = None) -> tuple[int, int]:
        if ris:
            self.__rectInSize = ris
        return self.__rectInSize

    def get_name(self, name=None):
        if name:
            self.__name = name
        return self.__name

    def get_text(self, text: str = None) -> str:
        if text:
            self.__text = text
        return self.__text

    def get_bg(self, bg: tuple[int, int, int] | list[int, int, int] = None) -> tuple[int, int, int]:
        if bg:
            self.__bg = bg
        return self.__bg

    def get_fg(self, fg: tuple[int, int, int] | list[int, int, int] = None) -> tuple[int, int, int]:
        if fg:
            self.__fg = fg
        return self.__fg

    def bind(self, button_list: list, func: str):
        button_list[0] += 1
        button_list.append([True, self.__name, (self.__rect, self.__size), func])

    def unBind(self, button_list):
        for i in range(1, button_list[0]):
            if button_list[i][1] == self.__name:
                button_list[i][0] = False


class SurfaceButton(Button):
    SURFACELEN = 0xAA

    def __init__(self,
                 rect: tuple[int, int] | list[int, int] = (0, 0),
                 size: tuple[int, int] | list[int, int] = (50, 50),
                 rectInSize: tuple[int, int] | list[int, int] = (0, 0),
                 area: int = None,
                 text: str = "SurfaceButton",
                 frameSize: int = 0,
                 actionColor: tuple[int, int, int] | list[int, int, int] = (127, 127, 127),
                 bg: tuple[int, int, int] | list[int, int, int] = (255, 255, 255),
                 fg: tuple[int, int, int] | list[int, int, int] = (0, 0, 0),
                 surface: list[Union[pygame.surface.Surface, HaveNameSurface]] = None,
                 font: pygame.font.Font = None,
                 name="Button"):
        super().__init__(rect, size, rectInSize, area, text, frameSize, actionColor, bg, fg, font, name)
        self.__surface = [0]
        for s in surface:
            self.__surface.append(s)

    def __add__(self, other):
        if isinstance(other, SurfaceButton):
            if self.__state == SurfaceButton.SURFACELEN:
                t = other.get_surface()
                self.__surface += t[1:]
                self.__surface[0] += t[0]
                return self
        super().__add__(other)

    def __len__(self) -> int:
        if self.__state == SurfaceButton.SURFACELEN:
            return self.__surface[0]
        else:
            super().__len__()

    def surfacelen(self, func=None, *args):
        self.__state = SurfaceButton.SURFACELEN
        if func:
            func(*args)

    def add_surface(self, surface: list[Union[pygame.surface.Surface, HaveNameSurface]]) -> None:
        t = 0
        for s in surface:
            self.__surface.append(s)
            t += 1
        self.__surface[0] += t

    def get_surface(self, surface: list[Union[pygame.surface.Surface, HaveNameSurface]] = None) \
            -> list[Union[pygame.surface.Surface, HaveNameSurface, int]]:
        if surface:
            self.__surface = [0]
            t = 0
            for s in surface:
                self.__surface.append(s)
                t += 1
            self.__surface[0] = t
        return self.__surface

    def render(self, screen: pygame.surface.Surface, antialias: bool = True, wraplength: int = -1,
               area: int = None) -> None:
        for s in self.__surface:
            screen.blit(s, s.get_rect())
        self.render(screen, antialias, wraplength, area)
