import pygame
import game_master.goods
import game_player.player

SYNTHESIS = 114514
# 人物身上的合成
# 类名可在className.GOODS里加入或查看
PLAYER_SYNTHESIS_LIST = [
    # 五个格子, 前四个以(类名, 数量)写入, 最后一个为输出
    ((game_master.goods.TestItem.NAME, 1), (game_master.goods.TestItemOther.NAME, 1))
]


class Synthesis:
    def __init__(self, bag: game_player.player.Bag):
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
        self.__synthesis_index = [0 for _ in range(10)]
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
                        107 + (self.bag.offset + 40) * (i % 3), self.bag.offset_rect + (self.bag.offset + 40) * (i // 3)))
            self.__background.blit(self.__frame[-1], (311, 62))

    def open(self):
        self.state = 1
        return self

    def close(self):
        self.state = 0
        self.bag.close()
        for i in range(10):
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
        self.bag.selected(pos, SYNTHESIS)
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
                    if pos[0] > 0:
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
            print(pos)
            if self.bag.selection_index == -1:
                if self.__synthesis_index[i]:
                    self.bag.selection_offset = [pos[0] + 40, pos[1] + 40]
                    self.bag.selection_index = self.__synthesis_index[i]
                    self.bag.selection = self.__synthesis[i]
                    self.__synthesis_index[i] = 0
                    self.__synthesis[i] = 0
                    self.__frame_state[i] = 1
                    self.__frame_state[-1] = 1
            else:
                if self.__synthesis_index[i]:
                    n = self.__synthesis_index[i]
                    self.__synthesis_index[i] = self.bag.selection_index
                    self.bag.selection_index = n
                    t = self.bag.selection
                    self.bag.selection = self.__synthesis[i]
                    self.__synthesis[i] = t
                else:
                    self.__synthesis_index[i] = self.bag.selection_index
                    self.__synthesis[i] = self.bag.selection
                    self.bag.selection_offset = [0, 0]
                    self.bag.selection_index = -1
                    self.bag.selection = 0
                self.__frame_state[i] = 1
                self.__frame_state[-1] = 1
        elif 251 <= pos[0] <= 291 and 62 <= pos[1] <= 102:
            if self.bag.selection_index == -1 and self.__synthesis[-1]:
                self.bag.selection_offset = [pos[0] - 398, pos[1] - 83]
                self.bag.selection_index = 48
                self.bag.selection = self.__synthesis[-1]
                self.__synthesis[-1] = 0
                self.__frame_state[-1] = 1

    def update(self):
        self.bag.update()
        temp = []
        for i in range(10):
            if self.__frame_state[i]:
                self.__frame[i].fill(self.bag.fg)
                if self.__synthesis[i]:
                    self.__frame[i].blit(self.__synthesis[i].surface)
                self.__frame_state[i] = 0
                temp.append(i)
        self.setup(temp)

    def render(self):
        if self.state:
            pygame.display.get_surface().blit(self.__background, self.bag.rect)
            if self.bag.selection_index != -1:
                pos = pygame.mouse.get_pos()
                pygame.display.get_surface().blit(self.bag.selection.surface, (
                    pos[0] - self.bag.selection_offset[0], pos[1] - self.bag.selection_offset[1]))
