from __future__ import annotations
import pygame


class GameSurface:
    def __init__(self, surface: pygame.Surface, name: str):
        self.__surface = surface
        self.__name = name

    @property
    def surface(self):
        return self.__surface

    @surface.setter
    def surface(self, surface):
        self.__surface = surface

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name


class MapSprite(pygame.sprite.Sprite):
    def __init__(self, pos, surface, layer, *group):
        super().__init__(*group)
        self.image = surface
        self.rect = self.image.get_rect(topleft=pos)
        self.layer_g = layer


class GameSprite(pygame.sprite.Sprite):
    def __init__(self, game_object, *groups):
        super().__init__(*groups)
        self.attribute = game_object
        self.image = game_object.surface
        self.rect = self.image.get_rect(center=game_object.rect)
        self.time = 3
        self.get = 0


class PickUpSpritesGroup(pygame.sprite.Group):
    def __init__(self, player):
        super().__init__()
        self.player = player

    def update(self, *groups):
        for s in self.sprites():
            if s.get:
                if self.player.rect.colliderect(s.rect):
                    self.player.bag.put(s.attribute)
                    self.remove(s)
                    for g in groups:
                        g.remove(s)


class AttackingObj(pygame.sprite.Sprite):
    def __init__(self, damage, pos, who, time, *groups, **kwargs):
        super().__init__(*groups)
        self.who = who
        self.damage = damage
        self.pos = pos
        self.time = time
        if "image" in kwargs:
            self.image = kwargs["image"]
            self.rect = self.image.get_rect(center=pos)
        if "path" in kwargs:
            self.image = pygame.image.load(kwargs["path"])
            self.rect = self.image.get_rect(center=pos)
        if "rect" in kwargs:
            self.rect = kwargs["rect"]