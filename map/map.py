from random import seed
from map import block


class Map:
    def __init__(self, seeds):
        self.seeds = seeds
        seed(self.seeds)
        self.headBlock = block.Block()