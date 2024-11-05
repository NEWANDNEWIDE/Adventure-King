from random import seed
from block import *


class Map:
    def __init__(self, seeds):
        self.seeds = seeds
        seed(self.seeds)
        self.headBlock = Block()