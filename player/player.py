import game_master.gameObject
import game_master.fileManager


class Player(game_master.gameObject.GameObject):
    def __init__(self):
        super().__init__()
        self.__surface = game_master.fileManager.game_surface["player"]
        self.__mid = (self.__surface[0] - 1) // 4

        self.__vec2 = (0, 0)
        self.__rect = (400, 300)

        self.health = 100
        self.attack = 5
        self.attack_speed = 1
        self.critical_strike_chance = 5
        self.critical_strike_damage = 1.5
        self.reach_distance = 1

    def move(self):
        pass