import random
import numpy as np
import sys
import tiles

from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtWidgets import QMainWindow, QFrame, QDesktopWidget, QApplication

class RoboArena(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.rarena = Arena(self)
        self.setCentralWidget(self.rarena)

        self.resize(1200, 1200)
        self.center()
        self.setWindowTitle('RoboArena')
        self.show()

    # centers the window on the screen
    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move(int((screen.width() - size.width()) / 2),
                  int((screen.height() - size.height()) / 2))

class Arena(QFrame):

    # Size of tiles in pixels
    TileWidth  = 10
    TileHeight = 10

    # Size of the arena in tiles
    ArenaWidth = 100
    ArenaHeight = 100

    def __init__(self, parent):
        super().__init__(parent)

        self.initArena()

    def initArena(self):
        # create an arena layout with a matrix filled at the start only with "normal" tiles
         self.ArenaLayout = [[self.randomTile() for j in range(self.ArenaWidth)] for i in range(self.ArenaHeight)]
    
    #method that returns a random tile
    def randomTile(self):
        h = random.randint(0,5)
        if h == 0:
            tile = tiles.NormalTile()
        elif h == 1:
            tile = tiles.WallTile()
        elif h == 2:
            tile = tiles.FireTile()
        elif h == 3:
            tile = tiles.IceTile()
        elif h == 4:
            tile = tiles.WaterTile()
        elif h == 5:
            tile = tiles.SandTile()
        return tile

    # paint all tiles of the arena
    def paintEvent(self, event):

        painter = QPainter(self)
        rect = self.contentsRect()

        arenaTop = rect.bottom() - self.ArenaHeight * self.TileHeight

        for i in range(Arena.ArenaHeight):
            for j in range(Arena.ArenaWidth):
                tile = self.ArenaLayout[i][j]

                self.drawTile(painter,
                              rect.left() + j * Arena.TileWidth, 
                              arenaTop + i * Arena.TileHeight, tile)


    # paint a single tile
    def drawTile(self, painter, x, y, tile):
        painter.fillRect(x, y, tile.width, tile.height, tile.color)


def main():

    app = QApplication(sys.argv)
    ra = RoboArena()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()   