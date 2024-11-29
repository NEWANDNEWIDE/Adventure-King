import os
import sys
import pygame
import control
import game_master.game

pygame.init()
screen = pygame.display.set_mode((1200, 900))
pygame.display.set_caption("UI制作")
clock = pygame.time.Clock()
running = True

def f(screen):
    print(1)

def h(screen):
    print(2)

f_l = []
h_l = []

f_l.append(control.button.Button((2, 2), (60, 60), (0, 0), "666", (123, 234, 222), (0, 0, 0), (0, 0, 0), "666", h))
f_l.append(control.button.Button((2, 2), (60, 60), (0, 0), "222", (123, 234, 222), (0, 0, 0), (0, 0, 0), "222", h))
f_l.append(control.button.ButtonList((80, 0), (80, 30), (2, 2), "帮助", (123, 234, 222), (0, 0, 0), (0, 0, 0), "h", h, b_list=h_l))
h_l.append(control.button.Button((2, 2), (60, 60), (0, 0), "666", (123, 234, 222), (0, 0, 0), (0, 0, 0), "666", h))
h_l.append(control.button.Button((2, 2), (60, 60), (0, 0), "222", (123, 234, 222), (0, 0, 0), (0, 0, 0), "222", h))

item = (0, 0, 1200, 30)
pos_line = (600, item[3], 2, 900)
file_item = (0, item[3], 600, item[3])
game = game_master.game.Game(True)
scene = control.scene.Scene()
scene.add(control.button.ButtonList((0, 0), (80, 30), (2, 2), "文件(F)", (123, 234, 222), (0, 0, 0), (0, 0, 0), "f", f, b_list=f_l))
scene.add(control.button.ButtonList((80, 0), (80, 30), (2, 2), "帮助(H)", (123, 234, 222), (0, 0, 0), (0, 0, 0), "h", h))


def init(screen):
    screen.fill((255, 255, 255))
    screen.fill((123, 234, 222), item)
    screen.fill((0, 0, 0), pos_line)
    screen.fill((100, 100, 100), file_item)



def run(dt, screen, event):
    screen.fill((255, 255, 255))
    screen.fill((123, 234, 222), item)
    screen.fill((0, 0, 0), pos_line)
    screen.fill((100, 100, 100), file_item)
    if event:
        if event.type == pygame.MOUSEBUTTONDOWN:
            scene.action(pygame.mouse.get_pos(), screen)
    scene.render(screen, "L")


init(screen)
while running:
    event = None
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    dt = clock.tick() / 1000
    run(dt, screen, event)
    pygame.display.update()
