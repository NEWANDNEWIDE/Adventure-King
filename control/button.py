from __future__ import annotations
import pygame.surface
import game_master


class Button:
    def __init__(self, rect, size, text_rect, text, bg, fg, action_color, name, callback=None, surface=None):
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
        self.name = name
        self.callback = callback

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

    def activate(self, pos, *args):
        if self.__action and self.callback:
            if self.rect[0] < pos[0] < self.rect[0] + self.size[0] and self.rect[1] < pos[1] < self.rect[1] + self.size[1]:
                print(self.name)
                self.callback(*args)
        return False

    def render(self, width=None, height=None):
        text_surface = game_master.game.Game.FONT.render(self.__text, True, self.__fg, self.__bg)
        if width and height:
            button_surface = pygame.Surface((width, height))
        elif width:
            button_surface = pygame.Surface((width, self.__size[1]))
        elif height:
            button_surface = pygame.Surface((self.__size[0], height))
        else:
            button_surface = pygame.Surface(self.__size)
        button_surface.fill(self.__bg)
        if self.__surface:
            button_surface.blit(self.__surface, (0, 0))
        button_surface.blit(text_surface, self.__text_rect)
        return button_surface, self.__rect


class ButtonList(Button):
    def __init__(self, rect, size, text_rect, text, bg, fg, action_color, name, callback=None, surface=None,
                 b_list=None, area="V"):
        super().__init__(rect, size, text_rect, text, bg, fg, action_color, name, callback, surface)
        self.__b_list = []
        self.__len = 0
        self.__l = False
        self.__area = area
        if b_list:
            if isinstance(b_list, list):
                self.__b_list = b_list
                self.__len = len(b_list)
            else:
                self.__b_list.append(b_list)
                self.__len += 1
        self.__b_size = 0
        if b_list:
            if self.__area == "V":
                self.__b_size += 2
                for i in b_list:
                    self.__b_size += self.size[1]
                    i.size = self.size
                    i.rect = (self.rect[0], self.rect[1] + self.__b_size)
                    self.__b_size += 2
            elif self.__area == "L":
                for i in b_list:
                    i.size = self.size
                    i.rect = (self.rect[0] + self.size[0], self.rect[1] + self.__b_size)
                    self.__b_size += self.size[1] + 2

    @property
    def area(self):
        return self.__area

    def activate(self, pos, *args):
        if self.action:
            if self.rect[0] < pos[0] < self.rect[0] + self.size[0] and self.rect[1] < pos[1] < self.rect[1] + self.size[1]:
                if self.__l:
                    self.__l = False
                    self.callback(*args)
                    return True
                else:
                    self.__l = True
                    self.callback(*args)
            else:
                if self.rect[0] < pos[0] < self.rect[0] + self.size[0] and self.__l:
                    t = (pos[1] - self.rect[1]) // self.size[1]
                    if 0 < t <= self.__len:
                        self.__l = self.__b_list[t-1].activate(pos, *args)
                    else:
                        self.__l = False
                else:
                    self.__l = False
        return self.__l

    def render(self, width=None, height=None):
        text_surface = game_master.game.Game.FONT.render(self.text, True, self.fg, self.bg)
        if self.__l:
            other = []
            if self.__area == "V":
                if width and height:
                    button_surface = pygame.Surface((width, height + self.__b_size))
                elif width:
                    button_surface = pygame.Surface((width, self.size[1] + self.__b_size))
                elif height:
                    button_surface = pygame.Surface((self.size[0], height + self.__b_size))
                else:
                    button_surface = pygame.Surface((self.size[0], self.size[1] + self.__b_size))
                button_surface.fill(self.bg)
                if self.surface:
                    button_surface.blit(self.surface, (0, 0))
                button_surface.blit(text_surface, self.text_rect)
                h = self.size[1]
                button_surface.fill((0, 0, 0), (self.rect[0], self.rect[1] + h, self.size[0], 2))
                for i in range(len(self.__b_list)):
                    t = self.__b_list[i].render()
                    button_surface.blit(t[0], (self.rect[0], self.rect[1] + h + 2))
                    if isinstance(self.__b_list[i], ButtonList):
                        if self.__b_list[i].area == "L" and len(t) == 3:
                            other.append(t[2])
                    h += self.size[1] + 2
                    button_surface.fill((0, 0, 0), (self.rect[0], self.rect[1] + h, self.size[0], 2))
                return button_surface, self.rect, other
            elif self.__area == "L":
                if width and height:
                    button_surface = pygame.Surface((width, height))
                elif width:
                    button_surface = pygame.Surface((width, self.size[1]))
                elif height:
                    button_surface = pygame.Surface((self.size[0], height))
                else:
                    button_surface = pygame.Surface(self.size)
                button_surface.fill(self.bg)
                if self.surface:
                    button_surface.blit(self.surface, (0, 0))
                button_surface.blit(text_surface, self.text_rect)
                level_surface = pygame.Surface((self.size[0], self.__b_size))
                other.append(level_surface)
                h = 0
                for i in range(len(self.__b_list)):
                    t = self.__b_list[i].render()
                    level_surface.blit(t[0], (self.rect[0] + self.size[0] + 2, self.rect[1] + h))
                    if isinstance(self.__b_list[i], ButtonList):
                        if self.__b_list[i].area == "L" and len(t) == 3:
                            other.append(t[2])
                    h += self.size[1]
                    level_surface.fill((0, 0, 0), (self.rect[0] + self.size[0] + 2, self.rect[1] + h, self.size[0], 2))
                    h += 2
                return button_surface, self.rect, other
        if width and height:
            button_surface = pygame.Surface((width, height))
        elif width:
            button_surface = pygame.Surface((width, self.size[1]))
        elif height:
            button_surface = pygame.Surface((self.size[0], height))
        else:
            button_surface = pygame.Surface(self.size)
        button_surface.fill(self.bg)
        if self.surface:
            button_surface.blit(self.surface, (0, 0))
        button_surface.blit(text_surface, self.text_rect)
        return button_surface, self.rect
