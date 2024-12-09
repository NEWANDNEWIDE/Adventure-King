import random
from typing import List
import pygame
from pytmx import TiledMap
import game_master.fileManager
import game_master.gameObject


class CameraGroup(pygame.sprite.Group):
    def __init__(self, surface: pygame.Surface, tmx=None):
        super().__init__()
        self.__display = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()
        self.__surface = surface

        self.h_w = self.__display.width // 2
        self.h_h = self.__display.height // 2

        self.ground_rect = self.__surface.get_rect(topleft=(0, 0))

        self.tmx: TiledMap = tmx

    def draw_tmx(self):
        for [layer] in self.tmx.visible_layers:
            for x, y, gid in layer:
                tile = self.tmx.get_tile_image_by_gid(gid)
                if tile:
                    self.__surface.blit(tile, (x * self.tmx.tilewidth, y * self.tmx.tileheight))

    def center_target_camera(self, target):
        self.offset.x = target[0] - self.h_w
        self.offset.y = target[1] - self.h_h

    def custom_draw(self, rect):
        if self.tmx:
            self.draw_tmx()

        self.center_target_camera(rect)

        ground_offset = self.ground_rect.topleft - self.offset
        self.__display.blit(self.__surface, ground_offset)

        # active elements
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.__display.blit(sprite.image, offset_pos)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)
        self.__surface = pygame.image.load(
            r"C:\Users\10962\Desktop\Pygame-Cameras-main\graphics\player.png").convert_alpha()
        # self.__l = (self.__surface[0] - 1) // 4
        self.__vec2 = [0, 0]

        # 是否打开合成台
        self.sys_state = 0
        # 是否奔跑
        self.run = 0
        # 闪避
        self.shanbi = 0
        self.shanbi_state = 1

        self.index = 1
        self.image = self.__surface
        self.attribute = game_master.gameObject.GameObject()
        self.spawn_point = pos
        self.attribute.rect = pos
        self.rect = self.__surface.get_rect(center=pos)

        # 头 胸 腿 靴
        self.armor = [0, 0, 0, 0]

        self.w = self.__surface.width
        self.h = self.__surface.height
        self.bag = Bag()

        self.attribute.health = 100
        self.attribute.attack = 5
        self.attribute.attack_speed = 1
        self.attribute.critical_strike_chance = 0.05
        self.attribute.critical_strike_damage = 1.5
        self.attribute.reach_distance = 1
        self.attribute.move_speed = 200

        self.attack_box = self.attribute.reach_distance * 50

    @property
    def vec2(self):
        return self.__vec2

    @vec2.setter
    def vec2(self, vec2):
        self.__vec2 = vec2

    def attack(self):
        if self.bag.bag[self.bag.selection_box]:
            chance = self.attribute.critical_strike_chance + self.bag.bag[self.bag.selection_box].critical_strike_chance
            damage = self.attribute.attack + self.bag.bag[self.bag.selection_box].attacked
            if self.attribute.critical_strike_chance < 1:
                r = random.random()
                damage = damage * self.attribute.critical_strike_damage if chance >= r else damage
            else:
                damage = damage * self.attribute.critical_strike_damage
        else:
            return

    def use(self):
        if self.bag.bag[self.bag.selection_box]:
            self.bag.bag[self.bag.selection_box].use()

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            self.__vec2[0] = 1
        elif keys[pygame.K_a]:
            self.__vec2[0] = -1
        else:
            self.__vec2[0] = 0
        if keys[pygame.K_s]:
            self.__vec2[1] = 1
        elif keys[pygame.K_w]:
            self.__vec2[1] = -1
        else:
            self.__vec2[1] = 0

    def move(self, dt):
        self.input()
        if not self.run and not self.shanbi_state:
            self.attribute.rect[0] += self.vec2[0] * self.attribute.move_speed * dt
            self.attribute.rect[1] += self.vec2[1] * self.attribute.move_speed * dt
        elif self.shanbi_state:
            if self.shanbi > 0:
                self.attribute.rect[0] += self.vec2[0] * self.attribute.move_speed * dt * 10
                self.attribute.rect[1] += self.vec2[1] * self.attribute.move_speed * dt * 10
                self.shanbi -= dt
            else:
                self.shanbi = -0.5
                self.shanbi_state = 0
        else:
            self.attribute.rect[0] += self.vec2[0] * self.attribute.move_speed * dt * 2
            self.attribute.rect[1] += self.vec2[1] * self.attribute.move_speed * dt * 2
        self.rect.centerx = self.attribute.rect[0]
        self.rect.centery = self.attribute.rect[1]
        if not self.shanbi_state and self.shanbi < 0:
            self.shanbi += dt

    def update(self, dt):
        self.move(dt)
        self.bag.update()
        if self.sys_state:
            self.sys_state.update()


