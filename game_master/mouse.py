import pygame
import main


def mouse_listening():
    state = main.g.running
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
        state = main.g.running
        pygame.time.delay(1000 // main.g.game_speed)