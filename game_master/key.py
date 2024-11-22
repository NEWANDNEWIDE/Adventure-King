import pygame.event
import settings
import game_master


def keys_listening(g: game_master.game.Game):
    state = g.running
    while state:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            pass
        elif keys[pygame.K_s]:
            pass
        if keys[pygame.K_a]:
            pass
        elif keys[pygame.K_d]:
            pass
        if keys[pygame.K_e]:
            pass
        if keys[pygame.K_ESCAPE]:
            pass
        pygame.time.delay(1000 // settings.FPS)
        state = g.running