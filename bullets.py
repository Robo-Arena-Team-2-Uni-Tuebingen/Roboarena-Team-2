import numpy as np

class Bullet:
    def __init__(self, x, y, angle, radius, speed):
        x = x
        y = y
        angle = angle
        speed = 5
        radius = 2

    def move(self):
        dx = self.speed * np.cos(self.angle)
        dy = -self.speed * np.sin(self.angle)
        self.x += dx
        self.y += dy
