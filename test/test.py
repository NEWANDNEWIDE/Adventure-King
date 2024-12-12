import sys
import pygame
import pytmx
from pytmx import TiledMap

pygame.init()
screen = pygame.display.set_mode((1200, 900))
clock = pygame.time.Clock()


class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.__display = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()

        self.h_w = self.__display.width // 2
        self.h_h = self.__display.height // 2

        self.ground_rect = self.__display.get_rect(topleft=(0, 0))

        self.tmx: TiledMap = pytmx.util_pygame.load_pygame(r"C:\Users\10962\Desktop\First_map\first_map.tmx")
        self.surface = pygame.Surface((2000, 1500))

    def draw_tmx(self):
        for layer in self.tmx.visible_layers:
            for x, y, gid in layer:
                tile = self.tmx.get_tile_image_by_gid(gid)
                if tile:
                    self.surface.blit(tile, (x * self.tmx.tilewidth, y * self.tmx.tileheight))

    def center_target_camera(self, target):
        self.offset.x = target[0] - self.h_w
        self.offset.y = target[1] - self.h_h

    def custom_draw(self, rect):
        self.center_target_camera(rect)

        ground_offset = self.ground_rect.topleft - self.offset
        self.__display.blit(self.surface, ground_offset)

        # active elements
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.__display.blit(sprite.image, offset_pos)


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
