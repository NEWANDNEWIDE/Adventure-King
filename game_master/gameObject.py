import pygame.time
import game_master.fileManager

ATTRIBUTE = ("Health", "Shield", "Attack",
             "Defense", "Move_speed", "Attack_speed",
             "Critical_strike_chance", "Critical_strike_damage", "Reach_distance")


# 所有游戏npc的基类
class GameNpc(pygame.sprite.Sprite):
    def __init__(self, pos, group, name):
        super().__init__(group)
        self.__surface = game_master.fileManager.game_surface[name]
        self.attribute = game_master.gameObject.GameObject()
        self.attribute.rect = pos
        self.rect = self.__surface.get_rect(center=pos)
        self.vec2 = [0, 0]
        """self.index = 1
        self.image = self.__surface[self.index]"""

    def move(self, dt):
        self.attribute.rect[0] += self.vec2[0] * self.attribute.move_speed * dt
        self.attribute.rect[1] += self.vec2[1] * self.attribute.move_speed * dt
        self.rect.center = self.attribute.rect

    def action(self):
        pass

    def attack(self):
        pass

    def update(self):
        pass


class GameObject:
    def __init__(self):
        self.__name = ""
        self.__attribute = [0, 0, 0,
                            0, 0, 0,
                            0, 0, 0]
        self.__number = 0
        self.__limit = 1
        # 是否可以穿上
        self.dressed = 0
        # 位置
        self.rect = [-1, -1]

    @property
    def number(self):
        return self.__number

    @number.setter
    def number(self, number):
        self.__number = number

    @property
    def limit(self):
        return self.__limit

    @limit.setter
    def limit(self, limit):
        self.__limit = limit

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
    def attacked(self):
        return self.__attribute[2]

    @attacked.setter
    def attacked(self, attacked):
        self.__attribute[2] = attacked

    @property
    def defense(self):
        return self.__attribute[3]

    @defense.setter
    def defense(self, defense):
        self.__attribute[3] = defense

    @property
    def move_speed(self):
        return self.__attribute[4]

    @move_speed.setter
    def move_speed(self, move_speed):
        self.__attribute[4] = move_speed

    @property
    def attack_speed(self):
        return self.__attribute[5]

    @attack_speed.setter
    def attack_speed(self, attack_speed):
        self.__attribute[5] = attack_speed

    @property
    def critical_strike_chance(self):
        return self.__attribute[6]

    @critical_strike_chance.setter
    def critical_strike_chance(self, critical_strike_chance):
        self.__attribute[6] = critical_strike_chance

    @property
    def critical_strike_damage(self):
        return self.__attribute[7]

    @critical_strike_damage.setter
    def critical_strike_damage(self, critical_strike_damage):
        self.__attribute[7] = critical_strike_damage

    @property
    def reach_distance(self):
        return self.__attribute[8]

    @reach_distance.setter
    def reach_distance(self, reach_distance):
        self.__attribute[8] = reach_distance

    def create(self):
        return GameObject()

    def attack(self):
        pass

    def use(self):
        pass


# 装备
class IronArmor(GameObject):
    def __init__(self, name, limit=1, number=0):
        super().__init__()
        self.name = name
        self.limit = limit
        self.dressed = 1
        self.shield = 20
        self.surface = game_master.fileManager.game_surface[name]


# 武器
class WoodenSword(GameObject):
    def __init__(self, name="wooden-sword", limit=1, number=0):
        super().__init__()
        self.name = name
        self.limit = limit
        self.attack = 20
        self.reach_distance = 1
        self.surface = game_master.fileManager.game_surface[name]
        self.__sleep = 1000 // (self.attack_speed * (self.surface[0] - 2))
        self.__mid = (self.surface[0] - 1) // 2 + 1

    def left_attack(self, surface: pygame.surface.Surface):
        for i in range(2, self.__mid):
            surface.blit(self.surface[i], (400, 300))
            pygame.time.delay(self.__sleep)
        surface.blit(self.surface[1], (400, 300))

    def right_attack(self, surface: pygame.surface.Surface):
        for i in range(self.__mid + 1, self.surface[0]):
            surface.blit(self.surface[i], (400, 300))
            pygame.time.delay(self.__sleep)
        surface.blit(self.surface[1], (400, 300))


class StoneSword(WoodenSword):
    def __init__(self):
        super().__init__("stone-sword")
        self.attack += 20


class GoldenSword(WoodenSword):
    def __init__(self):
        super().__init__("golden-sword")
        self.attack += 30


class IronSword(WoodenSword):
    def __init__(self):
        super().__init__("iron-sword")
        self.attack += 40


class DiamondSword(WoodenSword):
    def __init__(self):
        super().__init__("stone-sword")
        self.attack += 60
