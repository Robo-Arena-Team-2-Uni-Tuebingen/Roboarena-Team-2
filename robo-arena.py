import random
from PyQt5 import QtGui
import numpy as np
import sys
from robot import Robot
import tiles
from ascii_layout import textToTiles, translateAscii
import threads
from pause_menu import PauseMenu

import PyQt5.QtQuick
from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal, QPointF
from PyQt5.QtGui import QPainter, QColor, QKeyEvent, QMouseEvent
from PyQt5.QtWidgets import QMainWindow, QWidget, QFrame, QDesktopWidget, QApplication, QHBoxLayout, QVBoxLayout


class RoboArena(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.rarena = Arena(self)
        self.rarena.setMouseTracking(True)
        
        self.pause         = PauseMenu(self)
        self.pause_visible = False
        
        main_layout = QHBoxLayout()
        main_layout.addWidget(self.rarena)
        main_layout.addWidget(self.pause)
        main_layout.setContentsMargins(0, 0, 0, 0)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        central_widget.setMouseTracking(True)
        self.setCentralWidget(central_widget)

        self.pause.hide()
        self.resize(1940, 1200)
        self.center()
        self.setWindowTitle('RoboArena')
        self.show()

    # centers the window on the screen
    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move(int((screen.width() - size.width()) / 2),
                  int((screen.height() - size.height()) / 2))
        
    def keyPressEvent(self, event):  #get key press to the threads
        self.rarena.logKeyPressEvent(event)

        if event.key() == Qt.Key_Escape:
            self.toggle_pause()

    def keyReleaseEvent(self, event):
        self.rarena.logKeyReleaseEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        self.rarena.passMouseEvents(event)
    
    def mousePressEvent(self, event: QMouseEvent) -> None:
        self.rarena.passMouseEvents(event)
    
    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        self.rarena.passMouseEvents(event)

    def toggle_pause(self):

        if self.pause_visible:
            self.pause.hide()
        else:
            self.pause.show()
        
        self.pause_visible = not self.pause_visible


class Arena(QFrame):

    # Size of tiles in pixels
    TileWidth  = tiles.tileWidth
    TileHeight = tiles.tileHeight

    # Size of the arena in tiles
    ArenaWidth = 60
    ArenaHeight = 60

    PressedKeys = {
        Qt.Key_W: False,
        Qt.Key_A: False,
        Qt.Key_S: False,
        Qt.Key_D: False,
        Qt.Key_E: False,
        Qt.Key_Q: False,
        Qt.Key_Escape: False
    }

    pressedMouseButtons = {
        Qt.MouseButton.LeftButton: False,
        Qt.MouseButton.RightButton: False
    }

    def __init__(self, parent):
        super().__init__(parent)
        parent.setMouseTracking(True)
        self.setMouseTracking(True)

        self.initArena()
        self.robotThreads = []
        self.pawns = np.array([Robot(200, 400,  -np.pi/2, QColor(0xFF0000), is_player=True),
                               Robot(800, 1000, -np.pi/2, QColor(0xFFA500), is_player=False),
                               Robot(800, 400,  -np.pi/2, QColor(0x8A2BE2), is_player=False),
                               Robot(200, 1000, -np.pi/2, QColor(0x00FFFF), is_player=False)])  #is_play flags the robots which should be controlled manually

        self.createRobotThreads()
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

    def createRobotThreads(self):
        for robot in self.pawns:
            is_player = robot.is_player
            thread = threads.RobotThread(robot, self, is_player)
            thread.positionChanged.connect(self.updateRobotPosition)
            self.robotThreads.append(thread)
            thread.start()

    def updateRobotPosition(self):
        #redraw the widget with updated robot positions
        self.update()

    #method that returns a random tile
    def randomTile(self):
        return random.choice([tiles.GrassTile, tiles.HighGrassTile, tiles.DirtTile, tiles.SandTile, tiles.FieldTile, tiles.CobbleStoneTile, tiles.WaterTile, tiles.WallTile, tiles.SnowTile, tiles.SlimeTile])

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
        
        for robot in self.pawns:
            self.drawRobot(painter, robot)

    # paint a single tile
    def drawTile(self, painter, x, y, tile):
        painter.drawImage(x, y, tile.texture)
    
    #this method is responsible for painting the robot in the window
    def drawRobot(self, painter, robot):
         #corrects the position of the robot to the upper left corner where the drawing is positioned
         centerRobot = QPointF(robot.xpos - robot.radius, robot.ypos - robot.radius)
         #calculates the point indicated by the angle on the circle of the robot
         direction = QPointF(robot.radius*np.cos(robot.alpha) + centerRobot.x(), -robot.radius*np.sin(robot.alpha) + centerRobot.y())
         painter.setBrush(robot.color)
         painter.drawEllipse(centerRobot, robot.radius, robot.radius)
         painter.drawLine(centerRobot, direction)
         painter.setBrush(robot.targetColor)
         painter.drawEllipse(QPointF(robot.target_x, robot.target_y), 5, 5)

    def logKeyPressEvent(self, event):
        if self.PressedKeys.__contains__(event.key()):
            self.PressedKeys[event.key()] = True
            self.passKeyEvents(self.PressedKeys)
            
        
    def logKeyReleaseEvent(self, event):
        if self.PressedKeys.__contains__(event.key()):
            self.PressedKeys[event.key()] = False
            self.passKeyEvents(self.PressedKeys)

    def passKeyEvents(self, eventDict):
        for thread in self.robotThreads:
            thread.processKeyEvent(eventDict)

    def passMouseEvents(self, event: QMouseEvent):
        for key in self.pressedMouseButtons.keys():
            self.pressedMouseButtons[key] = event.buttons() & key
        self.robotThreads[0].processMouseEvent(event.x(), event.y(), self.pressedMouseButtons)

def main():

    app = QApplication(sys.argv)
    roboArena = RoboArena() 
    roboArena.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()   