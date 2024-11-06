import os
import settings
from game_master import gameSurface


game_surface = {}


def loading_item():
    path_surface = os.path.join(settings.ITEMPATH, "surface")
    item_surface = {}
    for name in os.listdir(path_surface):
        t = name.split(".")[0]
        item_surface[t] = gameSurface.HaveNameSurface.load(file=os.path.join(path_surface, name), name=t)
    return item_surface


def loading_game_surfaces():
    path_surface = os.path.join(settings.GAMEPATH, "surface")
    for name in os.listdir(path_surface):
        t = [1]
        temp = os.path.join(path_surface, name)
        for n in os.listdir(temp):
            t.append(gameSurface.HaveNameSurface.load(file=os.path.join(temp, n), name=n.split(".")[0]))
            t[0] += 1
        game_surface[name] = tuple(t)
    return game_surface