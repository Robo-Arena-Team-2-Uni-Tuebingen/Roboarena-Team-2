import numpy as np

class Bullet:
    def __init__(self, x, y, angle, radius, speed):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = 5
        self.radius = 2

    def move(self):
        dx = self.speed * np.cos(self.angle)
        dy = -self.speed * np.sin(self.angle)
        self.x += dx
        self.y += dy
