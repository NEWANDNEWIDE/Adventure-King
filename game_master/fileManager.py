import os
import settings
from game_master import gameSurface


def loading_item():
    path_surface = os.path.join(settings.ITEMPATH, "surface")
    item_surface = {}
    for name in os.listdir(path_surface):
        t = name.split(".")[0]
        item_surface[t] = gameSurface.HaveNameSurface.load(file=os.path.join(path_surface, name), name=t)
    return item_surface


def loading_game_surfaces():
    path_surface = os.path.join(settings.GAMEPATH, "surface")
    game_surface = {}
    for name in os.listdir(path_surface):
        t = name.split(".")[0]
        game_surface[t] = gameSurface.HaveNameSurface.load(file=os.path.join(path_surface, name), name=t)
    return game_surface