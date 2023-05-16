import tiles
import numpy as np
from random import random
from noise import snoise2, _simplex

#generates random noise with a simplex noise algorithm imported from
#https://github.com/caseman/noise
def generateMap(height, width):
    randomX = random()
    randomY = random()
    factor = 1000
    arenaLayout = np.matrix([[chooseTile(snoise2(i + (randomX * factor), j + (randomY * factor))) for i in range(width)] for j in range(height)])
    return arenaLayout

#chooses a tile based on a given float value, impassable tiles should get a lower range to decrease
#the probability of them blocking the player in
def chooseTile(f):
    if f >= -1 and f < -0.5:
        return tiles.FireTile()
    elif f >= -0.5 and f < -0.2:
        return tiles.SandTile()
    elif f >= -0.2 and f < 0:
        return tiles.NormalTile()
    elif f >= 0 and f < 0.2:
        return tiles.WaterTile()
    elif f >= 0.2 and f < 0.5:
        return tiles.IceTile()
    elif f >= 0.5 and f <= 1:
        return tiles.WallTile()