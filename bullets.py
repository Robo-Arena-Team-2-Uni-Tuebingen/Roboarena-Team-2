import typing
import numpy as np
import time
from PyQt5.QtCore import QObject, QThread

class Bullet:
    def __init__(self, x, y, angle, radius, speed, damage):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = speed
        self.radius = radius
        self.damage = damage

    def move(self):
        dx = self.speed * np.cos(self.angle)
        dy = -self.speed * np.sin(self.angle)
        self.x += dx
        self.y += dy

class BulletThread(QThread):
    is_paused = False
    bullets: list[Bullet] = []

    def __init__(self, arena) -> None:
        super().__init__()
        self.arena = arena
        self.pawns = self.arena.pawns

    def run(self) -> None:
        while True:
            if not self.is_paused:
                for bullet in self.bullets.copy():
                    bullet.move()
                    if not self.isBulletInsideArena(bullet) or self.isTileImpassable(bullet):
                            self.bullets.remove(bullet)
                            continue
                    for pawn in self.pawns:
                        if self.checkBulletCollision(pawn, bullet):
                            self.bullets.remove(bullet)
                            pawn.applyDamage(bullet.damage)
                            break
            self.msleep(30)
    
    def unpauseBullets(self):
        self.is_paused = False

    def pauseBullets(self):
        self.is_paused = True
    
    def addBullet(self, bullet: Bullet):
        self.bullets.append(bullet)

    def removeBullet(self, bullet: Bullet):
        self.bullets.remove(bullet)

    def checkBulletCollision(self, robot, bullet):
        distance_squared = (robot.xpos - bullet.x - robot.radius)**2 + (robot.ypos - bullet.y - robot.radius)**2
        return distance_squared <= (robot.radius + bullet.radius)**2
    
    def isBulletInsideArena(self, bullet):
        return 0 <= bullet.x <= self.arena.ArenaWidth * self.arena.TileWidth and 0 <= bullet.y <= self.arena.ArenaHeight * self.arena.TileHeight
    
    def isTileImpassable(self, bullet):
        return self.arena.getTileAtPos(bullet.x, bullet.y).isImpassable
    
    def getBullets(self):
        return self.bullets

#abstract weapon class
class Weapon:
    def __init__(self) -> None:
        self.type = 'projectile'    #attribute to indicate the type of projectile in case of further expansion
        self.damage = 5             #damage of one projectile
        self.radius = 2             #size of one projectile
        self.speed = 5              #speed of one projectile
        self.cycle = 0.05           #how fast projectiles can be fired (here one per 50ms)
        self.cdcycle = 0            #cooldown on the cycle time
        self.mag = 10               #magazine capacity
        self.magMax = 10            #maximum magazine capacity
        self.reload = 2             #how fast the magazine can be reloaded (here 2 seconds)
        self.cdreload = 0           #cooldown on the reload time

    def shoot(self, x, y, radius, alpha):
        t = time.time()
        if self.cdreload < t and self.cdcycle < t:
            if self.mag > 0:
                bullet_radius = self.radius
                bullet_speed = self.speed
                bullet_x = (x - radius) + radius*np.cos(-alpha) 
                bullet_y = (y - radius) + radius*np.sin(-alpha)
                bullet = Bullet(bullet_x, bullet_y, alpha, bullet_radius, bullet_speed, self.damage)
                self.mag = self.mag - 1
                self.cdcycle = t + self.cycle
                return True, bullet
            else:
                self.mag = self.magMax
                self.cdreload = t + self.reload
        return False, 0