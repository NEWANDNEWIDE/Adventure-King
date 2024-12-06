import pygame.event
import game_master
import player


class Map:
    def __init__(self, screen):
        self.__surface = game_master.fileManager.game_surface["map"]
        self.__item = game_master.item.Item()
        self.__state = 0
        self.__screen = screen
        self.camera = player.player.CameraGroup()
        self.player = player.player.Player((640, 360), self.camera)
        self.object_rect = []
        self.losing = []
        self.losing_time = []

        self.object_rect.append(self.player.attribute.rect)

    def create(self, obj):
        self.camera.add(obj)
        self.object_rect.append(obj.attribute.rect)

    def add(self, obj):
        self.camera.add(obj)
        self.object_rect.append(obj.rect)

    def setup(self):
        pass

    def event_update(self, event: pygame.event.Event):
        if self.__state:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    self.player.vec2[0] = -1
                elif event.key == pygame.K_d:
                    self.player.vec2[0] = 1
                elif event.key == pygame.K_w:
                    self.player.vec2[1] = -1
                elif event.key == pygame.K_s:
                    self.player.vec2[1] = 1
                elif event.key == pygame.K_b:
                    if not self.player.bag.state:
                        self.player.bag.open()
                    else:
                        self.player.bag.close()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    self.player.attack()
                elif event.button == pygame.BUTTON_RIGHT:
                    self.player.use()
            elif event.type == pygame.MOUSEWHEEL:
                if event.button == 4:
                    self.player.bag.selection_box += 1
                else:
                    self.player.bag.selection_box -= 1

    def update(self, dt):
        self.camera.update(dt)

    def render(self):
        pass