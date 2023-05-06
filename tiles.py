from PyQt5.QtGui import QColor

tileWidth = 10
tileHeight = 10

#super class for tiles
class Tile():
    def __init__(self):
        self.width = tileWidth
        self.height = tileHeight

#normal tile
class NormalTile(Tile):
    def __init__(self):
        super().__init__()
        self.color = QColor(0x66CD00)

#wall tile
class WallTile(Tile):
    def __init__(self):
        super().__init__()
        self.color = QColor(0x000000)

#fire tile
class FireTile(Tile):
    def __init__(self):
        super().__init__()
        self.color = QColor(0xFF4500)

#Ice tile
class IceTile(Tile):
    def __init__(self):
        super().__init__()
        self.color = QColor(0xB0E2FF)

#Water tile
class WaterTile(Tile):
    def __init__(self):
        super().__init__()
        self.color = QColor(0x1E90FF)

#Sand tile
class SandTile(Tile):
    def __init__(self):
        super().__init__()
        self.color = QColor(0xFFEC8B)