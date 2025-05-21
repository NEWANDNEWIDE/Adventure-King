# 装备
import os
import pygame
import settings
from game_master.gameObject import GameObject


class Leather(GameObject):
    NAME = "leather"

    def __init__(self, name="leather", limit=1, number=1):
        super().__init__()
        self.attribute = self.attribute.copy()

        self.name = name
        self.limit = limit
        self.number = number if number <= limit else limit
        self.real_name = "皮甲"

        self.dressed = 1
        self.defense = 20

        path = os.path.join(settings.EQUIP, "armor_01a.png")
        self.surface = pygame.image.load(path).convert_alpha()
        max_v = max(self.surface.width, self.surface.height)
        max_v = 40 / max_v
        self.surface = pygame.transform.scale(self.surface,
                                              (self.surface.width * max_v, self.surface.height * max_v)).convert_alpha()
        self.mask = pygame.mask.from_surface(self.surface)

    @staticmethod
    def create(number=1):
        return Leather(number=number)


class GoldenArmor(GameObject):
    NAME = "golden_armor"

    def __init__(self, name="golden_armor", limit=1, number=1):
        super().__init__()
        self.attribute = self.attribute.copy()

        self.name = name
        self.limit = limit
        self.number = number if number <= limit else limit
        self.real_name = "金甲"

        self.dressed = 1
        self.defense = 40

        path = os.path.join(settings.EQUIP, "armor_01d.png")
        self.surface = pygame.image.load(path).convert_alpha()
        max_v = max(self.surface.width, self.surface.height)
        max_v = 40 / max_v
        self.surface = pygame.transform.scale(self.surface,
                                              (self.surface.width * max_v, self.surface.height * max_v)).convert_alpha()
        self.mask = pygame.mask.from_surface(self.surface)

    @staticmethod
    def create(number=1):
        return GoldenArmor(number=number)


class IronArmor(GameObject):
    NAME = "iron_armor"

    def __init__(self, name="iron_armor", limit=1, number=1):
        super().__init__()
        self.attribute = self.attribute.copy()

        self.name = name
        self.limit = limit
        self.number = number if number <= limit else limit
        self.real_name = "铁甲"

        self.dressed = 1
        self.defense = 80

        path = os.path.join(settings.EQUIP, "armor_01b.png")
        self.surface = pygame.image.load(path).convert_alpha()
        max_v = max(self.surface.width, self.surface.height)
        max_v = 40 / max_v
        self.surface = pygame.transform.scale(self.surface,
                                              (self.surface.width * max_v, self.surface.height * max_v)).convert_alpha()
        self.mask = pygame.mask.from_surface(self.surface)

    @staticmethod
    def create(number=1):
        return IronArmor(number=number)


class SapphireArmor(GameObject):
    NAME = "sapphire_armor"

    def __init__(self, name="sapphire_armor", limit=1, number=1):
        super().__init__()
        self.attribute = self.attribute.copy()

        self.name = name
        self.limit = limit
        self.number = number if number <= limit else limit
        self.real_name = "蓝宝石甲"

        self.dressed = 1
        self.defense = 140
        self.attacked = 70
        self.critical_strike_damage = 0.7
        self.critical_strike_chance = 0.7

        path = os.path.join(settings.EQUIP, "armor_01c.png")
        self.surface = pygame.image.load(path).convert_alpha()
        max_v = max(self.surface.width, self.surface.height)
        max_v = 40 / max_v
        self.surface = pygame.transform.scale(self.surface,
                                              (self.surface.width * max_v, self.surface.height * max_v)).convert_alpha()
        self.mask = pygame.mask.from_surface(self.surface)

    @staticmethod
    def create(number=1):
        return SapphireArmor(number=number)


class RubyArmor(GameObject):
    NAME = "ruby_armor"

    def __init__(self, name="ruby_armor", limit=1, number=1):
        super().__init__()
        self.attribute = self.attribute.copy()

        self.name = name
        self.limit = limit
        self.number = number if number <= limit else limit
        self.real_name = "红宝石甲"

        self.dressed = 1
        self.defense = 220
        self.health = 100
        self.shield = 120

        path = os.path.join(settings.EQUIP, "armor_01e.png")
        self.surface = pygame.image.load(path).convert_alpha()
        max_v = max(self.surface.width, self.surface.height)
        max_v = 40 / max_v
        self.surface = pygame.transform.scale(self.surface,
                                              (self.surface.width * max_v, self.surface.height * max_v)).convert_alpha()
        self.mask = pygame.mask.from_surface(self.surface)

    @staticmethod
    def create(number=1):
        return RubyArmor(number=number)


