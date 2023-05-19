import random
import numpy as np
import sys
from robot import Robot
import tiles
from ascii_layout import textToTiles, translateAscii

from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal, QPointF
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
    TileWidth  = tiles.tileWidth
    TileHeight = tiles.tileHeight

    # Size of the arena in tiles
    ArenaWidth = 60
    ArenaHeight = 60

    def __init__(self, parent):
        super().__init__(parent)

        self.initArena()
        self.pawn = Robot(500, 700, -np.pi/2)

        # Create a timer to control the robot movement
        self.timer = QBasicTimer()
        self.timer.start(500, self)  # Timer interval and object to call


    def initArena(self):
        # set default arena saved in .txt file "layout1"
        self.ArenaLayout = textToTiles("testlayout.txt")
        for x in range(self.ArenaWidth):
            for y in range(self.ArenaHeight):
                if y - 1 > 0:
                    left = self.ArenaLayout[x, y - 1]
                else:
                    left = tiles.Tile()
                if y + 1 < self.ArenaHeight:
                    right = self.ArenaLayout[x, y + 1]
                else:
                    right = tiles.Tile()
                if x - 1 > 0:
                    up = self.ArenaLayout[x - 1, y]
                else:
                    up = tiles.Tile()
                if x + 1 < self.ArenaWidth:
                    down = self.ArenaLayout[x + 1, y]
                else:
                    down = tiles.Tile()
                context = [up, down, left, right]
                self.ArenaLayout[x, y].chooseTexture(context)

    #method that returns a random tile
    def randomTile(self):
        return random.choice([tiles.GrassTile, tiles.HighGrassTile, tiles.DirtTile, tiles.SandTile, tiles.FieldTile, tiles.CobbleStone, tiles.WaterTile, tiles.WallTile, tiles.SnowTile, tiles.SlimeTile])

    # paint all tiles of the arena
    def paintEvent(self, event):

        painter = QPainter(self)
        rect = self.contentsRect()

        arenaTop = rect.bottom() - self.ArenaHeight * self.TileHeight

        for i in range(self.ArenaHeight):
            for j in range(self.ArenaWidth):
                tile = self.ArenaLayout[i, j]

                self.drawTile(painter,
                              rect.left() + j * Arena.TileWidth, 
                              arenaTop + i * Arena.TileHeight, tile)
        
        self.drawRobot(painter, self.pawn)


    # paint a single tile
    def drawTile(self, painter, x, y, tile):
        painter.drawImage(x, y, tile.texture)
    
    #this method is responsible for painting the robot in the window
    def drawRobot(self, painter, robot):
        #corrects the position of the robot to the upper left corner where the drawing is positioned
        centerRobot = QPointF(robot.xpos - robot.radius, robot.ypos - robot.radius)
        #calculates the point indicated by the angle on the circle of the robot
        direction = QPointF(robot.radius*np.cos(robot.alpha) + centerRobot.x(), -robot.radius*np.sin(robot.alpha) + centerRobot.y())
        painter.setBrush(QColor(0xFFA500))
        painter.drawEllipse(centerRobot, robot.radius, robot.radius)
        painter.drawLine(centerRobot, direction)

    def timerEvent(self, event):
        # Move the robot randomly
        direction = random.choice(["up", "down", "left", "right"])
        if  direction  == "up" and self.pawn.ypos > 0:
            self.pawn.ypos -= Arena.TileHeight
        elif direction == "down" and self.pawn.ypos < self.height() - Arena.TileHeight:
            self.pawn.ypos += Arena.TileHeight
        elif direction == "left" and self.pawn.xpos > 0:
            self.pawn.xpos -= Arena.TileWidth
        elif direction == "right" and self.pawn.xpos < self.width() - Arena.TileWidth:
            self.pawn.xpos += Arena.TileWidth

        self.update()  # Redraw the widget



def main():

    app = QApplication(sys.argv)
    ra = RoboArena()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()   