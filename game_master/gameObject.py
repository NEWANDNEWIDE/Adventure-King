ATTRIBUTE = ("Health", "Shield", "Attack",
             "Defense", "Move_speed", "Attack_speed",
             "Critical_strike_chance", "Critical_strike_damage", "Reach_distance")


class GameObject:
    def __init__(self):
        self.__name = ""
        self.__attribute = [0, 0, 0,
                            0, 0, 0,
                            0, 0, 0]

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def health(self):
        return self.__attribute[0]

    @health.setter
    def health(self, health):
        self.__attribute[0] = health

    @property
    def shield(self):
        return self.__attribute[1]

    @shield.setter
    def shield(self, shield):
        self.__attribute[1] = shield

    @property
    def attack(self):
        return self.__attribute[2]

    @attack.setter
    def attack(self, attack):
        self.__attribute[2] = attack

    @property
    def defense(self):
        return self.__attribute[3]

    @defense.setter
    def defense(self, defense):
        self.__attribute[3] = defense

    @property
    def Move_speed(self):
        return self.__attribute[4]

    @Move_speed.setter
    def Move_speed(self, Move_speed):
        self.__attribute[4] = Move_speed

    @property
    def Attack_speed(self):
        return self.__attribute[5]

    @Attack_speed.setter
    def Attack_speed(self, Attack_speed):
        self.__attribute[5] = Attack_speed

    @property
    def Critical_strike_chance(self):
        return self.__attribute[6]

    @Critical_strike_chance.setter
    def Critical_strike_chance(self, Critical_strike_chance):
        self.__attribute[6] = Critical_strike_chance

    @property
    def Critical_strike_damage(self):
        return self.__attribute[7]

    @Critical_strike_damage.setter
    def Critical_strike_damage(self, Critical_strike_damage):
        self.__attribute[7] = Critical_strike_damage

    @property
    def Reach_distance(self):
        return self.__attribute[8]

    @Reach_distance.setter
    def Reach_distance(self, Reach_distance):
        self.__attribute[8] = Reach_distance
