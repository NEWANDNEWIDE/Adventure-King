import pygame
import settings
import game_master


def mouse_listening(g: game_master.game.Game):
    state = g.running
    while state:
        mouses = pygame.mouse.get_pressed()
        if mouses[pygame.BUTTON_LEFT]:
            pass
        if mouses[pygame.BUTTON_RIGHT]:
            pass
        if mouses[pygame.BUTTON_MIDDLE]:
            pass
        if mouses[pygame.BUTTON_WHEELUP]:
            pass
        if mouses[pygame.BUTTON_WHEELDOWN]:
            pass
        pygame.time.delay(1000 // settings.FPS)
        state = g.running