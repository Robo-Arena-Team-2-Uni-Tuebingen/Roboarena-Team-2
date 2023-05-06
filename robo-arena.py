import random
import numpy as np
import sys
from robot import Robot
import tiles

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
    TileWidth  = 10
    TileHeight = 10

    # Size of the arena in tiles
    ArenaWidth = 100
    ArenaHeight = 100

    def __init__(self, parent):
        super().__init__(parent)

        self.initArena()
        self.pawn = Robot(500, 700, -np.pi/2)

        # Create a timer to control the robot movement
        self.timer = QBasicTimer()
        self.timer.start(500, self)  # Timer interval and object to call


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
        
        self.drawRobot(painter, self.pawn)


    # paint a single tile
    def drawTile(self, painter, x, y, tile):
        painter.fillRect(x, y, tile.width, tile.height, tile.color)
    
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