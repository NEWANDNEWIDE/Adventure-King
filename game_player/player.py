import random
from typing import List

import pygame
import game_master.fileManager
import game_master.gameObject


class CameraGroup(pygame.sprite.Group):
    def __init__(self, surface: pygame.Surface):
        super().__init__()
        self.__display = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()
        self.__surface = surface

        self.h_w = self.__display.width // 2
        self.h_h = self.__display.height // 2

        self.ground_rect = self.__surface.get_rect(topleft = (0,0))

    def center_target_camera(self, target):
        self.offset.x = target[0] - self.h_w
        self.offset.y = target[1] - self.h_h

    def custom_draw(self, rect):

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
        self.__surface = pygame.image.load(r"C:\Users\10962\Desktop\Pygame-Cameras-main\graphics\player.png").convert_alpha()
        # self.__l = (self.__surface[0] - 1) // 4
        self.__vec2 = [0, 0]

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
        self.attribute.move_speed = 100

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
            damage = self.attribute.attack + self.bag.bag[self.bag.selection_box].attack
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
        self.attribute.rect[0] += self.vec2[0] * self.attribute.move_speed * dt
        self.attribute.rect[1] += self.vec2[1] * self.attribute.move_speed * dt
        self.rect.centerx = self.attribute.rect[0]
        self.rect.centery = self.attribute.rect[1]

    def update(self, dt):
        self.move(dt)
        self.bag.update()

