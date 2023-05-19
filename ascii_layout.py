import numpy as np
import tiles

# textToTiles takes a .txt file and generates a matrix of tiles from it
def textToTiles(tf):
    applyall = np.vectorize(translateAscii)
    m = textToMatrix(tf)
    return applyall(m)

# textToTiles put the single characters of a .txt file into a matrix
def textToMatrix(tf):
    with open(tf, "rt") as infile:
        m = np.matrix([list(line.strip()) for line in infile.readlines()])
        return m

# translate characters into it's corresponding tile type
def translateAscii(c):
    if c == tiles.WallTile.str:
        return tiles.WallTile()
    elif c == tiles.FieldTile.str:
        return tiles.FieldTile()
    elif c == tiles.SnowTile.str:
        return tiles.SnowTile()
    elif c == tiles.WaterTile.str:
        return tiles.WaterTile()
    elif c == tiles.SandTile.str:
        return tiles.SandTile()
    elif c == tiles.GrassTile.str:
        return tiles.GrassTile()
    elif c == tiles.SlimeTile.str:
        return tiles.SlimeTile()
    elif c == tiles.HighGrassTile.str:
        return tiles.HighGrassTile()
    elif c == tiles.CobbleStone.str:
        return tiles.CobbleStone()
    elif c == tiles.DirtTile.str:
        return tiles.DirtTile()
