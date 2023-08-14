import random
import numpy as np
import sys
from robot import Robot
import bullets
import tiles
from ascii_layout import textToTiles
import threads
import time
from pause_menu import PauseMenu
from game_menu import GameMenu
from settings_menu import SettingsMenu
from music_player import MusicPlayer 
from end_screen import EndScreen

import PyQt5.QtQuick
from PyQt5.QtCore import Qt, QRect, QBasicTimer, pyqtSignal, QPointF
from PyQt5.QtGui import QPainter, QColor, QFont, QKeyEvent, QMouseEvent, QBrush
from PyQt5.QtWidgets import QMainWindow, QWidget, QFrame, QDesktopWidget, QApplication, QHBoxLayout, QVBoxLayout, QStackedWidget, QLabel, QPushButton


class RoboArena(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setFixedSize(1200, 960)
        self.setWindowTitle('RoboArena')
        self.setObjectName("RoboArena")
        
        self.initUI()

    def initUI(self):

        self.game_running = False

        self.game_menu = GameMenu()
        self.game_menu.play_button.clicked.connect(self.switchToGame)
        self.game_menu.settings_button.clicked.connect(self.switchToSettings)

        self.stacked_widget = QStackedWidget(self)
        self.stacked_widget.addWidget(self.game_menu)

        self.setCentralWidget(self.stacked_widget)
        self.center()
        self.show()
        
        # Set the stacked widget as the main layout of the RoboArena
        layout = QVBoxLayout(self)
        layout.addWidget(self.stacked_widget)
        self.setLayout(layout)

        # play background music
        self.music_player = MusicPlayer()
        self.music_player.load_song("backgroundmusic/discord_amongst_operatives.mp3")
        self.music_player.playOrPauseMusic()

    def switchToGame(self):
        self.resize(1200, 960)
        self.passSpinBoxValues()
        self.makeGameWidget()
        self.game_running = True
        self.stacked_widget.setCurrentWidget(self.game_widget)
        self.center()
    
    def switchToMenu(self):
        self.resize(1200, 960)
        self.game_running = False
        # Switch to the menu widget in the stacked widget
        self.stacked_widget.setCurrentWidget(self.game_menu)
        self.center()

    def switchToSettings(self):
        self.resize(1200, 960)
        self.settings = SettingsMenu()
        self.settings.volume_slider.valueChanged.connect(self.music_player.set_volume)
        self.settings.volume_slider.setValue(self.music_player.volume)
        self.settings.music_button.clicked.connect(self.music_player.playOrPauseMusic)
        self.settings.back_button.clicked.connect(self.switchToMenu)
        self.stacked_widget.addWidget(self.settings)
        self.stacked_widget.setCurrentWidget(self.settings)
        self.center()

    def switchToVictoryScreen(self, kills, time, points):
        screenshot      = self.grab()
        self.end_screen = EndScreen(screenshot)
        self.end_screen.setupVictory(kills, time, points)
        self.end_screen.quit_button.clicked.connect(self.switchToMenu)
        self.end_screen.retry_button.clicked.connect(self.switchToGame)
        self.stacked_widget.addWidget(self.end_screen)
        self.stacked_widget.setCurrentWidget(self.end_screen)

    def switchToDefeatScreen(self, kills, time, points):
        screenshot      = self.grab()
        self.end_screen = EndScreen(screenshot)
        self.end_screen.setupDefeat(kills, time, points)
        self.end_screen.quit_button.clicked.connect(self.switchToMenu)
        self.end_screen.retry_button.clicked.connect(self.switchToGame)
        self.stacked_widget.addWidget(self.end_screen)
        self.stacked_widget.setCurrentWidget(self.end_screen)

    # centers the window on the screen
    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move(int((screen.width() - size.width()) / 2),
                  int((screen.height() - size.height()) / 2))
        
    def keyPressEvent(self, event):  #get key press to the threads
        if self.game_running:
            self.arena.logKeyPressEvent(event)

        if event.key() == Qt.Key_Escape:
            self.toggle_pause()

    def keyReleaseEvent(self, event):
        if self.game_running:
            self.arena.logKeyReleaseEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if self.game_running:
            self.arena.passMouseEvents(event)
    
    def mousePressEvent(self, event: QMouseEvent) -> None:
        if self.game_running:
            self.arena.passMouseEvents(event)
    
    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if self.game_running:
            self.arena.passMouseEvents(event)

    def toggle_pause(self):
        if self.game_running:
            if self.pause_visible:
                self.pause.hide()
                self.arena.unpause()
            else:
                self.arena.pause()
                self.pause.show()
            
            self.pause_visible = not self.pause_visible

    def makeGameWidget(self):

        self.arena = Arena(self)
        self.arena.setMouseTracking(True)
        self.arena.showVictory.connect(self.switchToVictoryScreen)
        self.arena.showDefeat.connect(self.switchToDefeatScreen)
        
        self.pause         = PauseMenu(self)
        self.pause.hide()
        self.pause_visible = False
        self.pause.quit_button.clicked.connect(self.switchToMenu)

        # make the slider of the pause menu able to change the volume of the background muisc
        self.pause.volume_slider.valueChanged.connect(self.music_player.set_volume)
        self.pause.volume_slider.setValue(self.music_player.volume)
        
        main_layout = QHBoxLayout()
        main_layout.addWidget(self.arena)
        main_layout.addWidget(self.pause)
        main_layout.setContentsMargins(0, 0, 0, 0)

        self.game_widget = QWidget()
        self.game_widget.setLayout(main_layout)
        self.game_widget.setMouseTracking(True)

        self.stacked_widget.addWidget(self.game_widget)
        self.stacked_widget.setMouseTracking(True)

    def passSpinBoxValues(self):
        self.player_numbers = self.game_menu.player_number.value()
        self.arena_number = self.game_menu.arena_number.value()

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
        Qt.Key_Escape: False,
        Qt.Key_Space: False
    }

    pressedMouseButtons = {
        Qt.MouseButton.LeftButton: False,
        Qt.MouseButton.RightButton: False
    }

    showVictory = pyqtSignal(str, str, str)
    showDefeat  = pyqtSignal(str, str, str)

    def __init__(self, parent):
        super().__init__(parent)
        self.parentObject = parent
        parent.setMouseTracking(True)
        self.setMouseTracking(True)

        self.pawns = np.array([Robot(600, 600,  -np.pi/2, player_number = 1, type ='player'),
                               Robot(200, 200,  -np.pi/2, player_number = 2, type ='scout')])
        #self.pawns = np.array([Robot(200, 200, -np.pi/2, 1, type ='player'),
        #                       Robot(600, 800, -np.pi/2, 2, type = 'assault'),
        #                       Robot(800, 200, -np.pi/2, 3, type = 'heavy_gunner'),
        #                       Robot(400, 800, -np.pi/2, 4, type = 'sniper'),
        #                       Robot(400, 400, 0, 5, type='scout')])
        self.player_numbers = parent.player_numbers
        self.arena_number = parent.arena_number
        self.points = 0
        self.victorycondition = 3 # 1: Victory by points, 2: Victory by Kills, 3: Victory by Time, 4: Survival
        self.starttime = time.time()
        self.currentTime = time.time()
        self.kills = 0
        self.player_lives = 2 # can be varied
        self.PointsToWin = 1000 # can be varied
        self.SecondsToWin = 60 # can be varied
        self.KillsToWin = 5 # can be varied
        self.chooseMap()
        self.initArena()
        self.createRobotThreads()
        self.createBulletsThread()

    def initArena(self):
        # set default arena saved in .txt file "layout1"
        self.ArenaLayout = textToTiles(self.arena_map)
        #this loop passes the direct neighbours of each tile to it, enabling it to choose the appropriate texture
        for x in range(self.ArenaWidth):
            for y in range(self.ArenaHeight):
                if y - 1 >= 0:
                    left = self.ArenaLayout[x, y - 1]
                else:
                    left = tiles.Tile()
                if y + 1 < self.ArenaHeight:
                    right = self.ArenaLayout[x, y + 1]
                else:
                    right = tiles.Tile()
                if x - 1 >= 0:
                    up = self.ArenaLayout[x - 1, y]
                else:
                    up = tiles.Tile()
                if x + 1 < self.ArenaWidth:
                    down = self.ArenaLayout[x + 1, y]
                else:
                    down = tiles.Tile()
                context = [up, down, left, right]
                self.ArenaLayout[x, y].chooseTexture(context)

    def getPlayerPosition(self):
        return self.pawns[0].xpos, self.pawns[0].ypos
    
    def getPlayerTarget(self):
        return self.pawns[0].target_x, self.pawns[0].target_y

    def createRobotThreads(self):
        self.robotThreads = []

        for robot in self.pawns:
            is_player = robot.player_number <= self.player_numbers
            self.appendRobotThread(robot, is_player)

    def removeRobot(self, robot):
        self.pawns = np.delete(self.pawns, np.where(self.pawns == robot))

    def addRobot(self, robot):
        self.pawns = np.append(self.pawns, robot)
        self.appendRobotThread(robot)
    
    #appends a new thread and starts it
    def appendRobotThread(self, robot, is_player=False):
        thread = threads.RobotThread(robot, self, is_player)
        thread.positionChanged.connect(self.updateRobotPosition)
        self.robotThreads.append(thread)
        thread.start()

    #spawns a robot at a random valid position
    def spawnRobot(self):
        x, y = self.getRandomValidPosition()
        type = random.choice(['heavy_gunner', 'cannoneer', 'assault', 'scout', 'sniper'])
        robot = Robot(x, y, random.random()*np.pi*2, 5, type=type)
        self.addRobot(robot)

    def createBulletsThread(self):
        self.bulletsThread = bullets.BulletThread(self)
        self.bulletsThread.start()

    def passBulletsToThread(self, bullet):
        self.bulletsThread.addBullet(bullet)

    def updateRobotPosition(self):
        #redraw the widget with updated robot positions
        self.update()

    def updatePointCounter(self, points):
        self.points = self.points + points
        if self.victorycondition == 1:
            if self.points > self.PointsToWin:
                self.win()

    def updateTime(self):
        self.currentTime = int(time.time())
        if self.victorycondition == 2:
            if self.starttime + self.SecondsToWin < self.currentTime:
                self.win() 
    
    def updateKillCounter(self):
        self.kills = self.kills + 1
        if self.victorycondition == 3:
            if self.KillsToWin < self.kills:
                self.win()

    def playerKill(self):
        self.player_lives = self.player_lives - 1
        #100 points deducted for dying
        self.updatePointCounter(-100)
        if self.player_lives > 0:
            return True
        else:
            self.lose()
            return False

    def win(self):
        self.stopGame()
        kills = self.kills.__str__()
        time = (self.currentTime - self.starttime).__str__()
        points = self.points.__str__()
        # emits signal with stats, so parent can show the correct screen 
        self.showVictory.emit(kills, time, points)

    def lose(self):
        self.stopGame()
        kills = self.kills.__str__()
        time = (self.currentTime - self.starttime).__str__()
        points = self.points.__str__()
        # emits signal with stats, so parent can show the correct screen
        self.showDefeat.emit(kills, time, points)

    #method to end the respective threads in a controlled manner by setting the abort flag
    def stopGame(self):
        for thread in self.robotThreads:
            thread.abort = True
        self.bulletsThread.abort = True

    #temporary method to generate a random valid position to spawn a robot on
    def getRandomValidPosition(self):
        Impassable = True
        while Impassable:
            x = random.randint(1, 959)
            y = random.randint(1, 959)
            Impassable = self.getTileAtPos(x, y).isImpassable
        return x, y
    
    #this function checks iteratively whether a robot has line of sight to the player
    #this function has cornercases where there's an impassable tile between the players centre and the robots centre
    #this 'fuzziness' is intentional, to make it seem like the player can be seen if only a part of the robot shows behind a corner
    def hasLineOfSightToPoint(self, r_x: int, r_y: int, p_x: int, p_y: int) -> bool:
        #stepsize of iterative check
        stepsize = 10
        #y = mx + c
        #we add 0.0001 to prevent a divide by zero error with a negligible margin of error
        m = (r_y - p_y)/((r_x - p_x) + 0.0001)
        #c = y - mx
        c = r_y - m*r_x
        #calculating the number of required steps to traverse the line from (r_x, r_y) to (p_x, p_y)
        length = np.sqrt((p_x - r_x)**2 + (p_y - r_y)**2)
        num_x_iteration = length/stepsize
        x_stepsize = (max(p_x, r_x) - min(p_x, r_x))/num_x_iteration
        #pick the smaller x value and traverse to the larger x value
        x = min(p_x, r_x)
        while x < max(p_x, r_x):
            if self.getTileAtPos(x, m*x + c).isImpassable:
                return False
            else:
                x = x + x_stepsize
        return True
    
    def hasLineOfSightToPlayer(self, r_x: int, r_y: int) -> bool:
        return self.hasLineOfSightToPoint(r_x, r_y, *self.getPlayerPosition())
    
    def hasLineOfSightToPlayerTarget(self, r_x: int, r_y: int) -> bool:
        return self.hasLineOfSightToPoint(r_x, r_y, *self.getPlayerTarget())

    def distanceToPlayer(self, r_x: int, r_y: int) -> float:
        p_x, p_y = self.getPlayerPosition()
        return np.sqrt((p_x - r_x)**2 + (p_y - r_y)**2)

        
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
            self.drawHealthBars(painter, robot)

        self.drawPlayerTarget(painter)

        # Draw bullets
        for bullet in self.bulletsThread.getBullets():
            self.drawBullet(painter, bullet)

    # paint a single tile
    def drawTile(self, painter : QPainter, x : int, y : int, tile : tiles.Tile):
        painter.drawImage(x, y, tile.texture)
    
    def drawPlayerTarget(self, painter: QPainter):
        target = QPointF(self.pawns[0].target_x, self.pawns[0].target_y)
        painter.setBrush(QColor(0xF5F000))
        painter.drawEllipse(target, 5, 5)

    #this method is responsible for painting the robot in the window
    def drawRobot(self, painter : QPainter, robot : Robot):
        #corrects the position of the robot to the upper left corner where the drawing is positioned
        centerRobot = QPointF(robot.xpos - robot.radius, robot.ypos - robot.radius)
        #translate origin of the coordinate system to the center of the robot
        painter.translate(centerRobot)
        #rotate by alpha + offset
        painter.rotate(-robot.alpha*180/np.pi + 90)
        painter.drawImage(-30, -30, robot.image)
        #reset the transformation matrices
        painter.resetTransform()
        #for debugging purposes
        #painter.drawEllipse(centerRobot, robot.radius, robot.radius)

    # draw the healthbars of the robots based on their current health    
    def drawHealthBars(self, painter: QPainter, robot: Robot):
        barWidth  = 60
        barHeight = 4
        barMargin = 5
       
        x = int(robot.xpos - 60)
        y = int(robot.ypos - barMargin - 60)

        # Background
        painter.setBrush(QBrush(Qt.lightGray))
        painter.drawRect(x, y, barWidth, barHeight)

        # Health
        healthWidth = int(barWidth * max(0, robot.health / robot.maxHealth)) # health cannot go below 0
        healthColor = QColor(0, 255, 0)  # Green
        painter.setBrush(QBrush(healthColor))
        painter.drawRect(x, y, healthWidth, barHeight)

        # Border
        painter.setPen(Qt.black)
        painter.setBrush(Qt.NoBrush)
        painter.drawRect(x, y, barWidth, barHeight)

    def drawBullet(self, painter, bullet):
        painter.setBrush(Qt.black)
        painter.drawEllipse(QPointF(bullet.x, bullet.y), bullet.radius, bullet.radius)

    #these functions log press and release events into a dictionary
    def logKeyPressEvent(self, event):
        if self.PressedKeys.__contains__(event.key()):
            self.PressedKeys[event.key()] = True
            self.passKeyEvents(self.PressedKeys)
              
    def logKeyReleaseEvent(self, event):
        if self.PressedKeys.__contains__(event.key()):
            self.PressedKeys[event.key()] = False
            self.passKeyEvents(self.PressedKeys)

    #these functions pass the dictionary of key events and the relevant mouse events along to the threads
    def passKeyEvents(self, eventDict):
        for thread in self.robotThreads:
            thread.processKeyEvent(eventDict)

    def passMouseEvents(self, event: QMouseEvent):
        for key in self.pressedMouseButtons.keys():
            self.pressedMouseButtons[key] = event.buttons() & key
        self.robotThreads[0].processMouseEvent(event.x(), event.y(), self.pressedMouseButtons)
    
    #this function translates a position on the map to the respective tile
    def getTileAtPos(self, x, y) -> tiles.Tile:
        x = (x//Arena.TileWidth)
        y = (y//Arena.TileHeight)
        if x < 0:
            x = 0
        if x >= Arena.ArenaWidth:
            x = Arena.ArenaWidth - 1
        if y < 0:
            y = 0
        if y >= Arena.ArenaHeight:
            y = Arena.ArenaHeight - 1
        return self.ArenaLayout[int(y), int(x)]
    
    def chooseMap(self):
        if self.arena_number == 1:
            self.arena_map = "maps/castlelayout.txt"
        elif self.arena_number == 2:
            self.arena_map = "maps/weapontestlayout.txt"
        elif self.arena_number == 3:
            self.arena_map = "maps/bunkermap.txt"
        else:
            self.arena_map = "maps/testlayout.txt"

    #sets/unsets the flags responsible for pausing the threads
    def unpause(self):
        for thread in self.robotThreads:
            thread.unpauseRobots()
        self.bulletsThread.unpauseBullets()

    def pause(self):
        for thread in self.robotThreads:
            thread.pauseRobots()
        self.bulletsThread.pauseBullets()

def main():
    app = QApplication(sys.argv)
    roboArena = RoboArena() 
    roboArena.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()   