class Bag:
    def __init__(self):
        self.__state = 0
        self.__inventory = pygame.Surface((422, 44))
        self.__inventory_rect = ((1200 - 422) / 2, 900 - 64)
        self.__rect = ((1200 - 458) / 2, (900 - 410) / 2)
        self.__background = pygame.Surface((458, 410))
        self.__role_box = pygame.Surface((100, 166))
        self.__frame = [pygame.Surface((40, 40)) for _ in range(49)]
        self.__frame_state = [0 for _ in range(49)]
        self.__synthesis = [0 for _ in range(4)]
        self.__arrowhead = pygame.Surface((40, 40))  # game_master.fileManager.game_surface["arrowhead"]
        self.__arrowhead.fill((0, 0, 0))
        self.__box = pygame.Surface((44, 44))
        self.__offset = 2
        self.__offset_rect = 20
        self.__bg = (196, 196, 196)
        self.__fg = (138, 138, 138)
        self.__bag = [0 for _ in range(49)]
        self.__free = 40
        self.__selection_box = 34
        self.__selection_offset = [0, 0]
        self.__selection = 0
        self.__selection_index = -1
        for i in range(49):
            self.__frame[i].fill(self.__fg)
        self.__role_box.fill((0, 0, 0))
        self.__inventory.fill(self.__bg)
        self.__box.fill((0, 0, 0))
        self.setup()

    @property
    def state(self):
        return self.__state

    @property
    def bag(self):
        return self.__bag

    @property
    def selection_box(self):
        return self.__selection_box

    @selection_box.setter
    def selection_box(self, sb):
        self.__selection_box = sb

    @property
    def inventory_rect(self):
        return self.__inventory_rect

    def setup(self):
        self.__background.fill(self.__bg)
        self.__inventory.blit(self.__box, (42 * (self.__selection_box - 34), 0))
        for i in range(4):
            self.__background.blit(self.__frame[i], (self.__offset_rect, self.__offset_rect + (self.__offset + 40) * i))
            self.__background.blit(self.__frame[44 + i], (272 + (self.__offset + 40) * (i % 2),
                                                          self.__offset_rect + self.__offset + 40 + (
                                                                      self.__offset + 40) * (i // 2)))
        self.__background.blit(self.__role_box, (self.__offset_rect * 2 + 40, self.__offset_rect))
        self.__background.blit(self.__arrowhead, (356, 83))
        self.__background.blit(self.__frame[-1], (398, 83))
        for i in range(30):
            self.__background.blit(self.__frame[4 + i],
                                   (20 + (self.__offset + 40) * (i % 10), 206 + (self.__offset + 40) * (i // 10)))
        for i in range(10):
            self.__background.blit(self.__frame[34 + i], (20 + (self.__offset + 40) * i, 350))
            self.__inventory.blit(self.__frame[34 + i], (2 + (self.__offset + 40) * i, 2))

    def open(self):
        self.__state = 1

    def close(self):
        self.__state = 0
        if self.__selection_index != -1:
            t = self.__bag[self.__selection_index]
            n = t.number + self.__selection.number
            if t.name == self.__selection.name and t.limit >= n:
                t.number = n
                self.__selection = 0
                self.__selection_index = -1
                self.__selection_offset = [0, 0]
            else:
                t = self.__selection
                self.__selection = 0
                self.__selection_index = -1
                self.__selection_offset = [0, 0]
                if not self.put(t):
                    return self.out(obj=t)
        for i in range(4):
            if self.__synthesis[i]:
                t = self.__bag[self.__synthesis[i]]
                n = t.number + self.__bag[44 + i].number
                if t.name == self.__bag[44 + i] and t.limit >= n:
                    t.number = n
                    self.__bag[44 + i] = 0
                    self.__synthesis[i] = 0
                else:
                    t, n = self.__bag[44 + i], self.__synthesis[i]
                    self.__bag[44 + i] = 0
                    self.__synthesis[i] = 0
                    if not self.put(t):
                        self.out(n)

    def use(self):
        if self.__bag[self.__selection_box]:
            self.__bag[self.__selection_box].use()

    def selected(self, pos: List[int]):
        pos = list(pos)
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
            if self.__selection_index == -1:
                if self.__bag[i]:
                    self.__selection_offset = [pos[0] - 20, pos[1] + 40]
                    self.__selection_index = i
                    self.__selection = self.__bag[i]
                    self.__bag[i] = 0
                    self.__frame_state[i] = 1
            else:
                if self.__bag[i]:
                    self.__selection_index = i
                    t = self.__selection
                    self.__selection = self.__bag[i]
                    self.__bag[i] = t
                else:
                    self.__bag[i] = self.__selection
                    self.__selection_offset = [0, 0]
                    self.__selection_index = -1
                    self.__selection = 0
                self.__frame_state[i] = 1
        elif 272 <= pos[0] <= 356 and 62 <= pos[1] <= 144:
            pos[0] -= 272
            pos[1] -= 62
            i, j = 0, 0
            for i in range(2):
                pos[1] -= 40
                if pos[1] <= 0:
                    break
                elif 0 < pos[1] < 2:
                    return
                pos[1] -= 2
                if pos[0] > 0:
                    for j in range(2):
                        pos[0] -= 40
                        if pos[0] <= 0:
                            break
                        elif 0 < pos[0] < 2:
                            return
                        pos[0] -= 2
            i = 44 + i * 2 + j
            if self.__selection_index == -1:
                if self.__bag[i]:
                    self.__selection_offset = [pos[0] + 40, pos[1] + 40]
                    self.__selection_index = i
                    self.__selection = self.__bag[i]
                    self.__bag[i] = 0
                    self.__frame_state[i] = 1
            else:
                if self.__bag[i]:
                    self.__selection_index = i
                    t = self.__selection
                    self.__selection = self.__bag[i]
                    self.__bag[i] = t
                else:
                    self.__bag[i] = self.__selection
                    self.__selection_offset = [0, 0]
                    self.__selection_index = -1
                    self.__selection = 0
                self.__frame_state[i] = 1
        elif 398 <= pos[0] <= 438 and 83 <= pos[1] <= 123:
            if self.__selection_index == -1 and self.__bag[48]:
                self.__selection_offset = [pos[0] - 398, pos[1] - 83]
                self.__selection_index = 48
                self.__selection = self.__bag[48]
                self.__bag[48] = 0
                self.__frame_state[48] = 1
        elif 20 <= pos[0] <= 438:
            pos[0] -= 20
            if 206 <= pos[1] <= 330:
                pos[1] -= 206
                i, j = 0, 0
                for i in range(3):
                    pos[1] -= 40
                    if pos[1] <= 0:
                        break
                    elif 0 < pos[1] < 2:
                        return
                    pos[1] -= 2
                    if pos[0] > 0:
                        for j in range(10):
                            pos[0] -= 40
                            if pos[0] <= 0:
                                break
                            elif 0 < pos[0] < 2:
                                return
                            pos[0] -= 2
                i = 4 + i * 10 + j
                if self.__selection_index == -1:
                    if self.__bag[i]:
                        self.__selection_offset = [pos[0] + 40, pos[1] + 40]
                        self.__selection_index = i
                        self.__selection = self.__bag[i]
                        self.__bag[i] = 0
                        self.__frame_state[i] = 1
                else:
                    if self.__bag[i]:
                        self.__selection_index = i
                        t = self.__selection
                        self.__selection = self.__bag[i]
                        self.__bag[i] = t
                    else:
                        self.__bag[i] = self.__selection
                        self.__selection_offset = [0, 0]
                        self.__selection_index = -1
                        self.__selection = 0
                    self.__frame_state[i] = 1
            elif 350 <= pos[1] <= 390:
                i = 0
                for i in range(10):
                    pos[0] -= 40
                    if pos[0] <= 0:
                        break
                    elif 0 < pos[0] < 2:
                        return
                    pos[0] -= 2
                i = 34 + i
                if self.__selection_index == -1:
                    if self.__bag[i]:
                        self.__selection_offset = [pos[0] + 40, pos[1] - 350]
                        self.__selection_index = i
                        self.__selection = self.__bag[i]
                        self.__bag[i] = 0
                        self.__frame_state[i] = 1
                else:
                    if self.__bag[i]:
                        self.__selection_index = i
                        t = self.__selection
                        self.__selection = self.__bag[i]
                        self.__bag[i] = t
                    else:
                        self.__bag[i] = self.__selection
                        self.__selection_offset = [0, 0]
                        self.__selection_index = -1
                        self.__selection = 0
                    self.__frame_state[i] = 1

    def put(self, obj):
        if self.__free:
            for i in range(40):
                if not self.__bag[4 + i]:
                    self.__bag[4 + i] = obj
                    self.__frame_state[4 + i] = 1
                    self.__free -= 1
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

    def update_inventory(self):
        if self.selection_box < 34:
            self.selection_box = 34
        elif self.selection_box > 43:
            self.selection_box = 43
        self.__inventory.fill(self.__bg)
        self.__inventory.blit(self.__box, (42 * (self.__selection_box - 34), 0))
        for i in range(10):
            self.__inventory.blit(self.__frame[34 + i], (2 + (self.__offset + 40) * i, 2))

    def update(self):
        for i in range(49):
            if self.__frame_state[i]:
                self.__frame[i].fill(self.__fg)
                if self.__bag[i]:
                    self.__frame[i].blit(self.__bag[i].surface)
                self.__frame_state[i] = 0
        # self.setup()

    def render_inventory(self):
        pygame.display.get_surface().blit(self.__inventory, self.__inventory_rect)

    def render(self):
        if self.__state:
            pygame.display.get_surface().blit(self.__background, self.__rect)
            if self.__selection_index != -1:
                pos = pygame.mouse.get_pos()
                pygame.display.get_surface().blit(self.__selection.surface, (
                pos[0] - self.__selection_offset[0], pos[1] - self.__selection_offset[1]))
