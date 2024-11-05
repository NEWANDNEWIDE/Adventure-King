from random import random


class Block:
    def __init__(self, var=None, up=None, down=None, right=None, left=None):
        self.var = var if not var else list()
        self.up = up
        self.down = down
        self.right = right
        self.left = left

    def generated_scores(self):
        return [int(random()*100+1) for _ in range(4)]

    def generated_grads(self):
        grads = []
        for _ in range(4):
            x, y = random(), random()
            a = pow(x**2 + y**2, 0.5)
            grads.append((x/a, y/a))
        return grads

    def lerp(self, x, y, w):
        return x*w + y*(1-w)

    def fade(self, x):
        return x*x*x*(x*(6*x-15)+10)

    def normalization(self, x, y):
        return (x/20 - x//20) / 20, (y/20 - y//20) / 20

    def grads_dot_mul(self, v1, v2, d=0):
        return v1[0]*v2[0] + v1[1]+v2[1] + d

    def mergePoints(self, x, y):
        count = self.var[x][y]
        for m in range(max(x - 3, 0), min(x + 4, 20)):
            for n in range(max(y - 3, 0), min(y + 4, 20)):
                count += self.var[m][n] if m != x or n != y else 0
        return count

    def generated_blocks(self):
        max_p = min_p = None

        for i in range(20):
            tmp = []
            for j in range(20):
                index = j
                scores = self.generated_scores()
                grads = self.generated_grads()
                i, j = self.normalization(i, j)
                tmp.append(self.lerp(self.lerp(self.grads_dot_mul(grads[0], (i, j), scores[0]), self.grads_dot_mul(grads[1], (i, j), scores[1]), self.fade(i)), self.lerp(self.grads_dot_mul(grads[2], (i, j), scores[2]), self.grads_dot_mul(grads[3], (i, j), scores[3]), self.fade(i)), self.fade(j)))
                if not min_p:
                    max_p = min_p = tmp[index]
                min_p = tmp[index] if tmp[index] < min_p else min_p
                max_p = tmp[index] if tmp[index] > max_p else max_p
            self.var.append(tmp)

        for i in range(20):
            for j in range(20):
                self.var[i][j] = 1 if (self.var[i][j] - min_p) / (max_p - min_p) > 0.85 or (self.var[i][j] - min_p) / (max_p - min_p) < 0.15 else 0
                self.var = 1 if self.mergePoints(i, j) > 15 else 0

"""
map = Map(20050507)
for x in range(3):
    for y in range(3):
        block = map.generated_blocks()
        for i in range(20):
            for j in range(20):
                block[i][j] = 1 if mergePoints(i, j, block) >= 15 else 0
                if block[i][j] == 1:
                    screen.blit(waterGround, (i*16 + x*320, j*16 + y*320))
                else:
                    screen.blit(greenGround, (i*16 + x*320, j*16 + y*320))
"""