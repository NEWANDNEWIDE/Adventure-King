from __future__ import annotations
import pygame
import game_master
import items.goods
import game_player.player
from game_master.gameObject import GameObject
from items import className

SYNTHESIS = 114514
# 人物身上的合成
# 类名可在className.GOODS里加入或查看(GOODS.items())
PLAYER_SYNTHESIS_LIST_NOT_PROCESSED = [
    # 五个格子, 前四个以(类名, 数量, (偏移x, 偏移y) or 位置)写入, 最后一个以(类名, 数量)为输出, 其中偏移为对前一个物品的位置偏移, 第一个物品无偏移(类名, 数量) or (类名, 数量, 位置)
    # (0, 0)为左上角第一个格子, 往右一格为(1, 0), 往下一格为(0, 1)
    # 偏移x为正代表在前一个物品的左边, 反之为右边
    # 偏移y为正代表在前一个物品的上面, 反之为下面
    ((items.goods.Iron.NAME, 1), (items.goods.Iron.NAME, 1, (1, 0)), (items.armors.IronBoots.NAME, 1)),
    ((items.goods.Iron.NAME, 1), (items.goods.Iron.NAME, 1, (0, -1)), (items.weapons.Blades.NAME, 1)),
    ((items.goods.Iron.NAME, 1), (items.goods.Iron.NAME, 1, (1, 0)), (items.armors.IronBoots.NAME, 1)),
    ((items.goods.Iron.NAME, 1), (items.goods.Iron.NAME, 1, (0, -1)), (items.weapons.Blades.NAME, 1)),
    ((items.goods.Iron.NAME, 1), (items.goods.Iron.NAME, 1, (1, 0)), (items.armors.IronBoots.NAME, 1)),
    ((items.goods.Iron.NAME, 1), (items.goods.Iron.NAME, 1, (0, -1)), (items.weapons.Blades.NAME, 1)),
    ((items.goods.Iron.NAME, 1), (items.goods.Iron.NAME, 1, (1, 0)), (items.armors.IronBoots.NAME, 1)),
    ((items.goods.Iron.NAME, 1), (items.goods.Iron.NAME, 1, (0, -1)), (items.weapons.Blades.NAME, 1)),
    ((items.goods.Iron.NAME, 1), (items.goods.Iron.NAME, 1, (1, 0)), (items.armors.IronBoots.NAME, 1)),
    ((items.goods.Iron.NAME, 1), (items.goods.Iron.NAME, 1, (0, -1)), (items.weapons.Blades.NAME, 1)),
    ((items.goods.Iron.NAME, 1), (items.goods.Iron.NAME, 1, (1, 0)), (items.armors.IronBoots.NAME, 1))
]

SYNTHESIS_LIST_NOT_PROCESSED = [
    # 十个格子, 前九个以(类名, 数量)写入, 最后一个为输出

]

PLAYER_SYNTHESIS_LIST = []
SYNTHESIS_LIST = []


def process(start: list, number: int = 2):
    target = []
    for g in start:
        l = len(g) - 1
        if l == 1:
            target.append(g)
        else:
            t = []
            if len(g[0]) == 3:
                t.append(g)
            else:
                t.append((g[0][0], g[0][1], -1))
            if isinstance(g[1][-1], tuple):
                for i in range(1, l):
                    t.append((g[i][0], g[i][1], t[-1][-1] + g[i][-1][0] - g[i][-1][1] * number))
            else:
                for i in range(1, l):
                    t.append(g[i])
            t.sort(key=lambda k: k[-1])
            t.append(g[l])
            target.append(tuple(t))
    return target


