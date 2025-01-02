import sys

import pygame.image

import control.inputField
import game_master.game
import settings


class Level:
    def __init__(self):
        self.display = pygame.display.get_surface()

        self.alpha = 255
        self.time = 5
        self.start_time = 0

        self.font = pygame.font.Font(settings.FONT, 50)
        self.png = pygame.image.load("res/ground.png").convert_alpha()
        self.theme = self.font.render("冒险王", True, (0, 0, 0)).convert_alpha()
        self.start_frame = pygame.Surface((100, 50))
        self.end_frame = self.start_frame.copy()
        self.start_frame_rect = self.start_frame.get_rect(center=(settings.WIDTH // 2, settings.HEIGHT // 2))
        self.end_frame_rect = self.end_frame.get_rect(center=(settings.WIDTH // 2, settings.HEIGHT // 2 + 120))
        self.start = game_master.game.Game.FONT.render("开始游戏", True, (0, 0, 0)).convert_alpha()
        self.end = game_master.game.Game.FONT.render("退出游戏", True, (0, 0, 0)).convert_alpha()
        self.theme_rect = self.theme.get_rect(center=(settings.WIDTH // 2, settings.HEIGHT // 2 - 300))
        self.start_rect = self.start.get_rect(center=(settings.WIDTH // 2, settings.HEIGHT // 2))
        self.end_rect = self.end.get_rect(center=(settings.WIDTH // 2, settings.HEIGHT // 2 + 120))

    def action(self, pos):
        if -self.start_frame.width // 2 < pos[0] - settings.WIDTH // 2 < self.start_frame.width // 2 and -self.start_frame.height // 2 < pos[1] - settings.HEIGHT // 2 < self.start_frame.height // 2:
            self.start_time = pygame.time.get_ticks()
            return 1
        elif -self.end_frame.width // 2 < pos[0] - settings.WIDTH // 2 < self.end_frame.width // 2 and -self.end_frame.height // 2 < pos[1] - settings.HEIGHT // 2 - 120 < self.end_frame.height // 2:
            pygame.quit()
            sys.exit()
        return 0

    def guodu(self, clock):
        self.start_time = pygame.time.get_ticks()
        while self.alpha:
            self.display.fill((255, 255, 255))
            self.png.set_alpha(self.alpha)
            self.display.blit(self.png)
            clock.tick()
            pygame.display.update()
            if pygame.time.get_ticks() - self.start_time >= self.time:
                self.alpha -= 1
                self.start_time = pygame.time.get_ticks()
        text = control.inputField.InputField((500, 430), (200, 40), "请输入名字", (196, 196, 196), (0, 0, 0), (138, 138, 138), "name")
        font = pygame.font.Font(settings.FONT, 20)
        help_text = "操作说明:\na:向左走\nd:向右走\nw:向上走\ns:向下走\n空格:闪避\nb:打开/关闭背包\nesc:暂停菜单"
        help_text = font.render(help_text, True, (0, 0, 0))
        while True:
            clock.tick()
            event = None
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            name = text.action(pygame.mouse.get_pos(), event)
            if isinstance(name, str):
                self.png.set_alpha(255)
                self.alpha = 255
                return name
            else:
                self.display.blit(name, text.rect)
            self.display.blit(help_text, (1, 1))
            pygame.display.update()

    def render(self):
        self.start_frame.fill((255, 255, 255))
        self.end_frame.fill((255, 255, 255))
        self.display.blit(self.png)
        self.display.blit(self.theme, self.theme_rect)
        self.display.blit(self.start_frame, self.start_frame_rect)
        self.display.blit(self.end_frame, self.end_frame_rect)
        self.display.blit(self.start, self.start_rect)
        self.display.blit(self.end, self.end_rect)
