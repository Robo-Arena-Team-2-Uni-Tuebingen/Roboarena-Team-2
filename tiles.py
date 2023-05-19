from PyQt5.QtGui import QColor, QPixmap, QImage
from PyQt5.QtCore import QRect

tileWidth = 16
tileHeight = 16
tilePath = '\openRPG_Tilesets_5.24.22'
dungeon = QImage('dungeon.png')
exterior = QImage('exterior.png')
interior = QImage('interior.png')

def getTileRect(x, y):
    return QRect(x*tileWidth, y*tileHeight, tileWidth, tileHeight)

def getBigTileRect(x, y):
    return QRect(x*tileWidth, y*tileHeight, 3*tileWidth, 3*tileHeight)

textureWallTile = exterior.copy(getTileRect(14, 10))
textureWaterTile = exterior.copy(getTileRect(0, 4))
textureGrassTile = exterior.copy(getTileRect(0, 8))
textureDirtTile = exterior.copy(getBigTileRect(0, 13))
textureHighGrassTile = exterior.copy(getBigTileRect(3, 9))
textureSandTile = exterior.copy(getBigTileRect(3, 13))
textureSnowTile = exterior.copy(getBigTileRect(6, 1))
textureSlimeTile = exterior.copy(getBigTileRect(9, 1))
textureFieldTile = exterior.copy(getBigTileRect(6, 5))
textureCobbleStoneTile = exterior.copy(getBigTileRect(9, 5))

#super class for tiles
class Tile():
    str = ''
    def __init__(self):
        self.str = Tile.str
        self.width = tileWidth
        self.height = tileHeight

    def compare(self, contextTile):
        if contextTile.str == self.str:
            return True
        else:
            return False

    #this function is supposed to determine whether the tile needs to be a tile with a transition, and if yes, choose which transition is necessary
    #watertiles not yet included
    #more special tiles have not been implemented for this
    def chooseTexture(self, context):
        left = self.compare(context[0])
        right = self.compare(context[1])
        up = self.compare(context[2])
        down = self.compare(context[3])
        #upleft = self.compare(context[0][0])
        #upright = self.compare(context[2][0])
        #downleft = self.compare(context[0][2])
        #downright = self.compare(context[2][2])
        
        #resolve whether the tile has a tile of the same type to the up or down
        if up and down:
            x = 1
        elif up:
            x = 2
        elif down:
            x = 0
        else:
            #tbd, placeholder, maybe resolve over map generation/design
            x = 1
            y = 1
        
        #resolve whether the tile has a tile of the same type to the left or right
        if left and right:
            y = 1
        elif left:
            y = 2
        elif right:
            y = 0
        else:
            #tbd, placeholder, maybe resolve over map generation/design
            x = 1
            y = 1

        #depending on x and y choose the appropriate subimage from the big tile and use it from hereon as texture
        self.texture = self.texture.copy(getTileRect(x, y))

class WallTile(Tile):
    str = 'X'
    def __init__(self):
        self.str = WallTile.str
        self.texture = textureWallTile
    
    def chooseTexture(self, context):
        return self.texture

class WaterTile(Tile):
    str = 'w'
    def __init__(self):
        self.str = WaterTile.str
        self.texture = textureWaterTile
    
    def chooseTexture(self, context):
        return self.texture

class GrassTile(Tile):
    str = 'g'
    def __init__(self):
        self.str = GrassTile.str
        self.texture = textureGrassTile
    
    def chooseTexture(self, context):
        return self.texture

class HighGrassTile(Tile):
    str = 'h'
    def __init__(self):
        self.str = HighGrassTile.str
        self.texture = textureHighGrassTile

class DirtTile(Tile):
    str = 'd'
    def __init__(self):
        self.str = DirtTile.str
        self.texture = textureDirtTile

class SandTile(Tile):
    str = 's'
    def __init__(self):
        self.str = SandTile.str
        self.texture = textureSandTile

class SnowTile(Tile):
    str = 'i'
    def __init__(self):
        self.str = SnowTile.str
        self.texture = textureSnowTile

class SlimeTile(Tile):
    str = 'v'
    def __init__(self):
        self.str = SlimeTile.str
        self.texture = textureSlimeTile

class FieldTile(Tile):
    str = 'f'
    def __init__(self):
        self.str = FieldTile.str
        self.texture = textureFieldTile

class CobbleStone(Tile):
    str = 'c'
    def __init__(self):
        self.str = CobbleStone.str
        self.texture = textureCobbleStoneTile
