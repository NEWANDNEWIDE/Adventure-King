import os
from typing import Union
import pyperclip
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
        self.__ctrl = 0
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

        self.time = 0.5
        self.cursor = pygame.Surface((1, game_master.game.Game.FONT.get_height() - 2))
        self.color = ((255, 255, 255), (0, 0, 0))
        self.index = 0
        self.cursor.fill(self.color[self.index])

        self.text_offset = 0
        self.cursor_offset = 0
        self.input_text_offset = 0

        self.copy_text = ""
        self.last_offset = 0

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

    def action(self, pos, event, dt):
        if self.__state:
            if pyperclip.is_available():
                self.copy_text = pyperclip.paste()
            self.time -= dt
            if self.time <= 0:
                self.time = 1
                self.index += 1
                if self.index > 1:
                    self.index = 0
                self.cursor.fill(self.color[self.index])
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
                self.index = 0
                self.time = 0.5
                self.cursor.fill(self.color[self.index])
        return self.update(event)

    def update(self, event: Union[pygame.event.Event] = None):
        if self.__state:
            if event.type == pygame.KEYDOWN:
                key = event.key
                if key == 13:
                    return self.__input_text
                elif key == 8 and self.__input_text != "" and self.text_offset:
                    if self.text_offset == len(self.__input_text):
                        w = game_master.game.Game.FONT.render(self.__input_text[-1], True, (0, 0, 0)).width
                        if self.input_text_offset:
                            if w > -self.input_text_offset:
                                self.cursor_offset -= w + self.input_text_offset
                                self.input_text_offset = 0
                            else:
                                self.input_text_offset += w
                        else:
                            self.cursor_offset -= game_master.game.Game.FONT.render(self.__input_text[-1], True, (0, 0, 0)).width
                        self.__input_text = self.__input_text[:-1]
                    else:
                        w = game_master.game.Game.FONT.render(self.__input_text[self.text_offset-1], True, (0, 0, 0)).width
                        if self.cursor_offset - w < 0:
                            w_2 = game_master.game.Game.FONT.render(self.__input_text[self.text_offset-2], True, (0, 0, 0)).width
                            self.input_text_offset += w - self.cursor_offset + w_2
                            self.cursor_offset = w_2
                        else:
                            self.cursor_offset -= w
                        self.__input_text = self.__input_text[:self.text_offset-1] + self.__input_text[self.text_offset:]
                    self.text_offset -= 1
                    if self.__all_selected:
                        self.__input_text = ""
                        self.__all_selected = 0
                        self.text_offset = 0
                        self.input_text_offset = 0
                        self.cursor_offset = 0
                elif key == 301 or key == 1073742049:
                    return self.__box
                elif key == 1073742048:
                    self.__ctrl = 1
                elif self.__ctrl:
                    pass
                elif key == 1073741904:
                    if self.text_offset:
                        self.text_offset -= 1
                        w = game_master.game.Game.FONT.render(self.__input_text[self.text_offset], True, (0, 0, 0)).width
                        self.cursor_offset -= w
                        if self.input_text_offset:
                            if self.cursor_offset < 0:
                                self.input_text_offset += w
                                if self.input_text_offset > 0:
                                    self.input_text_offset = 0
                                self.cursor_offset += w
                        else:
                            if self.cursor_offset < 0:
                                self.cursor_offset = 0

                elif key == 1073741903:
                    if self.text_offset < len(self.__input_text):
                        self.cursor_offset += game_master.game.Game.FONT.render(self.__input_text[self.text_offset], True, (0, 0, 0)).width
                        if self.cursor_offset > self.size[0] - 4:
                            self.input_text_offset -= self.cursor_offset - self.size[0] + 4
                            self.cursor_offset = self.size[0] - 4
                        self.text_offset += 1
                """else:
                    if key <= 255 and key != 8:
                        w = game_master.game.Game.FONT.render(chr(key), True, (0, 0, 0)).width
                        if self.text_offset == len(self.__input_text):
                            self.__input_text += chr(key)
                            if self.cursor_offset + w > self.size[0] - 4:
                                self.input_text_offset -= self.cursor_offset + w + 4 - self.size[0]
                                self.cursor_offset = self.size[0] - 4
                            else:
                                self.input_text_offset = -max(
                                    game_master.game.Game.FONT.render(self.__input_text, True, (0, 0, 0)).width -
                                    self.size[0] + 4, 0)
                                self.cursor_offset += w
                        else:
                            if self.cursor_offset + w > self.size[0] - 4:
                                self.input_text_offset -= w - (self.size[0] - 4 - self.cursor_offset)
                                self.cursor_offset = self.size[0] - 4
                                print(self.input_text_offset, self.cursor_offset)
                            else:
                                self.cursor_offset += w
                            self.__input_text = self.__input_text[:self.text_offset] + chr(key) + self.__input_text[self.text_offset:]
                        self.text_offset += 1"""
            elif event.type == pygame.KEYUP:
                if event.key == 1073742048:
                    self.__ctrl = 0
            elif event.type == pygame.TEXTINPUT:
                w = game_master.game.Game.FONT.render(event.text, True, (0, 0, 0)).width
                if self.text_offset == len(self.__input_text):
                    self.__input_text += event.text
                    if self.cursor_offset + w > self.size[0] - 4:
                        self.input_text_offset -= self.cursor_offset + w + 4 - self.size[0]
                        self.cursor_offset = self.size[0] - 4
                    else:
                        self.input_text_offset = -max(
                            game_master.game.Game.FONT.render(self.__input_text, True, (0, 0, 0)).width - self.size[0] + 4, 0)
                        self.cursor_offset += w
                else:
                    if self.cursor_offset + w > self.size[0] - 4:
                        self.input_text_offset -= w - (self.size[0] - 4 - self.cursor_offset)
                        self.cursor_offset = self.size[0] - 4
                    else:
                        self.cursor_offset += w
                    self.__input_text = self.__input_text[:self.text_offset] + event.text + self.__input_text[self.text_offset:]
                self.text_offset += len(event.text)
                if self.__all_selected:
                    self.__input_text = event.text
                    self.__last_text = ""
                    self.__all_selected = 0
                    self.text_offset = len(self.__input_text)
                    w = game_master.game.Game.FONT.render(event.text, True, (0, 0, 0)).width
                    if w > self.size[0] - 4:
                        self.input_text_offset = w + 4 - self.size[0]
                        self.cursor_offset = self.size[0] - 4
                    else:
                        self.cursor_offset = w
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pass

            if not self.__input_text:
                self.__last_text = ""
                self.__box.fill(self.__bg)
                if self.__surface:
                    self.__box.blit(self.__surface)
                if not self.__state:
                    self.__box.blit(game_master.game.Game.FONT.render(self.__text, True, self.__text_color, self.__bg,
                                                                      self.w - 2).convert_alpha(),
                                    (self.__offset, self.__offset))
            else:
                if self.__ctrl and event.key == 97 and not self.__all_selected:
                    self.__all_selected = 1
                    temp = self.__text_surface
                    temp.fill((138, 208, 230, 127))
                    self.__box.blit(temp, (self.__offset + self.input_text_offset, self.__offset))
                elif len(self.__input_text) != len(self.__last_text) or self.last_offset != self.input_text_offset:
                    self.__box.fill(self.__bg)
                    if self.__surface:
                        self.__box.blit(self.__surface)
                    if self.__input_text != "":
                        self.__text_surface = game_master.game.Game.FONT.render(self.__input_text, True, self.__fg,
                                                                                self.__bg).convert_alpha()
                        self.__box.blit(self.__text_surface, (self.__offset + self.input_text_offset, self.__offset))
                    self.last_offset = self.input_text_offset
                    self.__last_text = self.__input_text

        return self.__box

    def render_cursor(self):
        if self.__state:
            rect = self.rect[0] + 1 + self.cursor_offset, self.rect[1] + 2
            pygame.display.get_surface().blit(self.cursor, rect)
