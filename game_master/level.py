import sys

import pygame.image
import game_master.game
import settings


class Level:
    def __init__(self):
        self.display = pygame.display.get_surface()

        self.alpha = 255
        self.time = 5
        self.start_time = 0

        self.font = pygame.font.SysFont('microsoftyaheiui', 50)
        self.png = pygame.image.load(r"C:\Users\10962\Desktop\Pygame-Cameras-main\graphics\ground.png").convert_alpha()
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

    def guodu(self):
        self.start_time = pygame.time.get_ticks()
        while self.alpha:
            self.display.fill((255, 255, 255))
            self.png.set_alpha(self.alpha)
            self.display.blit(self.png)
            pygame.display.update()
            if pygame.time.get_ticks() - self.start_time >= self.time:
                self.alpha -= 1
                self.start_time = pygame.time.get_ticks()
        self.png.set_alpha(255)

    def render(self):
        self.start_frame.fill((255, 255, 255))
        self.end_frame.fill((255, 255, 255))
        self.display.blit(self.png)
        self.display.blit(self.theme, self.theme_rect)
        self.display.blit(self.start_frame, self.start_frame_rect)
        self.display.blit(self.end_frame, self.end_frame_rect)
        self.display.blit(self.start, self.start_rect)
        self.display.blit(self.end, self.end_rect)
