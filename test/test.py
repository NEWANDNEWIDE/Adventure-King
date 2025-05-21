import sys
import pygame
from pytmx import TiledMap

pygame.init()
screen = pygame.display.set_mode((1200, 900))
clock = pygame.time.Clock()


class CameraGroup(pygame.sprite.Group):
    def __init__(self, surface, tmx: TiledMap, *groups):
        super().__init__()
        self.__display = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()
        self.__surface = surface
        self.__tmx_group = [[], []]
        self.player_index = [0, -1]
        self.obj = self.sprites()

        self.h_w = settings.WIDTH // 2
        self.h_h = settings.HEIGHT // 2

        self.ground_rect = self.__surface.get_rect(topleft=(0, 0))

        self.tmx: TiledMap = tmx

        self.setup(*groups)

    def setup(self, *groups):
        if self.tmx:
            i = 0
            temp = []
            for layer in ["ground", "middle", "no_collision", "collision"]:
                    for x, y, surf in self.tmx.get_layer_by_name(layer).tiles():
                        if surf:
                            if i <= 1:
                                self.__surface.blit(surf, (self.tmx.tilewidth * x, self.tmx.tileheight * y))
                                temp.append(MapSprite((self.tmx.tilewidth * x, self.tmx.tileheight * y), surf, 1))
                            elif i == 2:
                                temp.append(MapSprite((self.tmx.tilewidth * x, self.tmx.tileheight * y), surf, 2))
                            else:
                                temp.append(MapSprite((self.tmx.tilewidth * x, self.tmx.tileheight * y), surf, 2, *groups))
                    i += 1
            temp.sort(key=lambda r: r.layer_g)
            m = sort_2(temp, 2)
            t1 = temp[:m]
            t2 = temp[m:]
            self.__tmx_group = [t1, t2]

    def center_target_camera(self, target):
        self.offset.x = target.centerx - self.h_w
        self.offset.y = target.centery - self.h_h

    def custom_draw(self, rect_other, dt):

        self.center_target_camera(rect_other)

        ground_offset = self.ground_rect.topleft - self.offset
        self.__display.blit(self.__surface, ground_offset)

        # active elements
        i = 0
        t = self.obj[self.player_index[0]]
        for sprite in self.__tmx_group[1]:
            if -620 <= rect_other.centerx - sprite.rect.centerx <= 620 and -470 <= rect_other.centery - sprite.rect.centery <= 470:
                if self.player_index[0] + i <= self.player_index[1]:
                    if sprite.rect.bottom > t.rect.bottom:
                        offset_pos = t.rect.center - self.offset
                        rect = t.image.get_rect(center=offset_pos)
                        self.__display.blit(t.image, rect)
                        if t.damage_a >= 0:
                            t.damage_t -= dt
                            font = game_master.game.Game.FONT.render(f"-{t.damage_a}" if t.damage_a else "0", True, (0, 0, 0))
                            rect_font = font.get_rect(center=rect.center)
                            rect_font.bottom = rect.top
                            self.__display.blit(font, rect_font)
                            if t.damage_t <= 0:
                                t.damage_a = -1
                                t.damage_t = 1
                        i += 1
                        if self.player_index[0] + i <= self.player_index[1]:
                            t = self.obj[self.player_index[0] + i]
                            while self.player_index[0] + i <= self.player_index[1] and (-620 > rect_other.centerx - t.rect.centerx or rect_other.centerx - t.rect.centerx > 620):
                                i += 1
                                if self.player_index[0] + i <= self.player_index[1]:
                                    t = self.obj[self.player_index[0] + i]
                        offset_pos = sprite.rect.center - self.offset
                        rect = sprite.image.get_rect(center=offset_pos)
                        self.__display.blit(sprite.image, rect)
                    else:
                        offset_pos = sprite.rect.center - self.offset
                        rect = sprite.image.get_rect(center=offset_pos)
                        self.__display.blit(sprite.image, rect)
                else:
                    offset_pos = sprite.rect.center - self.offset
                    rect = sprite.image.get_rect(center=offset_pos)
                    self.__display.blit(sprite.image, rect)
        while self.player_index[0] + i <= self.player_index[1]:
            offset_pos = t.rect.center - self.offset
            rect = t.image.get_rect(center=offset_pos)
            self.__display.blit(t.image, rect)
            if t.damage_a >= 0:
                t.damage_t -= dt
                font = game_master.game.Game.FONT.render(f"-{t.damage_a}" if t.damage_a else "0", True, (0, 0, 0))
                rect_font = font.get_rect(center=rect.center)
                rect_font.bottom = rect.top
                self.__display.blit(font, rect_font)
                if t.damage_t <= 0:
                    t.damage_a = -1
                    t.damage_t = 1
            i += 1
            if self.player_index[0] + i <= self.player_index[1]:
                t = self.obj[self.player_index[0] + i]

    def update(self, bottom):
        self.obj = self.sprites()
        self.obj.sort(key=lambda sprite: sprite.rect.bottom)
        self.player_index[0] = sort_1(self.obj, bottom - 470)
        self.player_index[1] = self.player_index[0] + sort_1(self.obj[self.player_index[0]:], bottom + 470)


class Player(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.surface = pygame.image.load(
            r"C:\Users\10962\Desktop\Pygame-Cameras-main\graphics\player.png").convert_alpha()
        self.surface = pygame.transform.scale(self.surface, (40, 40))
        self.image = self.surface
        self.pos = [640, 360]
        self.vec2 = [0, 0]
        self.speed = 100
        self.rect = self.surface.get_rect(center=self.pos)

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            self.vec2[0] = 1
        elif keys[pygame.K_a]:
            self.vec2[0] = -1
        else:
            self.vec2[0] = 0
        if keys[pygame.K_s]:
            self.vec2[1] = 1
        elif keys[pygame.K_w]:
            self.vec2[1] = -1
        else:
            self.vec2[1] = 0

    def move(self, dt):
        self.pos[0] += self.vec2[0] * dt * self.speed
        self.pos[1] += self.vec2[1] * dt * self.speed
        self.rect.centerx = self.pos[0]
        self.rect.centery = self.pos[1]

    def update(self, dt):
        self.input()
        self.move(dt)


camera = CameraGroup()
player = Player(camera)


while True:
    screen.fill((255, 255, 255))
    dt = clock.tick() / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    player.update(dt)
    camera.custom_draw(player.pos)

    pygame.display.update()
