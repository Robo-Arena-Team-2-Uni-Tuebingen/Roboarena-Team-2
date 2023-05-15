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
        m =  np.matrix([list(line.strip()) for line in infile.readlines()])
        return m

# translate characters into it's corresponding tile type
def translateAscii(c):
    if c == "X":
        return tiles.WallTile()
    elif c == "f":
        return tiles.FireTile()
    elif c == "i":
        return tiles.IceTile()
    elif c == "w":
            return tiles.WaterTile()
    elif c == "s":
        return tiles.SandTile()
    else:
        return tiles.NormalTile()
