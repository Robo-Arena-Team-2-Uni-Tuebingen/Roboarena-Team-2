import random
import numpy as np
from robot import Robot
from bullets import Bullet

from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal, QPointF, QThread

class RobotThread(QThread):
    positionChanged = pyqtSignal(float, float)

    def __init__(self, robot: Robot, arena, is_player):
        super().__init__()
        self.robot: Robot   = robot                 # robot class
        self.is_player      = is_player             # check if robot is player to determine movement
        self.is_paused      = False
        self.target_x       = robot.xpos + 8          # x position + 0.5*tile
        self.target_y       = robot.ypos + 8           # y position + 0.5*tile
        # size of the tiles
        self.arena = arena
        self.tile_width     = arena.TileWidth
        self.tile_height    = arena.TileHeight
        # size of the arena
        self.arena_width    = arena.ArenaWidth
        self.arena_height   = arena.ArenaHeight
        self.Mouse_x = robot.xpos
        self.Mouse_y = robot.ypos

        self.abort = False
    
    def run(self):
        #this sleep is necessary to ensure that all threads have started until they interact with each other
        self.msleep(10)
        #for enemies this loop will run until they die, for the player this loop will run as long as they have lives
        while (not self.robot.isRobotDead() or self.is_player) and not self.abort:
            if not self.is_paused:
                #handles respawns and loss condition
                if self.is_player and self.robot.isRobotDead():
                    self.arena.player_lives = self.arena.player_lives - 1
                    #100 points deducted for dying
                    self.arena.updatePointCounter(-100)
                    if self.arena.player_lives > 0:
                        self.robot.revive()
                    else:
                        self.arena.lose()
                #update the time-wincondition
                self.arena.updateTime()
                #vector-based movement of the robot
                self.moveRobotSmoothly()
                if self.is_player:
                    self.robot.getAlpha(self.Mouse_x, self.Mouse_y)
                else: 
                    loSPlayer = self.arena.hasLineOfSightToPlayer(self.robot.xpos, self.robot.ypos)
                    loSPlayerTarget = self.arena.hasLineOfSightToPlayerTarget(self.robot.xpos, self.robot.ypos)
                    playerpos = self.arena.getPlayerPosition()
                    playertarget = self.arena.getPlayerTarget()
                    #this function sets the new alpha and target of the robot, for the scout it also handles acceleration and deceleration
                    self.robot.behave(loSPlayer, loSPlayerTarget, playerpos, playertarget)
                    #update the target from inside the robot
                    self.target_x, self.target_y = self.robot.getTarget()
                    #determines whether the enemy opens fire or not
                    if(self.robot.openFire(loSPlayer, playerpos)):
                        shot, bullet = self.robot.shoot()
                        if shot:
                            self.arena.passBulletsToThread(bullet)
                #gets the tile from the arena class and applies a status effect
                currentTile = self.arena.getTileAtPos(self.robot.xpos, self.robot.ypos)
                if currentTile.hasEffect:
                    self.robot.applyEffect(currentTile.effect)
                self.robot.tickDownEffects()
            #trigger update of the GUI
            self.positionChanged.emit(self.robot.xpos, self.robot.ypos)
            self.msleep(30)
        #afterloop tasks for enemies
        if not self.is_player and not self.abort:
            self.arena.updateKillCounter()
            self.arena.updatePointCounter(self.robot.points)
            self.arena.removeRobot(self.robot)
            self.arena.spawnRobot()
            self.arena.spawnRobot()

    #processing of key events, only relevant for the thread that contains the player
    def processKeyEvent(self, eventDict):
        if self.is_player and (not self.is_paused):
            deltaTargetx = 0
            deltaTargety = 0
            if eventDict[Qt.Key_W]:
                deltaTargety -= self.tile_height

            if eventDict[Qt.Key_S]:
                deltaTargety += self.tile_height

            if eventDict[Qt.Key_A]:
                deltaTargetx -= self.tile_width

            if eventDict[Qt.Key_D]:
                deltaTargetx += self.tile_width

            if eventDict[Qt.Key_E]:
                self.robot.accelerate()
        
            if eventDict[Qt.Key_Q]:
                self.robot.decelerate()

            if eventDict[Qt.Key_Space]:  
                shot, bullet = self.robot.shoot()
                if shot:
                    self.arena.passBulletsToThread(bullet)
            self.setTarget(deltaTargetx, deltaTargety)

    #processes mouse events, which is currently just an update to the position
    def processMouseEvent(self, x, y, pressedMouseButtons):
        self.Mouse_x = x
        self.Mouse_y = y

    #responsible for moving the robot along a vector towards a target
    def moveRobotSmoothly(self):
        #gets the centerposition of the robot as an np array
        cPos = np.array([self.robot.xpos - self.robot.radius, self.robot.ypos - self.robot.radius])
        #gets the targetposition as a np array
        target = np.array([self.target_x, self.target_y])
        #subtracts center from target
        target_vector = np.subtract(target, cPos)
        #normalizes the vector to the target
        norm = np.linalg.norm(target_vector)
        #multiplies normalized target vector with the speed of the robot (which is influenced by status effects)
        if norm > 0:
            new_target_vector = self.robot.getV()*(target_vector/norm)
        else:
            new_target_vector = target_vector
        #prevents overshooting the target when the adjusted target_vector is longer than the actual vector to the target
        if np.linalg.norm(target_vector) < np.linalg.norm(new_target_vector):
            cPos = target
        else:
            cPos = cPos + new_target_vector

        #check if next movement location is Impassable
        collision = self.isTileAtPosImpassable(cPos[0], cPos[1])

        #adjusts the position to the upper left corner
        if not collision:
            self.robot.xpos = cPos[0] + self.robot.radius
            self.robot.ypos = cPos[1] + self.robot.radius

    #sets the new target determined by the keypress events for the player and ensures it stays within passable area and boundaries
    def setTarget(self, x, y):
        newTargetx = self.target_x + x
        newTargety = self.target_y + y

        if not self.isTileAtPosImpassable(newTargetx, newTargety):
            self.target_x = max(8, min(newTargetx, self.arena_width*self.tile_width - 9))
            self.target_y = max(8, min(newTargety, self.arena_height*self.tile_height - 9))

            self.robot.target_x = self.target_x
            self.robot.target_y = self.target_y

            return True

        return False
            
    def isTileAtPosImpassable(self, x, y):
        tile = self.arena.getTileAtPos(x, y)        
        return tile.isImpassable

    def unpauseRobots(self):
        self.is_paused = False

    def pauseRobots(self):
        self.is_paused = True