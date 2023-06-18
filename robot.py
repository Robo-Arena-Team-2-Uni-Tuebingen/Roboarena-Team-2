import numpy as np
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QColor


class Robot():

    #the size of the robot in px
    radius = 30
    #maximum accelerations

    a           = 0
    a_alpha     = 0
    A_max       = 100
    A_alpha_max = 100
    v           = 2
    v_alpha     = 0
    #effects
    appliedEffects = {
        "Slow": 0,
        "Freeze": 0,
        "Corrosion": 0,
        "Collateral": 0,
        "Speedup": 0,
    }
    canApply = True
    canRemove = True

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
        c_x = self.xpos-self.radius
        c_y = self.ypos-self.radius
        self.alpha = -np.arctan2(y - c_y, x - c_x) 
        print(self.alpha)

    def applyEffect(self, effect: tuple[str, int]):
        if self.appliedEffects[effect._1] < 100:
            self.appliedEffects[effect._1] += effect._2
            self.canApply = False
            QTimer.singleShot(10000, self.setCanApplyToTrue)

    def setCanApplyToTrue(self):
        self.canApply = True

    def tickDownEffects(self):
        if self.canRemove:
            for effect in self.appliedEffects.values:
                if effect > 0:
                    effect = effect - 5
            self.canRemove = False
            QTimer.singleShot(1000, self.setCanRemoveToTrue)

    def setCanRemoveToTrue(self):
        self.canRemove = True

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
