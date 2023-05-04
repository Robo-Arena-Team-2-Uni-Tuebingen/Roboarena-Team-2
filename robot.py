import numpy as np

class Robot():

    radius = 30

    def __init__(self, xpos, ypos, alpha):
        
        self.xpos = xpos
        self.ypos = ypos
        self.alpha = alpha - 180

    def update(newxpos, newypos):
        xpos = newxpos
        ypos = newypos

    def getAlpha(self, x, y):
        alpha = np.arctan(x - self.xpos, y - self.ypos) * 180 / np.pi