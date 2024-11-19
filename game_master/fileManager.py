import os
import pygame.image
import settings
from game_master import gameSurface


game_surface = []
item_surface = []


def loading_item():
    item_surface.append(1)
    path_surface = os.path.join(settings.ITEMPATH, "surface")
    for name in os.listdir(path_surface):
        item_surface.append(gameSurface.GameSurface(pygame.image.load(os.path.join(path_surface, name)), name.split(".")[0]))
        item_surface[0] += 1
    return item_surface


def loading_game_surfaces():
    game_surface.append(1)
    path_surface = os.path.join(settings.GAMEPATH, "surface")
    for name in os.listdir(path_surface):
        temp = os.path.join(path_surface, name)
        for n in os.listdir(temp):
            game_surface.append(gameSurface.GameSurface(pygame.image.load(os.path.join(temp, n)), n.split(".")[0]))
    return game_surface