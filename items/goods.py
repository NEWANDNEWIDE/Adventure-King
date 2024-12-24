from __future__ import annotations
import os.path
import pygame.image
import game_master.gameObject
import settings


class BoxWhite(game_master.gameObject.GameObject):
    NAME = "box_white"

    def __init__(self, name="box_white", limit=64, number=1):
        super().__init__()
        self.name = name
        self.limit = limit
        self.number = number if number <= limit else limit
        self.real_name = "白银箱"

        path = os.path.join(settings.SPRITES, "box_1")
        path = os.path.join(path, "box_1_3.png")
        self.surface = pygame.image.load(path).convert_alpha()
        max_v = max(self.surface.width, self.surface.height)
        max_v = 40 / max_v
        self.surface = pygame.transform.scale(self.surface,
                                              (self.surface.width * max_v, self.surface.height * max_v)).convert_alpha()
        self.mask = pygame.mask.from_surface(self.surface)

    @staticmethod
    def create(number=1):
        return BoxWhite(number=number)


class BoxYellow(game_master.gameObject.GameObject):
    NAME = "box_yellow"

    def __init__(self, name="box_yellow", limit=64, number=1):
        super().__init__()
        self.name = name
        self.limit = limit
        self.number = number if number <= limit else limit
        self.real_name = "黄铜箱"

        path = os.path.join(settings.SPRITES, "box_2")
        path = os.path.join(path, "box_2_3.png")
        self.surface = pygame.image.load(path).convert_alpha()
        max_v = max(self.surface.width, self.surface.height)
        max_v = 40 / max_v
        self.surface = pygame.transform.scale(self.surface,
                                              (self.surface.width * max_v, self.surface.height * max_v)).convert_alpha()
        self.mask = pygame.mask.from_surface(self.surface)

    @staticmethod
    def create(number=1):
        return BoxYellow(number=number)


class CarrotMin(game_master.gameObject.GameObject):
    NAME = "carrot_min"

    def __init__(self, name="carrot_min", limit=64, number=1):
        super().__init__()
        self.name = name
        self.limit = limit
        self.number = number if number <= limit else limit
        self.real_name = "小胡萝卜"

        path = os.path.join(settings.SPRITES, "carrot")
        path = os.path.join(path, "carrot1.png")
        self.surface = pygame.image.load(path).convert_alpha()
        max_v = max(self.surface.width, self.surface.height)
        max_v = 40 / max_v
        self.surface = pygame.transform.scale(self.surface, (self.surface.width * max_v, self.surface.height * max_v)).convert_alpha()
        self.mask = pygame.mask.from_surface(self.surface)

    @staticmethod
    def create(number=1):
        return CarrotMin(number=number)


class CarrotBig(game_master.gameObject.GameObject):
    NAME = "carrot_big"

    def __init__(self, name="carrot_big", limit=64, number=1):
        super().__init__()
        self.name = name
        self.limit = limit
        self.number = number if number <= limit else limit
        self.real_name = "大胡萝卜"

        path = os.path.join(settings.SPRITES, "carrot")
        path = os.path.join(path, "carrot2.png")
        self.surface = pygame.image.load(path).convert_alpha()
        max_v = max(self.surface.width, self.surface.height)
        max_v = 40 / max_v
        self.surface = pygame.transform.scale(self.surface,
                                              (self.surface.width * max_v, self.surface.height * max_v)).convert_alpha()
        self.mask = pygame.mask.from_surface(self.surface)

    @staticmethod
    def create(number=1):
        return CarrotBig(number=number)


class Iron(game_master.gameObject.GameObject):
    NAME = "iron"

    def __init__(self, name="iron", limit=64, number=1):
        super().__init__()
        self.name = name
        self.limit = limit
        self.number = number if number <= limit else limit
        self.real_name = "铁锭"

        path = os.path.join(settings.SPRITES, "iron")
        path = os.path.join(path, "iron_07.png")
        self.surface = pygame.image.load(path).convert_alpha()
        max_v = max(self.surface.width, self.surface.height)
        max_v = 40 / max_v
        self.surface = pygame.transform.scale(self.surface,
                                              (self.surface.width * max_v, self.surface.height * max_v)).convert_alpha()
        self.mask = pygame.mask.from_surface(self.surface)

    @staticmethod
    def create(number=1):
        return Iron(number=number)


class Gold(game_master.gameObject.GameObject):
    NAME = "gold"

    def __init__(self, name="gold", limit=64, number=1):
        super().__init__()
        self.name = name
        self.limit = limit
        self.number = number if number <= limit else limit
        self.real_name = "金锭"

        path = os.path.join(settings.SPRITES, "gold")
        path = os.path.join(path, "metals7.png")
        self.surface = pygame.image.load(path).convert_alpha()
        max_v = max(self.surface.width, self.surface.height)
        max_v = 40 / max_v
        self.surface = pygame.transform.scale(self.surface,
                                              (self.surface.width * max_v, self.surface.height * max_v)).convert_alpha()
        self.mask = pygame.mask.from_surface(self.surface)

    @staticmethod
    def create(number=1):
        return Gold(number=number)


class Stone(game_master.gameObject.GameObject):
    NAME = "stone"

    def __init__(self, name="stone", limit=64, number=1):
        super().__init__()
        self.name = name
        self.limit = limit
        self.number = number if number <= limit else limit
        self.real_name = "石块"

        path = os.path.join(settings.SPRITES, "stone")
        path = os.path.join(path, "stone_02.png")
        self.surface = pygame.image.load(path).convert_alpha()
        max_v = max(self.surface.width, self.surface.height)
        max_v = 40 / max_v
        self.surface = pygame.transform.scale(self.surface,
                                              (self.surface.width * max_v, self.surface.height * max_v)).convert_alpha()
        self.mask = pygame.mask.from_surface(self.surface)

    @staticmethod
    def create(number=1):
        return Gold(number=number)