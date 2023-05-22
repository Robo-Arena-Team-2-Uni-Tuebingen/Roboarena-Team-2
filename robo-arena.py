import random
import numpy as np
import sys
from robot import Robot
import tiles
from ascii_layout import textToTiles, translateAscii

from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal, QPointF, QThread
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtWidgets import QMainWindow, QFrame, QDesktopWidget, QApplication

class RobotThread(QThread):
    positionChanged = pyqtSignal(float, float)

    def __init__(self, robot):
        super().__init__()
        self.robot          = robot                 # robot class
        self.target_x       = robot.xpos            # x position
        self.target_y       = robot.ypos            # y position    
        self.speed          = robot.v               # speed
        self.turning_speed  = robot.v_alpha         # turning speed
        self.acceleration   = robot.a               # acceleration
        self.t_acceleration = robot.a_alpha         # turning acceleration
        self.acc_max        = robot.A_max           # maximum acceleration
        self.t_acc_max      = robot.A_alpha_max     # maximum turning acceleration

    def run(self):
        while True:
            self.moveRobotSmoothly()
            self.positionChanged.emit(self.robot.xpos, self.robot.ypos)
            self.msleep(50)  # Sleep for 50 milliseconds

    def moveRobotSmoothly(self):
        if self.robot.xpos != self.target_x:
            # Move towards the target X position
            if self.robot.xpos < self.target_x:
                self.robot.xpos += self.speed
            else:
                self.robot.xpos -= self.speed

        if self.robot.ypos != self.target_y:
            # Move towards the target Y position
            if self.robot.ypos < self.target_y:
                self.robot.ypos += self.speed
            else:
                self.robot.ypos -= self.speed

        # Check if the robot has reached the target position
        if self.robot.xpos == self.target_x and self.robot.ypos == self.target_y:
            self.generateNewTargetPosition()

    
    def generateNewTargetPosition(self):
        # Get the current tile indices of the robot
        current_tile_x = int(self.robot.xpos // Arena.TileWidth)
        current_tile_y = int(self.robot.ypos // Arena.TileHeight)

        # Generate random offsets to determine the neighboring tile
        offset_x = random.randint(-1, 1)
        offset_y = random.randint(-1, 1)

        # Calculate the new target tile indices, ensuring they are within the arena bounds
        new_tile_x = max(0, min(current_tile_x + offset_x, Arena.ArenaWidth - 1))
        new_tile_y = max(0, min(current_tile_y + offset_y, Arena.ArenaHeight - 1))

        # Calculate the target position based on the new tile indices
        self.target_x = new_tile_x * Arena.TileWidth + Arena.TileWidth // 2
        self.target_y = new_tile_y * Arena.TileHeight + Arena.TileHeight // 2

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
        self.robotThreads = []
        self.pawns = np.array([Robot(800, 1000, -np.pi/2, QColor(0xFFA500)), Robot(800, 400, -np.pi/2, QColor(0x8A2BE2)), 
                              Robot(200, 1000, -np.pi/2, QColor(0x00FFFF)), Robot(200, 400, -np.pi/2, QColor(0xFF0000))])
        self.createRobotThreads()
        # Create a timer to control the robot movement
        self.timer = QBasicTimer()
        self.timer.start(500, self)  # Timer interval and object to call

    def createRobotThreads(self):
        for robot in self.pawns:
            thread = RobotThread(robot)
            thread.positionChanged.connect(self.updateRobotPosition)
            self.robotThreads.append(thread)
            thread.start()

    def updateRobotPosition(self):
        #redraw the widget with updated robot positions
        self.update()


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
        
        self.drawRobot(painter, self.pawns[0])
        self.drawRobot(painter, self.pawns[1])
        self.drawRobot(painter, self.pawns[2])
        self.drawRobot(painter, self.pawns[3])


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



def main():

    app = QApplication(sys.argv)
    ra = RoboArena() 
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()   