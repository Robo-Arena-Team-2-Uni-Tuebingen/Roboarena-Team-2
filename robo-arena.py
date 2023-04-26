import random
import numpy as np
import sys

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
        self.ArenaLayout = [[TileTypes.Normal for j in range(Arena.ArenaWidth)] for i in range(Arena.ArenaHeight)]

    # generates a random layout by filling the matrix ArenaLayout with random integers which represent the diffrent tiles
    def setRandomLayout(self):
        for i in range(Arena.ArenaHeight):
            for j in range(Arena.ArenaWidth):
                self.ArenaLayout[i][j] = random.randint(0,5)

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

        # color of the tiles
        colorTable = [0x66CD00, 0x000000, 0xFF4500, 0xB0E2FF,
                      0x1E90FF, 0xFFEC8B]

        color = QColor(colorTable[tile])
        painter.fillRect(x, y, Arena.TileWidth,
                         Arena.TileHeight, color)

# class TileTypes contains the names of all possible tiles 
class TileTypes(object):
    Normal = 0
    Wall   = 1
    Fire   = 2
    Ice    = 3
    Water  = 4
    Sand   = 5

def main():

    app = QApplication(sys.argv)
    ra = RoboArena()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()   