class Bag:
    def __init__(self):
        # 背包是否打开
        self.__state = 0
        # 物品栏位置
        self.__inventory_rect = ((1200 - 422) / 2, 900 - 64)
        # 背包位置
        self.__rect = ((1200 - 458) / 2, (900 - 410) / 2)
        # 物品栏大小
        self.__inventory = pygame.Surface((422, 44))
        # 背包大小
        self.__background = pygame.Surface((458, 410))
        # 人物框大小
        self.__role_box = pygame.Surface((100, 166))
        # 保存每个格子的surface
        self.__frame = [pygame.Surface((40, 40)) for _ in range(49)]
        # 保存格子的状态, 用于判断是否改变
        self.__frame_state = [0 for _ in range(49)]
        # 保存合成格中物品之前存储的索引
        self.__synthesis = [0 for _ in range(4)]
        # 箭头
        self.arrowhead = pygame.Surface((40, 40))  # game_master.fileManager.game_surface["arrowhead"]
        self.arrowhead.fill((0, 0, 0))
        # 颜色, 偏移量
        self.offset = 2
        self.offset_rect = 20
        self.bg = (196, 196, 196)
        self.fg = (138, 138, 138)
        # 保存背包物品和空余数, 0-3是盔甲格子, 4-33是背包格子, 34-43是物品栏格子, 44-47是合成格子, 48是合成的物品格子
        self.__bag = [0 for _ in range(49)]
        self.__free = 40
        self.remaining_quantity = []
        # 物品栏选择框
        self.__box = pygame.Surface((44, 44))
        self.__selection_box = 34
        # 鼠标选择
        self.selection_offset = [0, 0]
        self.selection = 0
        self.selection_index = -1
        # 初始化格子
        for i in range(49):
            self.__frame[i].fill(self.fg)
        self.__role_box.fill((0, 0, 0))
        self.__inventory.fill(self.bg)
        self.__box.fill((0, 0, 0))
        self.setup()

    @property
    def state(self):
        return self.__state

    @property
    def frame_state(self):
        return self.__frame_state

    @frame_state.setter
    def frame_state(self, frame_state):
        self.__frame_state = frame_state

    @property
    def background(self):
        return self.__background

    @background.setter
    def background(self, background):
        self.__background = background

    @property
    def inventory(self):
        return self.__inventory

    @inventory.setter
    def inventory(self, inventory):
        self.__inventory = inventory

    @property
    def bag(self):
        return self.__bag

    @bag.setter
    def bag(self, bag):
        self.__bag = bag

    @property
    def selection_box(self):
        return self.__selection_box

    @selection_box.setter
    def selection_box(self, sb):
        self.__selection_box = sb

    @property
    def inventory_rect(self):
        return self.__inventory_rect

    @property
    def rect(self):
        return self.__rect

    @property
    def frame(self):
        return self.__frame

    @frame.setter
    def frame(self, frame):
        self.__frame = frame

    def setup(self, index=None):
        # 在index不为None的情况下为更新格子
        if not index:
            self.__background.fill(self.bg)
            self.__inventory.blit(self.__box, (42 * (self.__selection_box - 34), 0))
            for i in range(4):
                self.__background.blit(self.__frame[i], (self.offset_rect, self.offset_rect + (self.offset + 40) * i))
                self.__background.blit(self.__frame[44 + i], (272 + (self.offset + 40) * (i % 2),
                                                              self.offset_rect + self.offset + 40 + (
                                                                      self.offset + 40) * (i // 2)))
            self.__background.blit(self.__role_box, (self.offset_rect * 2 + 40, self.offset_rect))
            self.__background.blit(self.arrowhead, (356, 83))
            self.__background.blit(self.__frame[-1], (398, 83))
            for i in range(30):
                self.__background.blit(self.__frame[4 + i],
                                       (20 + (self.offset + 40) * (i % 10), 206 + (self.offset + 40) * (i // 10)))
            for i in range(10):
                self.__background.blit(self.__frame[34 + i], (20 + (self.offset + 40) * i, 350))
                self.__inventory.blit(self.__frame[34 + i], (2 + (self.offset + 40) * i, 2))
        else:
            for i in index:
                if 0 <= i <= 3:
                    self.__background.blit(self.__frame[i],
                                           (self.offset_rect, self.offset_rect + (self.offset + 40) * i))
                elif 4 <= i <= 33:
                    i -= 4
                    self.__background.blit(self.__frame[4 + i],
                                           (20 + (self.offset + 40) * (i % 10),
                                            206 + (self.offset + 40) * (i // 10)))
                elif 34 <= i <= 43:
                    i -= 34
                    self.__background.blit(self.__frame[34 + i], (20 + (self.offset + 40) * i, 350))
                    self.__inventory.blit(self.__frame[34 + i], (2 + (self.offset + 40) * i, 2))
                elif 44 <= i <= 47:
                    i -= 44
                    self.__background.blit(self.__frame[44 + i], (272 + (self.offset + 40) * (i % 2),
                                                                  self.offset_rect + self.offset + 40 + (
                                                                          self.offset + 40) * (i // 2)))
            if index[-1] >= 44:
                self.__background.blit(self.__frame[-1], (398, 83))

    def open(self):
        self.__state = 1

    def close(self):
        self.__state = 0
        if self.selection_index != -1:
            if self.selection_index > 43:
                t = self.selection
                self.selection = 0
                self.selection_index = -1
                self.selection_offset = [0, 0]
                if not self.put(t):
                    return self.out(obj=t)
            elif self.__bag[self.selection_index]:
                t = self.__bag[self.selection_index]
                n = t.number + self.selection.number
                if t.name == self.selection.name and t.limit >= n:
                    t.number = n
                    self.selection = 0
                    self.selection_index = -1
                    self.selection_offset = [0, 0]
                else:
                    t = self.selection
                    self.selection = 0
                    self.selection_index = -1
                    self.selection_offset = [0, 0]
                    if not self.put(t):
                        return self.out(obj=t)
            else:
                self.__frame_state[self.selection_index] = 1
                self.__bag[self.selection_index] = self.selection
                self.selection = 0
                self.selection_index = -1
                self.selection_offset = [0, 0]
        for i in range(4):
            if self.__synthesis[i]:
                if self.__synthesis[i] > 43:
                    t, n = self.__bag[44 + i], self.__synthesis[i]
                    self.__bag[44 + i] = 0
                    self.__synthesis[i] = 0
                    if not self.put(t):
                        return self.out(n)
                elif self.__bag[self.__synthesis[i]]:
                    t = self.__bag[self.__synthesis[i]]
                    n = t.number + self.__bag[44 + i].number
                    if t.name == self.__bag[44 + i].name and t.limit >= n:
                        t.number = n
                        self.__frame_state[self.__synthesis[i]] = 1
                        self.__frame_state[44 + i] = 1
                        self.__bag[44 + i] = 0
                        self.__synthesis[i] = 0
                    else:
                        t, n = self.__bag[44 + i], self.__synthesis[i]
                        self.__bag[44 + i] = 0
                        self.__synthesis[i] = 0
                        if not self.put(t):
                            return self.out(n)
                else:
                    self.__frame_state[self.__synthesis[i]] = 1
                    self.__frame_state[44 + i] = 1
                    self.__bag[self.__synthesis[i]] = self.__bag[44 + i]
                    self.__bag[44 + i] = 0
                    self.__synthesis[i] = 0
        return 0

    def use(self):
        if self.__bag[self.__selection_box]:
            self.__bag[self.__selection_box].use()

    def selected(self, pos: List[int], state):
        pos = list(pos)
        pos[0] -= self.__rect[0]
        pos[1] -= self.__rect[1]
        if state == game_master.synthesis.SYNTHESIS:
            print(pos)
            if 20 <= pos[0] <= 438:
                if 206 <= pos[1] <= 330:
                    print(4)
                    pos[0] -= 20
                    pos[1] -= 206
                    i, j = 0, 0
                    for i in range(3):
                        pos[1] -= 40
                        if pos[1] <= 0:
                            if pos[0] > 0:
                                for j in range(10):
                                    pos[0] -= 40
                                    if pos[0] <= 0:
                                        break
                                    elif 0 < pos[0] < 2:
                                        return
                                    pos[0] -= 2
                            break
                        elif 0 < pos[1] < 2:
                            return
                        pos[1] -= 2
                    i = 4 + i * 10 + j
                    if self.selection_index == -1:
                        if self.__bag[i]:
                            self.selection_offset = [pos[0] + 40, pos[1] + 40]
                            self.selection_index = i
                            self.selection = self.__bag[i]
                            self.__bag[i] = 0
                            self.__frame_state[i] = 1
                    else:
                        if self.__bag[i]:
                            self.selection_index = i
                            t = self.selection
                            self.selection = self.__bag[i]
                            self.__bag[i] = t
                        else:
                            self.__bag[i] = self.selection
                            self.selection_offset = [0, 0]
                            self.selection_index = -1
                            self.selection = 0
                        self.__frame_state[i] = 1
                elif 350 <= pos[1] <= 390:
                    print(5)
                    pos[0] -= 20
                    i = 0
                    for i in range(10):
                        pos[0] -= 40
                        if pos[0] <= 0:
                            break
                        elif 0 < pos[0] < 2:
                            return
                        pos[0] -= 2
                    i = 34 + i
                    if self.selection_index == -1:
                        if self.__bag[i]:
                            self.selection_offset = [pos[0] + 40, pos[1] - 350]
                            self.selection_index = i
                            self.selection = self.__bag[i]
                            self.__bag[i] = 0
                            self.__frame_state[i] = 1
                    else:
                        if self.__bag[i]:
                            self.selection_index = i
                            t = self.selection
                            self.selection = self.__bag[i]
                            self.__bag[i] = t
                        else:
                            self.__bag[i] = self.selection
                            self.selection_offset = [0, 0]
                            self.selection_index = -1
                            self.selection = 0
                        self.__frame_state[i] = 1
            elif pos[0] < 0 or pos[0] > 458 or pos[1] < 0 or pos[1] > 410:
                print(pos)
                if self.selection_index != -1:
                    self.out(self.selection_index)
                    self.selection_index = -1
                    self.selection = 0
                    self.selection_offset = [0, 0]
        else:
            if 20 <= pos[0] <= 60 and 20 <= pos[1] <= 186:
                pos[1] -= 20
                i = 0
                for i in range(4):
                    pos[1] -= 40
                    if pos[1] <= 0:
                        break
                    elif 0 < pos[1] < 2:
                        return
                    pos[1] -= 2
                if self.selection_index == -1:
                    if self.__bag[i]:
                        self.selection_offset = [pos[0] - 20, pos[1] + 40]
                        self.selection_index = i
                        self.selection = self.__bag[i]
                        self.__bag[i] = 0
                        self.__frame_state[i] = 1
                else:
                    if self.__bag[i]:
                        self.selection_index = i
                        t = self.selection
                        self.selection = self.__bag[i]
                        self.__bag[i] = t
                    else:
                        self.__bag[i] = self.selection
                        self.selection_offset = [0, 0]
                        self.selection_index = -1
                        self.selection = 0
                    self.__frame_state[i] = 1
            elif 272 <= pos[0] <= 356 and 62 <= pos[1] <= 144:
                pos[0] -= 272
                pos[1] -= 62
                i, j = 0, 0
                for i in range(2):
                    pos[1] -= 40
                    if pos[1] <= 0:
                        if pos[0] > 0:
                            for j in range(2):
                                pos[0] -= 40
                                if pos[0] <= 0:
                                    break
                                elif 0 < pos[0] < 2:
                                    return
                                pos[0] -= 2
                        break
                    elif 0 < pos[1] < 2:
                        return
                    pos[1] -= 2
                k = i
                i = 44 + i * 2 + j
                if self.selection_index == -1:
                    if self.__bag[i]:
                        self.selection_offset = [pos[0] + 40, pos[1] + 40]
                        self.selection_index = self.__synthesis[k * 2 + j]
                        self.selection = self.__bag[i]
                        self.__synthesis[k * 2 + j] = 0
                        self.__bag[i] = 0
                        self.__frame_state[i] = 1
                        self.__frame_state[-1] = 1
                else:
                    if self.__bag[i]:
                        n = self.__synthesis[k * 2 + j]
                        self.__synthesis[k * 2 + j] = self.selection_index
                        self.selection_index = n
                        t = self.selection
                        self.selection = self.__bag[i]
                        self.__bag[i] = t
                    else:
                        self.__bag[i] = self.selection
                        self.__synthesis[k * 2 + j] = self.selection_index
                        self.selection_offset = [0, 0]
                        self.selection_index = -1
                        self.selection = 0
                    self.__frame_state[i] = 1
                    self.__frame_state[-1] = 1
            elif 398 <= pos[0] <= 438 and 83 <= pos[1] <= 123:
                if self.selection_index == -1 and self.__bag[48]:
                    self.selection_offset = [pos[0] - 398, pos[1] - 83]
                    self.selection_index = 48
                    self.selection = self.__bag[48]
                    self.__bag[48] = 0
                    self.__frame_state[48] = 1
                    for i in self.remaining_quantity:
                        self.__bag[i] = 0
                        self.__frame_state[i] = 1
            elif 20 <= pos[0] <= 438:
                if 206 <= pos[1] <= 330:
                    pos[0] -= 20
                    pos[1] -= 206
                    i, j = 0, 0
                    for i in range(3):
                        pos[1] -= 40
                        if pos[1] <= 0:
                            if pos[0] > 0:
                                for j in range(10):
                                    pos[0] -= 40
                                    if pos[0] <= 0:
                                        break
                                    elif 0 < pos[0] < 2:
                                        return
                                    pos[0] -= 2
                            break
                        elif 0 < pos[1] < 2:
                            return
                        pos[1] -= 2
                    i = 4 + i * 10 + j
                    if self.selection_index == -1:
                        if self.__bag[i]:
                            self.selection_offset = [pos[0] + 40, pos[1] + 40]
                            self.selection_index = i
                            self.selection = self.__bag[i]
                            self.__bag[i] = 0
                            self.__frame_state[i] = 1
                    else:
                        if self.__bag[i]:
                            self.selection_index = i
                            t = self.selection
                            self.selection = self.__bag[i]
                            self.__bag[i] = t
                        else:
                            self.__bag[i] = self.selection
                            self.selection_offset = [0, 0]
                            self.selection_index = -1
                            self.selection = 0
                        self.__frame_state[i] = 1
                elif 350 <= pos[1] <= 390:
                    pos[0] -= 20
                    i = 0
                    for i in range(10):
                        pos[0] -= 40
                        if pos[0] <= 0:
                            break
                        elif 0 < pos[0] < 2:
                            return
                        pos[0] -= 2
                    i = 34 + i
                    if self.selection_index == -1:
                        if self.__bag[i]:
                            self.selection_offset = [pos[0] + 40, pos[1] - 350]
                            self.selection_index = i
                            self.selection = self.__bag[i]
                            self.__bag[i] = 0
                            self.__frame_state[i] = 1
                    else:
                        if self.__bag[i]:
                            self.selection_index = i
                            t = self.selection
                            self.selection = self.__bag[i]
                            self.__bag[i] = t
                        else:
                            self.__bag[i] = self.selection
                            self.selection_offset = [0, 0]
                            self.selection_index = -1
                            self.selection = 0
                        self.__frame_state[i] = 1
            elif pos[0] < 0 or pos[0] > 458 or pos[1] < 0 or pos[1] > 410:
                if self.selection_index != -1:
                    self.out(self.selection_index)
                    self.selection_index = -1
                    self.selection = 0
                    self.selection_offset = [0, 0]

    def put(self, obj):
        for i in range(40):
            if self.bag[4 + i] and self.bag[4 + i].name == obj.name and self.bag[4 + i].limit > self.bag[4 + i].number:
                self.__frame_state[4 + i] = 1
                t = self.__bag[4 + i]
                n = t.number + obj.number
                if t.limit >= n:
                    t.number = n
                    return 1
                else:
                    obj.number -= t.limit - t.number
                    t.number = t.limit
        if self.__free:
            for i in range(40):
                if not self.__bag[4 + i]:
                    self.__bag[4 + i] = obj
                    self.__frame_state[4 + i] = 1
                    self.__free -= 1
                    print(4 + i)
                    return 1
        return 0

    def out(self, index=-1, obj=None):
        if obj:
            return obj
        if index != -1:
            t = self.__bag[index]
            self.__frame_state[index] = 1
            self.__bag[index] = 0
            self.__free += 1
            return t
        return 0

    def synthesis(self):
        number = []
        for i in range(4):
            if self.__frame_state[44 + i] and self.__bag[44 + i]:
                number.append(i)
        if not number:
            return 0
        state = 1
        ans = 0
        obj = 0
        for g in game_master.synthesis.PLAYER_SYNTHESIS_LIST:
            l = len(g) - 1
            if len(number) == l:
                for i in range(l):
                    if self.__bag[44 + number[i]].name != g[i][0] or self.__bag[44 + number[i]].number < g[i][1]:
                        state = 0
                        break
                if state:
                    i = 0
                    while self.__bag[44 + number[i]].number >= g[i][1]:
                        self.__bag[44 + number[i]].number -= g[i][1]
                        if i == l - 1:
                            i = 0
                            ans += 1
                        else:
                            i += 1
                    obj = g
                    break
        if ans and obj:
            self.__bag[-1] = game_master.className.GOODS[obj[-1][0]](obj[-1][0], number=ans)
            self.__frame_state[-1] = 1
            temp = []
            for i in range(len(number)):
                if self.__bag[number[i] + 44].number == 0:
                    temp.append(number[i] + 44)
            return temp
        else:
            if self.__bag[-1]:
                self.__bag[-1] = 0
                self.__frame_state[-1] = 1
        return 0

    def update_inventory(self):
        if self.selection_box < 34:
            self.selection_box = 34
        elif self.selection_box > 43:
            self.selection_box = 43
        self.__inventory.fill(self.bg)
        self.__inventory.blit(self.__box, (42 * (self.__selection_box - 34), 0))
        for i in range(10):
            self.__inventory.blit(self.__frame[34 + i], (2 + (self.offset + 40) * i, 2))

    def update(self):
        temp = []
        if not self.remaining_quantity:
            t = self.synthesis()
            self.remaining_quantity = t if t else []
        for i in range(49):
            if self.__frame_state[i]:
                self.__frame[i].fill(self.fg)
                if self.__bag[i]:
                    # pygame.transform.scale(self.__bag[i].surface, (40, 40), self.__frame[i])
                    self.__frame[i].blit(self.__bag[i].surface)
                self.__frame_state[i] = 0
                temp.append(i)
        self.setup(temp)

    def render_inventory(self):
        pygame.display.get_surface().blit(self.__inventory, self.__inventory_rect)

    def render(self):
        if self.__state:
            pygame.display.get_surface().blit(self.__background, self.__rect)
            if self.selection_index != -1:
                pos = pygame.mouse.get_pos()
                pygame.display.get_surface().blit(self.selection.surface, (
                    pos[0] - self.selection_offset[0], pos[1] - self.selection_offset[1]))
