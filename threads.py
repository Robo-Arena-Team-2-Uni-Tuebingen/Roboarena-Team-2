import random
import numpy as np
from robot import Robot

from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal, QPointF, QThread

class RobotThread(QThread):
    positionChanged = pyqtSignal(float, float)

    def __init__(self, robot, arena, is_player):
        super().__init__()
        self.robot: Robot          = robot                 # robot class
        self.is_player      = is_player             # check if robot is player to determine movement
        self.is_paused      = False
        self.target_x       = robot.xpos           # x position
        self.target_y       = robot.ypos           # y position    
        # size of the tiles
        self.tile_width     = arena.TileWidth
        self.tile_height    = arena.TileHeight
        # size of the arena
        self.arena_width    = arena.ArenaWidth
        self.arena_height   = arena.ArenaHeight
        self.Mouse_x = robot.xpos
        self.Mouse_y = robot.ypos
       
    
    def run(self):
        while not self.is_paused:
            self.moveRobotSmoothly()
            self.robot.getAlpha(self.Mouse_x, self.Mouse_y)
            self.positionChanged.emit(self.robot.xpos, self.robot.ypos)
            self.msleep(30)


    def processKeyEvent(self, eventDict):
        if self.is_player and (not self.is_paused):
            if eventDict[Qt.Key_W]:
                self.target_y -= self.tile_height

            if eventDict[Qt.Key_S]:
                self.target_y += self.tile_height

            if eventDict[Qt.Key_A]:
                self.target_x -= self.tile_width

            if eventDict[Qt.Key_D]:
                self.target_x += self.tile_width

            if eventDict[Qt.Key_E]:
                self.robot.accelerate()
        
            if eventDict[Qt.Key_Q]:
                self.robot.deccelerate()

        if eventDict[Qt.Key_Escape]:
            
            if self.is_paused:
                self.unpauseRobots()

            else: 
                self.pauseRobots()

            
        
        self.target_x = max(0, min(self.target_x, self.arena_width*self.tile_width - 1))
        self.target_y = max(240, min(self.target_y, self.arena_height*self.tile_height - 1 + 240))
        self.robot.target_x = self.target_x
        self.robot.target_y = self.target_y

    def processMouseEvent(self, x, y, pressedMouseButtons):
        self.Mouse_x = x
        self.Mouse_y = y

    def moveRobotSmoothly(self):
        cPos = np.array([self.robot.xpos - self.robot.radius, self.robot.ypos - self.robot.radius])
        target = np.array([self.target_x, self.target_y])
        target_vector = np.subtract(target, cPos)
        norm = np.linalg.norm(target_vector)
        if norm > 0:
            target_vector = self.robot.v*(target_vector/norm)
        if np.linalg.norm(np.subtract(target, cPos)) < np.linalg.norm(target_vector):
            cPos = target
        else:
            cPos = cPos + target_vector
        self.robot.xpos = cPos[0] + self.robot.radius
        self.robot.ypos = cPos[1] + self.robot.radius

        # Check if the robot has reached the target position
        if cPos[0] - self.target_x < 1 and cPos[1] - self.target_y < 1 and not self.is_player:
            self.generateNewTargetPosition()
            self.robot.target_x = self.target_x
            self.robot.target_y = self.target_y

    def unpauseRobots(self):
        self.is_paused = False
        self.msleep(1000)

    def pauseRobots(self):
        self.is_paused = True
        self.msleep(1000)
    
    def generateNewTargetPosition(self):
        # Get the current tile indices of the robot
        current_tile_x = int(self.robot.xpos // self.tile_width)
        current_tile_y = int(self.robot.ypos // self.tile_height)

        # Generate random offsets to determine the neighboring tile
        offset_x = random.randint(0, 60)
        offset_y = random.randint(0, 60)

        # Calculate the new target tile indices, ensuring they are within the arena bounds
        #new_tile_x = max(0, min(current_tile_x + offset_x, self.arena_width - 1))
        #new_tile_y = max(0, min(current_tile_y + offset_y, self.arena_height - 1))

        # Calculate the target position based on the new tile indices
        self.target_x = offset_x * self.tile_width + self.tile_width // 2
        self.target_y = (offset_y * self.tile_height + self.tile_height // 2) + 240