import pygame.event
import main


def keys_listening():
    state = main.g.running
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
        pygame.time.delay(1000 // main.g.game_speed)
        state = main.g.running