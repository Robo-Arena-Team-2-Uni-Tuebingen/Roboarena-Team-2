import numpy as np

class Robot():

    #the size of the robot in px
    radius = 30

    def __init__(self, xpos, ypos, alpha):
        
        self.xpos = xpos
        self.ypos = ypos
        #angle the robot in degrees
        self.alpha = alpha - 180

    #updates the position of the robot
    def update(newxpos, newypos):
        xpos = newxpos
        ypos = newypos

    #this function is supposed to get the angle from the robot to a specific point relative to the x-axis
    def getAlpha(self, x, y):
        alpha = np.arctan(x - self.xpos, y - self.ypos) * 180 / np.pi