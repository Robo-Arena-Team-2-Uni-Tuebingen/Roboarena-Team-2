import numpy as np
import time
import bullets
from PyQt5.QtCore import QRect
from PyQt5.QtGui import QColor, QImage

heavy_gunner = QImage('assets/heavy_gunner.png').scaled(60, 60)
cannoneer = QImage('assets/cannoneer.png').scaled(60, 60)
assault = QImage('assets/assault.png').scaled(60, 60)
scout = QImage('assets/scout.png').scaled(60, 60)
sniper = QImage('assets/sniper.png').scaled(60, 60)
player = QImage('assets/tech.png').scaled(60, 60)

class Robot():

    #the size of the robot in px
    radius = 30
    #maximum accelerations
    acceleration    = 2
    a_alpha         = 2
    speed_max       = 100
    A_alpha_max     = 100
    speed           = 2
    v_alpha         = 2
    #effects
    appliedEffects = {
        'Slow': 0, #slows the robot
        'Freeze': 0, #makes shots more inaccurate
        'Corrosion': 0, #increases taken damage
        'Collateral': 0, #increases done damage
        'Speedup': 0 #increases speed
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
    #health
    maxHealth = 100
    health = 100
    delayDamage = 0.1
    delayHealing = 1
    cdDamage = time.time() + 3 # 3 second invulnerability after new spawn
    cdHealing = 0
    is_dead = False
    #damage
    weapon = bullets.Weapon()
    points = 100 # temporary, should depend on weapon and behaviour

    def __init__(self, xpos, ypos, alpha, color, player_number, type):

        self.player_number  = player_number
        self.xpos       = xpos
        self.ypos       = ypos
        #angle the robot in degrees
        self.alpha      = alpha - 180
        self.color      = color
        self.type = type
        if type == 'heavy_gunner':
            self.speed = 1
            self.health = 75
            self.radius = 25
            self.image = heavy_gunner
            self.weapon = bullets.MachineGun()
        elif type == 'cannoneer':
            self.speed = 1
            self.health = 75
            self.radius = 25
            self.image = cannoneer
            self.weapon = bullets.Cannon()
        elif type == 'assault':
            self.speed = 2
            self.health = 50
            self.radius = 20
            self.image = assault
            self.weapon = bullets.AssaultRifle()
        elif type == 'scout':
            self.speed = 3
            self.health = 30
            self.radius = 15
            self.image = scout
            self.weapon = bullets.DualPistols()
        elif type == 'sniper':
            self.speed = 1
            self.health = 20
            self.radius = 15
            self.image = sniper
            self.weapon = bullets.SniperRifle()

        elif type == 'player':
            self.image = player
            self.weapon = bullets.DualPistols()
        


    #this function is supposed to get the angle from the robot to acceleration specific point relative to the x-axis
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
        if self.speed + self.acceleration <= self.speed_max and time.time() > self.cdAccelerate:
            self.speed += self.acceleration
            self.cdAccelerate = time.time() + self.delayAccelerate

    def deccelerate(self):
        if self.speed - self.acceleration >= 0 and time.time() > self.cdDeccelerate:
            self.speed -= self.acceleration
            self.cdDeccelerate = time.time() + self.delayDeccelerate

    #applies up to 50% Slow/Speedup based on the stack count of "Slow"
    def getV(self):
        return self.speed*(200 - self.appliedEffects['Slow'] + self.appliedEffects['Speedup'])/200

    def collidesWithBullet(self, bullet):
        distance_squared = (bullet.xpos - self.xpos)**2 + (bullet.ypos - self.ypos)**2
        return distance_squared <= (self.radius + bullet.radius)**2

    def applyDamage(self, damage):
        if time.time() > self.cdDamage:
            self.health = self.health - (damage * (200 - self.appliedEffects['Corrosion'])/200)
            self.cdDamage = time.time() + self.delayDamage
            if self.health <= 0:
                self.is_dead = True

    def applyHealing(self, healing):
        if time.time() > self.cdHealing:
            if self.health + healing <= 100:
                self.health = self.health + healing
            else:
               self.health = 100
            self.cdHealing = time.time() + self.delayHealing

    def shoot(self):
        offset_radius = 0
        offset_angle = 0
        if self.type == 'player':
            offset_radius = 2
            offset_angle = -0.55
        if self.type == 'sniper':
            offset_radius = 4
            offset_angle = -0.45
        if self.type == 'scout':
            offset_radius = 2
            offset_angle = 0.3
        if self.type == 'heavy_gunner':
            offset_radius = 2
            offset_angle = -0.15
        if self.type == 'assault':
            offset_radius = 2
            offset_angle = 0.15
        return self.weapon.shoot(self.xpos, self.ypos, self.radius, offset_radius, offset_angle, self.alpha, self.speed)
    
    def isRobotDead(self):
        return self.is_dead