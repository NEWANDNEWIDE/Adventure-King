import control
import game_master.fileManager


class Item:
    def __init__(self):
        self.__bgp = []
        self.button_list = [1]
        self.surface_button_list = [1]
        self.box_list = [1]
        self.surface_box_list = [1]


class Bag:
    def __init__(self):
        self.__bag = [-1 for _ in range(36)]
        self.__state = False
        self.__surface = game_master.fileManager.game_surface["bag"]

    def insert(self, pos, data):
        self.__bag[pos] = data
