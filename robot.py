import numpy as np
import time
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QColor



class Robot():

    #the size of the robot in px
    radius = 30
    #maximum accelerations

    a           = 2
    a_alpha     = 2
    A_max       = 100
    A_alpha_max = 100
    v           = 2
    v_alpha     = 2
    #effects
    appliedEffects = {
        'Slow': 0,
        'Freeze': 0,
        'Corrosion': 0,
        'Collateral': 0,
        'Speedup': 0
    }
    #temporary
    target_x = 0
    target_y = 0
    targetColor = QColor(0xFFFFFF)
    delayApplyEffect = 10
    delayRemoveEffect = 5
    delayAccelerate = 1
    delayDeccelerate = 1
    cdApplyEffect = 0
    cdRemoveEffect = 0
    cdAccelerate = 0
    cdDeccelerate = 0

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

    def applyEffect(self, effect: tuple[str, int]):
        if self.appliedEffects[effect[0]] < 100 and time.time() > self.cdApplyEffect:
            if self.appliedEffects[effect[0]] + effect[1] > 100:
                self.appliedEffects[effect[0]] = 100
            else:
                self.appliedEffects[effect[0]] = self.appliedEffects[effect[0]] + effect[1]
            self.cdApplyEffect = time.time() + self.delayApplyEffect

    def tickDownEffects(self):
        if time.time() > self.cdRemoveEffect:
            for key in self.appliedEffects:
                if self.appliedEffects[key] > 0:
                    if self.appliedEffects[key] - 10 < 0:
                        self.appliedEffects[key] = 0
                    else:
                        self.appliedEffects[key] = self.appliedEffects[key] - 10
            self.cdRemoveEffect = time.time() + self.delayRemoveEffect

    def accelerate(self):
        if self.v + self.a <= self.A_max and time.time() > self.cdAccelerate:
            self.v += self.a
            self.cdAccelerate = time.time() + self.delayAccelerate

    def deccelerate(self):
        if self.v - self.a >= 0 and time.time() > self.cdDeccelerate:
            self.v -= self.a
            self.cdDeccelerate = time.time() + self.delayDeccelerate

    #applies up to 50% Slow/Speedup based on the stack count of "Slow"
    def getV(self):
        return self.v*(200 - self.appliedEffects['Slow'] + self.appliedEffects['Speedup'])/200
