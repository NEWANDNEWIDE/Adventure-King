from typing import Union

import pygame.surface


class SlideBar:
    def __init__(self, slide: Union[pygame.surface.Surface, tuple[int, int, int]] =None, bar:Union[pygame.surface.Surface, tuple[int, int, int]]=None):
        self.slide = slide
        self.bar = bar

    def render_text_slide_bar(self, text:pygame.surface.Surface):
        self.h = text.height
        self.w = text.width