class Synthesis(pygame.sprite.Sprite):
    def __init__(self, pos, group, bag: game_player.player.Bag):
        super().__init__(group)

        self.attribute = GameObject().copy()
        self.attribute.name = "synthesis"
        self.attribute.rect = pos
        self.surface = pygame.Surface((40, 40))
        self.image = self.surface
        self.rect = self.image.get_rect(center=pos)

        self.double_right = 0
        self.time = 300
        self.start = 0

        self.bag = bag
        # 合成界面是否打开
        self.state = 0
        # 合成界面的大小与背包一样
        self.__background = pygame.Surface((458, 410))
        # 合成格子
        self.__frame = [pygame.Surface((40, 40)) for _ in range(10)]
        # 保存格子的状态, 用于判断是否改变
        self.__frame_state = [0 for _ in range(10)]
        # 存储合成
        self.__synthesis = [0 for _ in range(10)]
        # 存储索引
        self.__synthesis_index = [0 for _ in range(9)]
        # 剩余数量
        self.remaining_quantity = []
        self.__background.fill(self.bag.bg)
        for i in range(10):
            self.__frame[i].fill(self.bag.fg)

    def setup(self, index=None):
        if not index:
            for i in range(9):
                self.__background.blit(self.__frame[i], (107 + (self.bag.offset + 40) * (i % 3),
                                                         self.bag.offset_rect + (self.bag.offset + 40) * (i // 3)))
            self.__background.blit(self.bag.arrowhead, (251, 62))
            self.__background.blit(self.__frame[-1], (311, 62))
            for i in range(30):
                self.__background.blit(self.bag.frame[4 + i],
                                       (20 + (self.bag.offset + 40) * (i % 10),
                                        206 + (self.bag.offset + 40) * (i // 10)))
            for i in range(10):
                self.__background.blit(self.bag.frame[34 + i], (20 + (self.bag.offset + 40) * i, 350))
        else:
            for i in index:
                if i <= 8:
                    self.__background.blit(self.__frame[i], (
                        107 + (self.bag.offset + 40) * (i % 3),
                        self.bag.offset_rect + (self.bag.offset + 40) * (i // 3)))
            self.__background.blit(self.__frame[-1], (311, 62))

    def open(self):
        self.state = 1
        return self

    def close(self):
        self.state = 0
        self.bag.close()
        for i in range(9):
            if self.__synthesis_index[i]:
                if self.bag.bag[self.__synthesis_index[i]]:
                    t = self.bag.bag[self.__synthesis_index[i]]
                    n = t.number + self.__synthesis[i].number
                    if t.name == self.__synthesis[i].name and t.limit >= n:
                        t.number = n
                        self.bag.frame_state[self.__synthesis[i]] = 1
                        self.__frame_state[i] = 1
                        self.__synthesis[i] = 0
                        self.__synthesis_index[i] = 0
                    else:
                        t, n = self.__synthesis[i], self.__synthesis_index[i]
                        self.__synthesis[i] = 0
                        self.__synthesis_index[i] = 0
                        if not self.bag.put(t):
                            return self.bag.out(n)
                else:
                    self.bag.frame_state[self.__synthesis_index[i]] = 1
                    self.__frame_state[i] = 1
                    self.bag.bag[self.__synthesis_index[i]] = self.__synthesis[i]
                    self.__synthesis[i] = 0
                    self.__synthesis_index[i] = 0
        return 0

    def selected(self, pos, state):
        losing = self.bag.selected(pos, state, 1)
        if losing:
            return losing
        pos = list(pos)
        pos[0] -= self.bag.rect[0]
        pos[1] -= self.bag.rect[1]
        if 107 <= pos[0] <= 231 and 20 <= pos[1] <= 144:
            pos[0] -= 107
            pos[1] -= 20
            i, j = 0, 0
            for i in range(3):
                pos[1] -= 40
                if pos[1] <= 0:
                    if pos[0] >= 0:
                        for j in range(3):
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
            i = i * 3 + j
            if self.bag.selection_index == -1:
                if self.__synthesis[i]:
                    self.bag.selection_offset = [pos[0] + 40, pos[1] + 40]
                    self.bag.selection_index = self.__synthesis_index[i]
                    if state == pygame.BUTTON_LEFT or self.__synthesis[i].number == 1:
                        self.bag.selection = self.__synthesis[i]
                        self.__synthesis_index[i] = 0
                        self.__synthesis[i] = 0
                    elif state == pygame.BUTTON_RIGHT:
                        mid = self.__synthesis[i].number // 2
                        self.bag.selection = className.GOODS[self.__synthesis[i].NAME](mid)
                        self.__synthesis[i].number -= mid
                    self.__frame_state[i] = 1
                    self.bag.selection_state = 1
                    self.remaining_quantity = self.synthesis()
            else:
                if self.__synthesis[i]:
                    if self.bag.selection.name != self.__synthesis[i].name or self.__synthesis[i].number == self.__synthesis[i].limit:
                        n = self.__synthesis_index[i]
                        self.__synthesis_index[i] = self.bag.selection_index
                        self.bag.selection_index = n
                        t = self.bag.selection
                        self.bag.selection = self.__synthesis[i]
                        self.__synthesis[i] = t
                    elif state == pygame.BUTTON_LEFT:
                        t = self.bag.selection.number + self.__synthesis[i].number
                        if self.__synthesis[i].limit >= t:
                            self.__synthesis[i].number = t
                            self.bag.selection = 0
                            self.bag.selection_index = -1
                        else:
                            t -= self.__synthesis[i].limit
                            self.__synthesis[i].number = self.__synthesis[i].limit
                            self.bag.selection.number = t
                    elif state == pygame.BUTTON_RIGHT:
                        t = 1 + self.__synthesis[i].number
                        if self.__synthesis[i].limit >= t:
                            self.__synthesis[i].number = t
                            self.bag.selection.number -= 1
                        else:
                            t = self.__synthesis[i].limit - self.__synthesis[i].number
                            self.__synthesis[i].number = self.__synthesis[i].limit
                            self.bag.selection.number -= t
                else:
                    if state == pygame.BUTTON_LEFT or self.bag.selection.number == 1:
                        self.__synthesis[i] = self.bag.selection
                        self.__synthesis_index[i] = self.bag.selection_index
                        self.bag.selection_offset = [0, 0]
                        self.bag.selection_index = -1
                        self.bag.selection = 0
                    elif state == pygame.BUTTON_RIGHT:
                        self.__synthesis[i] = className.GOODS[self.bag.selection.NAME](1)
                        self.__synthesis_index[i] = self.bag.selection_index
                        self.bag.selection.number -= 1
                self.bag.selection_state = 1
                self.__frame_state[i] = 1
                self.remaining_quantity = self.synthesis()
        elif 311 <= pos[0] <= 351 and 62 <= pos[1] <= 102:
            if self.__synthesis[9]:
                if self.bag.selection_index == -1:
                    self.bag.selection_offset = [pos[0] - 311, pos[1] - 62]
                    self.bag.selection_index = 48
                    self.bag.selection_state = 1
                    if state == pygame.BUTTON_LEFT:
                        self.bag.selection = className.GOODS[self.__synthesis[9].NAME](self.remaining_quantity[-2])
                        self.remaining_quantity[-1] -= 1
                        for i in range(len(self.remaining_quantity) - 2):
                            self.__synthesis[self.remaining_quantity[i][1]].number -= self.remaining_quantity[i][0]
                            if not self.__synthesis[self.remaining_quantity[i][1]].number:
                                self.__synthesis[self.remaining_quantity[i][1]] = 0
                                self.__synthesis_index[self.remaining_quantity[i][1]] = 0
                            self.__frame_state[self.remaining_quantity[i][1]] = 1
                        if not self.remaining_quantity[-1]:
                            self.remaining_quantity = self.synthesis()
                    elif state == pygame.BUTTON_RIGHT:
                        if self.__synthesis[9].limit >= self.remaining_quantity[-2] * self.remaining_quantity[-1]:
                            self.bag.selection = self.__synthesis[9]
                            self.bag.selection.number = self.remaining_quantity[-2] * self.remaining_quantity[-1]
                        else:
                            self.bag.selection = className.GOODS[self.__synthesis[9].NAME](self.__synthesis[9].limit)
                            t = self.remaining_quantity[-2] * self.remaining_quantity[-1] - self.__synthesis[9].limit
                            group = t // self.__synthesis[9].limit
                            t -= group * self.__synthesis[9].limit
                            for i in range(group):
                                self.bag.put(className.GOODS[self.__synthesis[9].NAME](self.__synthesis[9].limit))
                            if t:
                                self.bag.put(className.GOODS[self.__synthesis[9].NAME](t))
                        self.__synthesis[9] = 0
                        self.__frame_state[9] = 1
                        for i in range(len(self.remaining_quantity) - 2):
                            self.__synthesis[self.remaining_quantity[i][1]].number -= self.remaining_quantity[i][0] * \
                                                                                self.remaining_quantity[-1]
                            if not self.__synthesis[self.remaining_quantity[i][1]].number:
                                self.__synthesis[self.remaining_quantity[i][1]] = 0
                                self.__synthesis_index[self.remaining_quantity[i][1]] = 0
                            self.__frame_state[self.remaining_quantity[i][1]] = 1
                        self.remaining_quantity = self.synthesis()
                elif self.bag.selection.name == self.__synthesis[9].name and self.__synthesis[9].number != self.__synthesis[9].limit:
                    if (state == pygame.BUTTON_LEFT and
                            self.bag.selection.number + self.remaining_quantity[-2] <= self.bag.selection.limit):
                        self.bag.selection.number += self.remaining_quantity[-2]
                        self.bag.selection_state = 1
                        self.remaining_quantity[-1] -= 1
                        for i in range(len(self.remaining_quantity) - 2):
                            self.__synthesis[self.remaining_quantity[i][1]].number -= self.remaining_quantity[i][0]
                            if not self.__synthesis[self.remaining_quantity[i][1]].number:
                                self.__synthesis[self.remaining_quantity[i][1]] = 0
                                self.__synthesis_index[self.remaining_quantity[i][1]] = 0
                            self.__frame_state[self.remaining_quantity[i][1]] = 1
                        if not self.remaining_quantity[-1]:
                            self.remaining_quantity = self.synthesis()
                    elif state == pygame.BUTTON_RIGHT:
                        if self.bag.selection.limit - self.bag.selection.number >= self.remaining_quantity[-2] * \
                                self.remaining_quantity[-1]:
                            self.bag.selection.number += self.remaining_quantity[-2] * self.remaining_quantity[-1]
                        else:
                            t = self.remaining_quantity[-2] * self.remaining_quantity[
                                -1] - self.bag.selection.limit + self.bag.selection.number
                            self.bag.selection.number = self.bag.selection.limit
                            group = t // self.bag.selection.limit
                            t -= group * self.bag.selection.limit
                            for i in range(group):
                                self.bag.put(className.GOODS[self.bag.selection.NAME](self.bag.selection.limit))
                            if t:
                                self.bag.put(className.GOODS[self.bag.selection.NAME](t))
                        self.bag.selection_state = 1
                        self.__synthesis[9] = 0
                        self.__frame_state[9] = 1
                        for i in range(len(self.remaining_quantity) - 2):
                            self.__synthesis[self.remaining_quantity[i][1]].number -= self.remaining_quantity[i][0] * \
                                                                                self.remaining_quantity[-1]
                            if not self.__synthesis[self.remaining_quantity[i][1]].number:
                                self.__synthesis[self.remaining_quantity[i][1]] = 0
                                self.__synthesis_index[self.remaining_quantity[i][1]] = 0
                            self.__frame_state[self.remaining_quantity[i][1]] = 1
                        self.remaining_quantity = self.synthesis()

    def synthesis(self):
        number = []
        if self.__synthesis[-1]:
            self.__synthesis[-1] = 0
            self.__frame_state[-1] = 1
        for i in range(9):
            if self.__synthesis[i]:
                number.append(i)
        if not number:
            return 0
        temp = []
        obj = 0
        for g in game_master.synthesis.SYNTHESIS_LIST:
            l = len(g) - 1
            if len(number) == l:
                state = 1
                if l == 1:
                    if g[0][0] != self.__synthesis[number[0]].name or g[0][1] > self.__synthesis[number[0]].number:
                        state = 0
                else:
                    if g[0][-1] == -1:
                        d = number[0] - g[0][-1]
                        for i in range(l):
                            if d != number[i] - g[i][-1] or self.__synthesis[number[i]].name != g[i][0] or \
                                    self.__synthesis[number[i]].number < g[i][1]:
                                state = 0
                                break
                    else:
                        for i in range(l):
                            if number[i] != g[i][2] or self.__synthesis[number[i]].name != g[i][0] or \
                                    self.__synthesis[number[i]].number < g[i][1]:
                                state = 0
                                break
                if state:
                    t = []
                    for i in range(l):
                        temp.append([g[i][1], number[i]])
                        t.append(self.__synthesis[number[i]].number // g[i][1])
                    ans = min(t)
                    temp.append(g[-1][-1])
                    temp.append(ans)
                    obj = g
                    break
        if obj:
            self.__synthesis[-1] = items.className.GOODS[obj[-1][0]](number=obj[-1][-1])
            self.__frame_state[-1] = 1
            return temp
        return 0

    def update(self):
        self.bag.update(None, 0.001)
        temp = []
        for i in range(10):
            if self.__frame_state[i]:
                self.__frame[i].fill(self.bag.fg)
                if self.__synthesis[i]:
                    self.__frame[i].blit(self.__synthesis[i].surface)
                    if self.__synthesis[i].number > 1:
                        font = game_master.game.Game.FONT.render(str(self.__synthesis[i].number), True,
                                                                 (255, 255, 255)).convert_alpha()
                        rect = font.get_rect(bottomright=(40, 40))
                        self.__frame[i].blit(font, rect)
                self.__frame_state[i] = 0
                temp.append(i)
        self.setup(temp)

    def render(self):
        if self.state:
            pygame.display.get_surface().blit(self.__background, self.bag.rect)
            self.bag.render_selection()
