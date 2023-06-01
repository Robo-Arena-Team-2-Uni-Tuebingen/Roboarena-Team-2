import random

from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal, QPointF, QThread

class RobotThread(QThread):
    positionChanged = pyqtSignal(float, float)

    def __init__(self, robot, arena):
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
        # size of the tiles
        self.tile_width     = arena.TileWidth
        self.tile_height    = arena.TileHeight
        # size of the arena
        self.arena_width    = arena.ArenaWidth
        self.arena_height   = arena.ArenaHeight

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
        current_tile_x = int(self.robot.xpos // self.tile_width)
        current_tile_y = int(self.robot.ypos // self.tile_height)

        # Generate random offsets to determine the neighboring tile
        offset_x = random.randint(-1, 1)
        offset_y = random.randint(-1, 1)

        # Calculate the new target tile indices, ensuring they are within the arena bounds
        new_tile_x = max(0, min(current_tile_x + offset_x, self.arena_width - 1))
        new_tile_y = max(0, min(current_tile_y + offset_y, self.arena_height - 1))

        # Calculate the target position based on the new tile indices
        self.target_x = new_tile_x * self.tile_width + self.tile_width // 2
        self.target_y = new_tile_y * self.tile_height + self.tile_height // 2