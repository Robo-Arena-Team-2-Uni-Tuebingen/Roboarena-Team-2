import numpy as np
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QColor

class Robot():

    #the size of the robot in px
    radius = 30
    #maximum accelerations
    a           = 2     #acceleration
    a_alpha     = 0     #turning acceleration
    A_max       = 10    #Max Speed
    A_alpha_max = 100   #Max Turning Speed
    v           = 2     #Speed
    v_alpha     = 0     #Turning speed
    #temporary
    target_x = 0
    target_y = 0
    targetColor = QColor(0xFFFFFF)

    canAccelerate = True
    canDeccelerate = True

    def __init__(self, xpos, ypos, alpha, color, is_player):

        self.is_player  = is_player
        self.xpos       = xpos
        self.ypos       = ypos
        #angle the robot in degrees
        self.alpha      = alpha - 180
        self.color      = color 

    #this function is supposed to get the angle from the robot to a specific point relative to the x-axis
    def getAlpha(self, x, y):
        alpha = np.arctan(x - self.xpos, y - self.ypos) * 180 / np.pi

    def accelerate(self):
        if self.v + self.a <= self.A_max:
            self.v += self.a
            self.canAccelerate = False
            QTimer.singleShot(1000, self.setCanAccelerateToTrue)

    def deccelerate(self):
        if self.v - self.a >= 0:
            self.v -= self.a
            self.canDeccelerate = False
            QTimer.singleShot(1000, self.setCanDeccelerateToTrue)

    def setCanAccelerateToTrue(self):
        self.canAccelerate = True

    def setCanDeccelerateToTrue(self):
        self.canDeccelerate = True