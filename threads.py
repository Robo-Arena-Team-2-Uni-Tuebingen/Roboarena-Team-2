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
        self.msleep(10)
        while (not self.robot.isRobotDead() or self.is_player) and not self.abort:
            if not self.is_paused:
                if self.is_player and self.robot.isRobotDead():
                    self.arena.player_lives = self.arena.player_lives - 1
                    if self.arena.player_lives > 0:
                        self.robot.health = 100
                    else:
                        self.arena.lose()
                self.moveRobotSmoothly()
                if self.is_player:
                    self.robot.getAlpha(self.Mouse_x, self.Mouse_y)
                else:
                    self.robot.behave(self.arena.hasLineOfSightToPlayer(self.robot.xpos, self.robot.ypos),
                                      self.arena.hasLineOfSightToPlayerTarget(self.robot.xpos, self.robot.ypos),
                                      self.arena.getPlayerPosition(), self.arena.getPlayerTarget())
                    self.target_x = self.robot.target_x
                    self.target_y = self.robot.target_y
                    if(self.robot.openFire(self.arena.hasLineOfSightToPlayer(self.robot.xpos, self.robot.ypos), self.arena.getPlayerPosition())):
                        shot, bullet = self.robot.shoot()
                        if shot:
                            self.arena.passBulletsToThread(bullet)
                currentTile = self.arena.getTileAtPos(self.robot.xpos, self.robot.ypos)
                if currentTile.hasEffect:
                    self.robot.applyEffect(currentTile.effect)
                self.robot.tickDownEffects()
                
            self.positionChanged.emit(self.robot.xpos, self.robot.ypos)
            self.msleep(30)
        if not self.is_player and not self.abort:
            self.arena.updateKillCounter()
            self.arena.updatePointCounter(self.robot.points)
            self.arena.removeRobot(self.robot)
            self.arena.spawnRobot()
            self.arena.spawnRobot()

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

    def processMouseEvent(self, x, y, pressedMouseButtons):
        self.Mouse_x = x
        self.Mouse_y = y

    def moveRobotSmoothly(self):
        cPos = np.array([self.robot.xpos - self.robot.radius, self.robot.ypos - self.robot.radius])
        target = np.array([self.target_x, self.target_y])
        target_vector = np.subtract(target, cPos)
        norm = np.linalg.norm(target_vector)
        if norm > 0:
            target_vector = self.robot.getV()*(target_vector/norm)
        if np.linalg.norm(np.subtract(target, cPos)) < np.linalg.norm(target_vector):
            cPos = target
        else:
            cPos = cPos + target_vector

        #check if next movement location is Impassable
        collision = self.isTileAtPosImpassable(cPos[0], cPos[1])

        if not collision:
            self.robot.xpos = cPos[0] + self.robot.radius
            self.robot.ypos = cPos[1] + self.robot.radius

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