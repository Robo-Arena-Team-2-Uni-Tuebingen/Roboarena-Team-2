import numpy as np
from PyQt5.QtCore import QTimer

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

    def __init__(self, xpos, ypos, alpha, color):
        
        self.xpos = xpos
        self.ypos = ypos
        #angle the robot in degrees
        self.alpha = alpha - 180
        self.color = color 

    #updates the position of the robot
    def update(self, newxpos, newypos, new_a, new_a_alpha, t):
        self.xpos = newxpos
        self.ypos = newypos
        self.a     = self.a + new_a

        if self.a >= self.A_max:
            self.a = self.A_max

        self.a_alpha = self.a_alpha + new_a_alpha

        if self.a_alpha >= self.A_alpha_max:
            self.a_alpha = self.A_alpha_max
            
        self.v       = self.v + self.a * t
        self.v_alpha = self.v_alpha + self.a_alpha * t

    #this function is supposed to get the angle from the robot to a specific point relative to the x-axis
    def getAlpha(self, x, y):
        alpha = np.arctan(x - self.xpos, y - self.ypos) * 180 / np.pi

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