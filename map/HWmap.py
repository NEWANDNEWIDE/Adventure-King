import pygame.event
import pytmx.util_pygame
import game_master
import game_player.player
import items


class Map:
    """这个类是用来交作业的"""
    def __init__(self, screen):
        self.tmx = pytmx.util_pygame.load_pygame(r"C:\Users\10962\Desktop\First_map\first_map.tmx")
        self.__surface = pygame.image.load(
            r"D:\PyDew-Valley-main\s23 - Audio & fixes\demo\graphics\world\ground.png").convert_alpha()
        self.__item = game_master.item.Item()
        self.__state = 1
        self.__screen = screen

        self.camera = game_player.player.CameraGroup(self.__surface)
        self.player = game_player.player.Player([600, 450], self.camera)

        self.inventory_rect = self.player.bag.inventory_rect

        self.object = []
        self.goods = []

        self.losing = []
        self.losing_time = []

        self.object.append(self.player)

        self.setup()

        self.player.bag.put(items.goods.TestItem(number=64))
        self.player.bag.put(items.goods.TestItemOther(number=61))
        self.goods.append(game_master.synthesis.Synthesis(self.player.bag))
        self.object.append(game_master.gameObject.GameNpc([800, 600], self.camera))

    def create(self, obj):
        self.camera.add(obj)
        self.object.append(obj)

    def add(self, obj):
        self.camera.add(obj)
        self.losing.append(obj)

    def create_goods(self):
        pass

    @staticmethod
    def get_rect_x(obj):
        return obj.attribute.rect[0]

    @staticmethod
    def get_rect_y(obj):
        return obj.attribute.rect[1]

    def sort_losing(self):
        self.losing.sort(key=Map.get_rect_x)

    def sort_object(self):
        self.object.sort(key=Map.get_rect_y)

    def setup(self):
        game_master.synthesis.PLAYER_SYNTHESIS_LIST = game_master.synthesis.process(
            game_master.synthesis.PLAYER_SYNTHESIS_LIST_NOT_PROCESSED)
        game_master.synthesis.SYNTHESIS_LIST = game_master.synthesis.process(
            game_master.synthesis.SYNTHESIS_LIST_NOT_PROCESSED, 3)

    def event_update(self, event: pygame.event.Event):
        if self.__state:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    if self.player.bag.state:
                        self.player.bag.close()
                    elif not self.player.sys_state:
                        self.player.bag.open()
                elif 48 <= event.key <= 57:
                    if event.key == 48:
                        self.player.bag.selection_box = 43
                    elif self.player.bag.selection_box != event.key - 48:
                        self.player.bag.selection_box = event.key - 15
                    self.player.bag.update_inventory()
                elif event.key == pygame.K_e:
                    if not self.player.bag.state and not self.player.sys_state:
                        self.player.sys_state = self.goods[0].open()
                    elif self.player.sys_state:
                        self.player.sys_state = self.goods[0].close()
                elif event.key == 1073742049:
                    self.player.run = 0 if self.player.run else 1
                elif event.key == 32 and not self.player.shanbi_state and self.player.shanbi >= 0 and (
                        self.player.vec2[0] or self.player.vec2[1]):
                    self.player.shanbi_state = 1
                    self.player.shanbi = 0.1
                    self.player.dir = self.player.vec2.copy()
            elif event.type == pygame.KEYUP:
                pass
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                pos = list(pos)
                if self.inventory_rect[0] + 2 <= pos[0] <= self.inventory_rect[0] + 420 and self.inventory_rect[
                    1] + 2 <= pos[1] <= self.inventory_rect[1] + 42:
                    pos[0] -= self.inventory_rect[0] + 2
                    i = 0
                    for i in range(10):
                        pos[0] -= 40
                        if pos[0] <= 0:
                            break
                        elif 0 < pos[0] < 2:
                            i = -1
                            break
                        pos[0] -= 2
                    if i + 1 and self.player.bag.selection_box != 34 + i:
                        self.player.bag.selection_box = 34 + i
                        self.player.bag.update_inventory()
                        return
                if event.button == pygame.BUTTON_LEFT:
                    if self.player.bag.state:
                        self.player.bag.selected(pos, pygame.BUTTON_LEFT)
                    elif self.player.sys_state:
                        self.player.sys_state.selected(pos, pygame.BUTTON_LEFT)
                    else:
                        self.player.attack()
                elif event.button == pygame.BUTTON_RIGHT:
                    if self.player.bag.state:
                        self.player.bag.selected(pos, pygame.BUTTON_RIGHT)
                    elif self.player.sys_state:
                        self.player.sys_state.selected(pos, pygame.BUTTON_RIGHT)
                    else:
                        self.player.use()
                elif event.button == 4:
                    self.player.bag.selection_box += 1
                    self.player.bag.update_inventory()
                elif event.button == 5:
                    self.player.bag.selection_box -= 1
                    self.player.bag.update_inventory()

    def update(self, dt):
        for o in self.object:
            if o.attribute.name != "player":
                o.update(dt, self.player.rect)
            else:
                o.update(dt)

    def render_UI(self):
        self.player.bag.render_inventory()
        if self.player.bag.state:
            self.player.bag.render()
        elif self.player.sys_state:
            self.player.sys_state.render()

    def render(self):
        self.camera.custom_draw(self.player.attribute.rect)
        self.render_UI()
