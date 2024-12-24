import os.path
import pygame.sprite
import settings


class ItemObject(pygame.sprite.Sprite):
    def __init__(self, pos, name: str, *groups):
        super().__init__(*groups)
        self.pos = pos
        self.name = name

        path = os.path.join(settings.SPRITES, name)

        self.surface = []
        self.mask = []
        self.index = 0

        for a in os.listdir(path):
            self.surface.append(pygame.image.load(os.path.join(path, a)).convert_alpha())
            self.mask = pygame.mask.from_surface(self.surface[-1])

        self.CAN_ATTACKED = len(self.surface)


class Tree(ItemObject):
    def __init__(self, pos, *groups):
        super().__init__(pos, "tree", *groups)


class Iron(ItemObject):
    def __init__(self, pos, *groups):
        super().__init__(pos, "iron", *groups)


class Gold(ItemObject):
    def __init__(self, pos, *groups):
        super().__init__(pos, "gold", *groups)


class BoxW(ItemObject):
    def __init__(self, pos, *groups):
        super().__init__(pos, "box_1", *groups)


class BoxY(ItemObject):
    def __init__(self, pos, *groups):
        super().__init__(pos, "box_2", *groups)


class Stone(ItemObject):
    def __init__(self, pos, *groups):
        super().__init__(pos, "stone", *groups)