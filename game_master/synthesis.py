import pygame


class Synthesis:
    def __init__(self, bag):
        self.bag = bag
        # 合成界面是否打开
        self.state = 0
        # 合成界面的大小与背包一样
        self.__background = pygame.Surface((458, 410))
        # 存储合成
        self.__synthesis = [0 for _ in range(10)]
        # 存储索引
        self.__synthesis_index = [-1 for _ in range(10)]