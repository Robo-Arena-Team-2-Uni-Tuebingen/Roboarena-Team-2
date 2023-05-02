import typing
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtWidgets import QMainWindow, QFrame, QDesktopWidget, QApplication, QWidget
import numpy as np
import Tiles
import random
import sys
from robot import Robot

#temp
class RoboArena(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.arena = Arena(self)
        self.setCentralWidget(self.arena)

        self.resize(1200, 1200)
        self.center()
        self.setWindowTitle('RoboArena')
        self.show()

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move(int((screen.width() - size.width())/2),
                  int((screen.height() - size.height())/2))

#contains the Arena
class Arena(QFrame):
    

    def __init__(self, parent):
        super().__init__(parent)

        self.arenaHeight = 100
        self.arenaWidth = 100

        self.randomArena()
        self.pawn = Robot(500, 700, np.pi)
    
    #def initBoard(self):
        
    def randomArena(self):
        self.ArenaLayout = [[self.randomTile() for j in range(self.arenaWidth)] for i in range(self.arenaHeight)]
    
    def randomTile(self):
        h = random.randint(0,5)
        if h == 0:
            tile = Tiles.NormalTile()
        elif h == 1:
            tile = Tiles.WallTile()
        elif h == 2:
            tile = Tiles.FireTile()
        elif h == 3:
            tile = Tiles.IceTile()
        elif h == 4:
            tile = Tiles.WaterTile()
        elif h == 5:
            tile = Tiles.SandTile()
        return tile

    def paintEvent(self, event):
        painter = QPainter(self)
        rect = self.contentsRect()

        arenaTop = rect.bottom() - self.arenaHeight * Tiles.tileHeight

        for i in range(self.arenaHeight):
            for j in range(self.arenaWidth):
                tile = self.ArenaLayout[i][j]
                self.drawTile(painter, rect.left() + j * tile.width, arenaTop + i * tile.width, tile)
        
        self.drawRobot(painter, self.pawn)

    def drawTile(self, painter, x, y, tile):
        painter.fillRect(x, y, tile.width, tile.height, tile.color)

    def drawRobot(self, painter, robot):
        centerRobot = QtCore.QPointF(robot.xpos - robot.radius, robot.ypos - robot.radius)
        direction = QtCore.QPointF(robot.radius*np.cos(robot.alpha) + centerRobot.x(), robot.radius*np.sin(robot.alpha) + centerRobot.y())
        painter.setBrush(QColor(0xFFA500))
        painter.drawEllipse(centerRobot, robot.radius, robot.radius)
        painter.drawLine(centerRobot, direction)

def main():
    app = QApplication(sys.argv)
    ra = RoboArena()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()