class Boots(GameObject):
    NAME = "boots"

    def __init__(self, name="boots", limit=1, number=1):
        super().__init__()
        self.attribute = self.attribute.copy()

        self.name = name
        self.limit = limit
        self.number = number if number <= limit else limit
        self.real_name = "皮靴"

        self.dressed = 1
        self.defense = 5
        self.move_speed = 20

        path = os.path.join(settings.EQUIP, "boots_01a.png")
        self.surface = pygame.image.load(path).convert_alpha()
        max_v = max(self.surface.width, self.surface.height)
        max_v = 40 / max_v
        self.surface = pygame.transform.scale(self.surface,
                                              (self.surface.width * max_v, self.surface.height * max_v)).convert_alpha()
        self.mask = pygame.mask.from_surface(self.surface)

    @staticmethod
    def create(number=1):
        return Boots(number=number)


class GoldenBoots(GameObject):
    NAME = "golden_boots"

    def __init__(self, name="golden_boots", limit=1, number=1):
        super().__init__()
        self.attribute = self.attribute.copy()

        self.name = name
        self.limit = limit
        self.number = number if number <= limit else limit
        self.real_name = "金靴"

        self.dressed = 1
        self.defense = 10
        self.move_speed = 20

        path = os.path.join(settings.EQUIP, "boots_01d.png")
        self.surface = pygame.image.load(path).convert_alpha()
        max_v = max(self.surface.width, self.surface.height)
        max_v = 40 / max_v
        self.surface = pygame.transform.scale(self.surface,
                                              (self.surface.width * max_v, self.surface.height * max_v)).convert_alpha()
        self.mask = pygame.mask.from_surface(self.surface)

    @staticmethod
    def create(number=1):
        return GoldenBoots(number=number)


class IronBoots(GameObject):
    NAME = "iron_boots"

    def __init__(self, name="iron_boots", limit=1, number=1):
        super().__init__()
        self.attribute = self.attribute.copy()

        self.name = name
        self.limit = limit
        self.number = number if number <= limit else limit
        self.real_name = "铁靴"

        self.dressed = 1
        self.defense = 20
        self.move_speed = 20

        path = os.path.join(settings.EQUIP, "boots_01b.png")
        self.surface = pygame.image.load(path).convert_alpha()
        max_v = max(self.surface.width, self.surface.height)
        max_v = 40 / max_v
        self.surface = pygame.transform.scale(self.surface,
                                              (self.surface.width * max_v, self.surface.height * max_v)).convert_alpha()
        self.mask = pygame.mask.from_surface(self.surface)

    @staticmethod
    def create(number=1):
        return IronBoots(number=number)


class SapphireBoots(GameObject):
    NAME = "sapphire_boots"

    def __init__(self, name="sapphire_boots", limit=1, number=1):
        super().__init__()
        self.attribute = self.attribute.copy()

        self.name = name
        self.limit = limit
        self.number = number if number <= limit else limit
        self.real_name = "蓝宝石靴"

        self.dressed = 1
        self.defense = 35
        self.move_speed = 40

        path = os.path.join(settings.EQUIP, "boots_01c.png")
        self.surface = pygame.image.load(path).convert_alpha()
        max_v = max(self.surface.width, self.surface.height)
        max_v = 40 / max_v
        self.surface = pygame.transform.scale(self.surface,
                                              (self.surface.width * max_v, self.surface.height * max_v)).convert_alpha()
        self.mask = pygame.mask.from_surface(self.surface)

    @staticmethod
    def create(number=1):
        return SapphireBoots(number=number)


class RubyBoots(GameObject):
    NAME = "ruby_boots"

    def __init__(self, name="ruby_boots", limit=1, number=1):
        super().__init__()
        self.attribute = self.attribute.copy()

        self.name = name
        self.limit = limit
        self.number = number if number <= limit else limit
        self.real_name = "红宝石靴"

        self.dressed = 1
        self.defense = 55
        self.move_speed = 30

        path = os.path.join(settings.EQUIP, "boots_01e.png")
        self.surface = pygame.image.load(path).convert_alpha()
        max_v = max(self.surface.width, self.surface.height)
        max_v = 40 / max_v
        self.surface = pygame.transform.scale(self.surface,
                                              (self.surface.width * max_v, self.surface.height * max_v)).convert_alpha()
        self.mask = pygame.mask.from_surface(self.surface)

    @staticmethod
    def create(number=1):
        return RubyArmor(number=number)


