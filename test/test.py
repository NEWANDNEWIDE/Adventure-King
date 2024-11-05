import pygame
from control.button import Button

pygame.init()

l = []


def f(func=None, *args):
    if func:
        func(*args)
        print(*args)

def function(a, b):
    print(a + b)

def c():
    print(666)

def load(func, *args):
    l.append((func, *args))
