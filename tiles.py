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

textureNormalTile = dungeon.copy(0*tileWidth, 12*tileHeight, tileWidth, tileHeight)
textureWallTile = exterior.copy(getTileRect(14, 10))
textureFireTile = dungeon.copy(getTileRect(4, 10))
textureIceTile = dungeon.copy(getTileRect(10, 2))
textureWaterTile = dungeon.copy(getTileRect(0, 4))
textureSandTile = exterior.copy(getTileRect(4, 14))

#super class for tiles
class Tile():
    def __init__(self):
        self.width = tileWidth
        self.height = tileHeight

#normal tile
class NormalTile(Tile):
    def __init__(self):
        super().__init__()
        self.texture = textureNormalTile

#wall tile
class WallTile(Tile):
    def __init__(self):
        super().__init__()
        self.texture = textureWallTile

#fire tile
class FireTile(Tile):
    def __init__(self):
        super().__init__()
        self.texture = textureFireTile

#Ice tile
class IceTile(Tile):
    def __init__(self):
        super().__init__()
        self.texture = textureIceTile

#Water tile
class WaterTile(Tile):
    def __init__(self):
        super().__init__()
        self.texture = textureWaterTile

#Sand tile
class SandTile(Tile):
    def __init__(self):
        super().__init__()
        self.texture = textureSandTile

