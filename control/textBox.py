import pygame
import control.button


class TextBox(control.button.Button):
    def __init__(self,
                 rect: tuple[int, int] = (0, 0),
                 size: tuple[int, int] = (50, 50),
                 rectInSize: tuple[int, int] = (0, 0),
                 area: int = None,
                 text: str = "Button",
                 bg: tuple[int, int, int] = (255, 255, 255),
                 fg: tuple[int, int, int] = (0, 0, 0),
                 font: pygame.font.Font = None,
                 name="Button"):
        super().__init__(rect, size, rectInSize, area, text, bg, fg, font, name)


class SurfaceTextBox(control.button.SurfaceButton):
    def __init__(self,
                 rect: tuple[int, int] = (0, 0),
                 size: tuple[int, int] = (50, 50),
                 rectInSize: tuple[int, int] = (0, 0),
                 area: int = None,
                 text: str = "SurfaceButton",
                 bg: tuple[int, int, int] = (255, 255, 255),
                 fg: tuple[int, int, int] = (0, 0, 0),
                 surface: list[pygame.surface.Surface] = None,
                 font: pygame.font.Font = None,
                 name="Button"):
        super().__init__(rect, size, rectInSize, area, text, bg, fg, surface, font, name)
