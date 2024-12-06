import sys
import pygame


pygame.init()
screen = pygame.display.set_mode((1200, 900))
clock = pygame.time.Clock()
surface = pygame.image.load(r"C:\Users\10962\Desktop\Pygame-Cameras-main\graphics\ground.png")
rect = [0, 0]
state = 0
pos = [0, 0]

while True:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        print(event)
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_LEFT:
                state = 1
                pos = pygame.mouse.get_pos()
        elif event.type == pygame.MOUSEBUTTONUP:
            if state:
                t = pygame.mouse.get_pos()
                rect = [rect[0] + t[0] - pos[0], rect[1] + t[1] - pos[1]]
                state = 0

    if state:
        t = pygame.mouse.get_pos()
        screen.blit(surface, (rect[0] + t[0] - pos[0], rect[1] + t[1] - pos[1]))
    else:
        screen.blit(surface, rect)

    pygame.display.update()
    clock.tick()
