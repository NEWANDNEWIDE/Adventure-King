import os


def addition(a, b, *args):
    t = 0
    for i in args:
        t += i
    return t


def func(*args):
    return addition(*args)

print(addition(1, 2, 3))
print(func(1, 2, 3))
