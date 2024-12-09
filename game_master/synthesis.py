import pygame


SYNTHESIS = 114514


class Synthesis:
    def __init__(self, bag):
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
                        107 + (self.bag.offset + 40) * (i % 2), self.bag.offset_rect + (self.bag.offset + 40) * (i // 2)))
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
                    self.bag.frame_state[self.__synthesis[i]] = 1
                    self.__frame_state[i] = 1
                    self.bag.bag[self.__synthesis_index[i]] = self.__synthesis[i]
                    self.__synthesis[i] = 0
        return 0

    def selected(self, pos, state):
        self.bag.selected(pos, SYNTHESIS)
        if 272 <= pos[0] <= 356 and 62 <= pos[1] <= 144:
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
                    self.selection_index = i
                    self.selection = self.__bag[i]
                    self.__synthesis[k * 2 + j] = 0
                    self.__bag[i] = 0
                    self.__frame_state[i] = 1
                    self.__frame_state[-1] = 1
            else:
                self.__synthesis[k * 2 + j] = self.selection_index
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
                self.__frame_state[-1] = 1

    def update(self):
        self.bag.update()
        temp = []
        for i in range(10):
            if self.__synthesis_index[i]:
                self.__frame[i].fill(self.bag.fg)
                if self.__synthesis[i]:
                    self.__frame[i].blit(self.__synthesis[i - 49].surface)
                self.__synthesis_index[i] = 0
                temp.append(i)
        self.setup(temp)

    def render(self):
        if self.state:
            pygame.display.get_surface().blit(self.__background, self.bag.rect)
            if self.bag.selection_index != -1:
                pos = pygame.mouse.get_pos()
                pygame.display.get_surface().blit(self.bag.selection.surface, (
                    pos[0] - self.bag.selection_index[0], pos[1] - self.bag.selection_index[1]))
