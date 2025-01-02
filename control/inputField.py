import os
from typing import Union

import pygame.key
import game_master

os.environ["SDL_IME_SHOW_UI"] = "1"


class InputField:
    def __init__(self, rect, size, text, bg, fg, text_color, name, surface=None):
        self.x = rect[0]
        self.y = rect[1]
        self.w = size[0]
        self.h = size[1]
        self.name = name
        self.__rect = rect
        self.__size = size
        self.__text_color = text_color
        self.__text = text
        self.__bg = bg
        self.__fg = fg
        self.__surface = surface
        self.__input_text = ""
        self.__last_text = ""
        self.__state = 0
        self.__alt = 0
        self.__all_selected = 0
        self.__offset = 2
        self.__outside = 2
        self.__text_surface = game_master.game.Game.FONT.render(self.__text, True,
                                                                self.__text_color, self.__bg,
                                                                self.w - 2).convert_alpha()
        self.__box = pygame.Surface(size)
        self.__box.fill(self.__bg)
        if self.__surface:
            self.__box.blit(self.__surface)
        self.__box.blit(self.__text_surface, (self.__offset, self.__offset))

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
    def text_color(self):
        return self.__text_color

    @text_color.setter
    def text_color(self, text_color):
        self.__text_color = text_color

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
    def surface(self):
        return self.__surface

    @surface.setter
    def surface(self, surface):
        self.__surface = surface

    @property
    def box(self):
        return self.__box

    def action(self, pos, event):
        if not event:
            return self.__box
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.__all_selected:
                self.__all_selected = 0
                self.__box.blit(self.__text_surface)
            if self.x <= pos[0] <= self.x + self.w and self.y <= pos[1] <= self.y + self.h:
                pygame.key.start_text_input()
                pygame.key.set_text_input_rect((self.x, self.y + self.h, 0, 0))
                self.__state = 1
            else:
                pygame.key.stop_text_input()
                self.__state = 0
        return self.update(event)

    def update(self, event: Union[pygame.event.Event] = None):
        if self.__state:
            if event.type == pygame.KEYDOWN:
                key = event.key
                if key == 13:
                    return self.__input_text
                elif key == 8:
                    self.__input_text = self.__input_text[:-1]
                    if self.__all_selected:
                        self.__input_text = ""
                        self.__last_text = ""
                        self.__all_selected = 0
                elif key == 301 or key == 1073742049:
                    return self.__box
                elif key == 1073742050:
                    self.__alt = 1
                elif self.__alt:
                    pass
                else:
                    self.__input_text += chr(key)
            elif event.type == pygame.KEYUP:
                if event.key == 1073742050:
                    self.__alt = 0
            elif event.type == pygame.TEXTINPUT:
                self.__input_text += event.text
                if self.__all_selected:
                    self.__input_text = event.text
                    self.__last_text = ""
                    self.__all_selected = 0

            if not self.__input_text:
                self.__last_text = ""
                self.__box.fill(self.__bg)
                if self.__surface:
                    self.__box.blit(self.__surface)
                self.__box.blit(game_master.game.Game.FONT.render(self.__text, True, self.__text_color, self.__bg,
                                                                  self.w - 2).convert_alpha(),
                                (self.__offset, self.__offset))
            else:
                if self.__alt and event.key == 97 and not self.__all_selected:
                    self.__all_selected = 1
                    temp = self.__text_surface
                    temp.fill((138, 208, 230, 127))
                    self.__box.blit(temp, (self.__offset, self.__offset))
                elif len(self.__input_text) != len(self.__last_text):
                    self.__box.fill(self.__bg)
                    if self.__surface:
                        self.__box.blit(self.__surface)
                    self.__text_surface = game_master.game.Game.FONT.render(self.__input_text, True, self.__fg,
                                                                            self.__bg, self.w - 2).convert_alpha()
                    self.__box.blit(self.__text_surface, (self.__offset, self.__offset))
                    self.__last_text = self.__input_text
        return self.__box
