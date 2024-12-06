import control.button


class Scene:
    def __init__(self, item=None):
        self.__item = []
        if item:
            if issubclass(item, list):
                self.__item = item
            else:
                self.__item.append(item)

    def add(self, item):
        if isinstance(item, list):
            self.__item += item
        else:
            self.__item.append(item)

    def delete(self, index):
        del self.__item[index]

    def delete_name(self, name):
        for i in range(len(self.__item)):
            if self.__item[i].name == name:
                del self.__item[i]
                break

    def action(self, pos, screen):
        for i in self.__item:
            if isinstance(i, control.button.Button) | isinstance(i, control.button.ButtonList):
                i.activate(pos, screen)

    def render(self, screen, area=None, surf_list=None):
        x, y = 0, 0
        if not surf_list:
            for i in self.__item:
                t = i.render()
                screen.blit(t[0], (t[1][0] + x, t[1][1] + y))
                if area == "V":
                    y = 2
                    screen.fill((0, 0, 0), (t[1][0], t[1][1] + t[0].height, t[0].width, y))
                elif area == "L":
                    x = 2
                    screen.fill((0, 0, 0), (t[1][0] + t[0].width, t[1][1], x, t[0].height))
                if len(t) == 3:
                    if len(t[2]) >= 2:
                        self.render(screen, area, t[2])
        else:
            if len(surf_list) >= 2:
                screen.blit(surf_list[0], surf_list[1])
                if area == "V":
                    y = 2
                    screen.fill((0, 0, 0), (surf_list[1][0], surf_list[1][1] + surf_list[0].height, surf_list[0].width, y))
                elif area == "L":
                    x = 2
                    screen.fill((0, 0, 0), (surf_list[1][0] + surf_list[0].width, surf_list[1][1], x, surf_list[0].height))
                if len(surf_list) == 3:
                    if surf_list[2] >= 2:
                        self.render(screen, area, surf_list[2])