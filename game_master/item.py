import pygame
import settings


class Item:
    def __init__(self):
        self.__bgp = [1]
        self.__text_box = []
        self.__button = []
        self.__input = []

    def load(self):
        pass

    def render(self):
        if self.__bgp[0] != 1:
            for i in range(2, self.__bgp[0]):
                self.__bgp[1].bilt(self.__bgp[i][0], self.__bgp[i][1])
            for t in self.__text_box:
                t = t.render()
                self.__bgp[1].bilt(t[0], t[1])
            for b in self.__button:
                b = b.render()
                self.__bgp[1].bilt(b[0], b[1])
            for i in self.__input:
                self.__bgp[1].bilt(i.box, i.rect)
        else:
            self.__bgp.append(pygame.Surface(settings.WIDTH, settings.HEIGHT))
            self.__bgp[0] += 1
            for t in self.__text_box:
                t = t.render()
                self.__bgp[1].bilt(t[0], t[1])
            for b in self.__button:
                b = b.render()
                self.__bgp[1].bilt(b[0], b[1])
            for i in self.__input:
                self.__bgp[1].bilt(i.box, i.rect)
        return self.__bgp[1]