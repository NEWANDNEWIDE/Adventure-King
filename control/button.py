from __future__ import annotations
import pygame.surface
import game_master


class Button:
    def __init__(self, rect, size, text_rect, text, bg, fg, action_color, surface):
        self.x = rect[0]
        self.y = rect[1]
        self.w = size[0]
        self.h = size[1]
        self.__rect = rect
        self.__size = size
        self.__text_rect = text_rect
        self.__text = text
        self.__bg = bg
        self.__fg = fg
        self.__action_color = action_color
        self.__action = True
        self.__surface = surface

    @property
    def rect(self):
        return self.__rect

    @rect.setter
    def rect(self, rect):
        self.__rect = rect
        self.w = rect[0]
        self.h = rect[1]

    @property
    def size(self):
        return self.__size

    @size.setter
    def size(self, size):
        self.__size = size

    @property
    def text_rect(self):
        return self.__text_rect

    @text_rect.setter
    def text_rect(self, text_rect):
        self.__text_rect = text_rect

    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, text):
        self.__text = text

    @property
    def bg(self):
        return self.__bg

    @bg.setter
    def bg(self, bg):
        self.__bg = bg

    @property
    def fg(self):
        return self.__fg

    @fg.setter
    def fg(self, fg):
        self.__fg = fg

    @property
    def action_color(self):
        return self.__action_color

    @action_color.setter
    def action_color(self, action_color):
        self.__action_color = action_color

    @property
    def action(self):
        return self.__action

    @action.setter
    def action(self, action):
        self.__action = action

    @property
    def surface(self):
        return self.__surface

    @surface.setter
    def surface(self, surface):
        self.__surface = surface

    def activate(self, func, *args):
        if self.__action:
            func(*args)

    def render(self, screen: pygame.Surface):
        text_surface = game_master.game.Game.FONT.render(self.__text, True, self.__fg, self.__bg)
        button_surface = pygame.Surface(self.__size)
        button_surface.fill(self.__bg)
        button_surface.blit(self.__surface, (0, 0))
        button_surface.blit(text_surface, self.__text_rect)
        return button_surface, self.__rect
