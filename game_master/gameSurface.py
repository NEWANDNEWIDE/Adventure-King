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


class MapSpirit(pygame.sprite.Sprite):
    def __init__(self, pos, surface, name, layer, *group):
        super().__init__(*group)
        self.image = surface
        self.rect = self.image.get_rect(topleft=pos)
        self.name = name
        self.layer = layer


class GameSpirit(pygame.sprite.Sprite):
    def __init__(self, game_object, *groups):
        super().__init__(*groups)
        self.attribute = game_object
        self.image = game_object.surface[game_object.index]
        self.rect = self.image.get_rect(center=game_object.rect)
        self.time = 3
        self.get = 0


class PickUpSpritesGroup(pygame.sprite.Group):
    def __init__(self, player):
        super().__init__()
        self.player = player
        self.box = pygame.Surface((self.player.image.width + self.player.attack_box, self.player.image.height + self.player.attack_box))
        self.rect = self.box.get_rect(center=self.player.attribute.rect)

    def update(self):
        self.box = pygame.Surface((self.player.image.width + self.player.attack_box, self.player.image.height + self.player.attack_box))
        self.rect = self.box.get_rect(center=self.player.attribute.rect)
        for s in self.sprites():
            if self.rect.colliderect(s.rect):
                self.player.bag.put(s.attribute)
                self.remove(s)