class LeatherHelmet(GameObject):
    NAME = "leather_helmet"

    def __init__(self, name="leather_helmet", limit=1, number=1):
        super().__init__()
        self.attribute = self.attribute.copy()

        self.name = name
        self.limit = limit
        self.number = number if number <= limit else limit
        self.real_name = "皮盔"

        self.dressed = 1
        self.defense = 5

        path = os.path.join(settings.EQUIP, "helmet_01a.png")
        self.surface = pygame.image.load(path).convert_alpha()
        max_v = max(self.surface.width, self.surface.height)
        max_v = 40 / max_v
        self.surface = pygame.transform.scale(self.surface,
                                              (self.surface.width * max_v, self.surface.height * max_v)).convert_alpha()
        self.mask = pygame.mask.from_surface(self.surface)

    @staticmethod
    def create(number=1):
        return LeatherHelmet(number=number)


class GoldenHelmet(GameObject):
    NAME = "golden_helmet"

    def __init__(self, name="golden_helmet", limit=1, number=1):
        super().__init__()
        self.attribute = self.attribute.copy()

        self.name = name
        self.limit = limit
        self.number = number if number <= limit else limit
        self.real_name = "金盔"

        self.dressed = 1
        self.defense = 10

        path = os.path.join(settings.EQUIP, "helmet_01d.png")
        self.surface = pygame.image.load(path).convert_alpha()
        max_v = max(self.surface.width, self.surface.height)
        max_v = 40 / max_v
        self.surface = pygame.transform.scale(self.surface,
                                              (self.surface.width * max_v, self.surface.height * max_v)).convert_alpha()
        self.mask = pygame.mask.from_surface(self.surface)

    @staticmethod
    def create(number=1):
        return GoldenHelmet(number=number)


class IronHelmet(GameObject):
    NAME = "iron_helmet"

    def __init__(self, name="iron_helmet", limit=1, number=1):
        super().__init__()
        self.attribute = self.attribute.copy()

        self.name = name
        self.limit = limit
        self.number = number if number <= limit else limit
        self.real_name = "铁盔"

        self.dressed = 1
        self.defense = 20

        path = os.path.join(settings.EQUIP, "helmet_01b.png")
        self.surface = pygame.image.load(path).convert_alpha()
        max_v = max(self.surface.width, self.surface.height)
        max_v = 40 / max_v
        self.surface = pygame.transform.scale(self.surface,
                                              (self.surface.width * max_v, self.surface.height * max_v)).convert_alpha()
        self.mask = pygame.mask.from_surface(self.surface)

    @staticmethod
    def create(number=1):
        return IronHelmet(number=number)


class SapphireHelmet(GameObject):
    NAME = "sapphire_helmet"

    def __init__(self, name="sapphire_helmet", limit=1, number=1):
        super().__init__()
        self.attribute = self.attribute.copy()

        self.name = name
        self.limit = limit
        self.number = number if number <= limit else limit
        self.real_name = "蓝宝石盔"

        self.dressed = 1
        self.defense = 35

        path = os.path.join(settings.EQUIP, "helmet_01c.png")
        self.surface = pygame.image.load(path).convert_alpha()
        max_v = max(self.surface.width, self.surface.height)
        max_v = 40 / max_v
        self.surface = pygame.transform.scale(self.surface,
                                              (self.surface.width * max_v, self.surface.height * max_v)).convert_alpha()
        self.mask = pygame.mask.from_surface(self.surface)

    @staticmethod
    def create(number=1):
        return SapphireHelmet(number=number)


class RubyHelmet(GameObject):
    NAME = "ruby_helmet"

    def __init__(self, name="ruby_helmet", limit=1, number=1):
        super().__init__()
        self.attribute = self.attribute.copy()

        self.name = name
        self.limit = limit
        self.number = number if number <= limit else limit
        self.real_name = "红宝石盔"

        self.dressed = 1
        self.defense = 55

        path = os.path.join(settings.EQUIP, "helmet_01e.png")
        self.surface = pygame.image.load(path).convert_alpha()
        max_v = max(self.surface.width, self.surface.height)
        max_v = 40 / max_v
        self.surface = pygame.transform.scale(self.surface,
                                              (self.surface.width * max_v, self.surface.height * max_v)).convert_alpha()
        self.mask = pygame.mask.from_surface(self.surface)

    @staticmethod
    def create(number=1):
        return RubyHelmet(number=number)