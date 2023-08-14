import numpy as np
import time
import bullets
import behaviour
import random
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
    acceleration    = 1
    speed_max       = 10
    speed           = 3
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

    def __init__(self, xpos, ypos, alpha, player_number, type):

        self.player_number  = player_number
        self.xpos       = xpos
        self.ypos       = ypos
        #angle the robot in degrees
        self.alpha      = alpha - 180
        self.type       = type
        #high health/slow speed/patroller
        if type == 'heavy_gunner':
            self.speed = 0.5
            self.health = 75
            self.radius = 25
            self.image = heavy_gunner
            self.weapon = bullets.MachineGun()
            self.behaviour : behaviour.Behaviour = behaviour.Patrolling(xpos, ypos)
            self.points = 75 + random.randint(-10, 10)
        #high health/no speed/stationary gunner
        elif type == 'cannoneer':
            self.speed = 0
            self.health = 75
            self.radius = 25
            self.image = cannoneer
            self.weapon = bullets.Cannon()
            self.behaviour : behaviour.Behaviour = behaviour.Stationary(xpos, ypos)
            self.points = 75 + random.randint(-10, 10)
        #normal health/normal speed/chases upon contact
        elif type == 'assault':
            self.speed = 1
            self.health = 50
            self.radius = 20
            self.image = assault
            self.weapon = bullets.AssaultRifle()
            self.behaviour : behaviour.Behaviour = behaviour.Standard(xpos, ypos)
            self.points = 50 + random.randint(-10, 10)
        #low health/high speed/chaser
        elif type == 'scout':
            self.speed = 3
            self.speed_max = 6
            self.acceleration = 1
            self.health = 30
            self.radius = 15
            self.image = scout
            self.weapon = bullets.DualPistols()
            self.behaviour : behaviour.Behaviour = behaviour.Scouting(xpos, ypos)
            self.points = 30 + random.randint(-10, 10)
        #low health/low speed/long range damage dealer
        elif type == 'sniper':
            self.speed = 0.25
            self.health = 20
            self.radius = 15
            self.image = sniper
            self.weapon = bullets.SniperRifle()
            self.behaviour : behaviour.Behaviour = behaviour.Sniping(xpos, ypos)
            self.points = 20 + random.randint(-10, 10)

        elif type == 'player':
            self.image = player
            self.weapon = bullets.DualPistols()

    #handles basic decision making for target, alpha, acceleration, deceleration and reloading 
    def behave(self, hasLineOfSight: bool, hasLineOfSightToTarget: bool, ppos: (int, int), pTarget: (int, int)) -> None:
        pos = (self.xpos, self.ypos)
        x, y = ppos
        a, b = pTarget
        distanceToPlayer = np.sqrt((self.xpos - x)**2 + (self.ypos - y)**2)
        distanceToTarget = np.sqrt((self.xpos - a)**2 + (self.ypos - b)**2)

        #sets the angle to a random point or the players centre when aware of the player
        angle = self.behaviour.getAngle(ppos, hasLineOfSight, distanceToPlayer)
        if not isinstance(angle, bool):
            self.getAlpha(*angle)
        
        #checks whether the behaviour is scouting or not to pass the proper parameter
        if isinstance(self.behaviour, behaviour.Scouting):
            newTarget = self.behaviour.getNewTarget(pos, pTarget, distanceToPlayer, hasLineOfSightToTarget)
        else:
            newTarget = self.behaviour.getNewTarget(pos, ppos, distanceToPlayer, hasLineOfSight)
        if not isinstance(newTarget, bool):
            self.target_x, self.target_y = newTarget
        
        #checks conditions for acceleration/deceleration
        if self.behaviour.accelerate(self.speed, distanceToTarget, hasLineOfSightToTarget):
            self.accelerate()
        if self.behaviour.decelerate(self.speed, distanceToTarget, hasLineOfSightToTarget):
            self.decelerate()

        #reload the weapon if conditions are fulfilled
        if self.behaviour.reload(self.weapon.getAmmoLeft()):
            self.weapon.reload()
    
    #decide whether the robot should open fire
    def openFire(self, hasLineOfSight: bool, ppos: (int, int)) -> bool:
        x, y = ppos
        distanceToPlayer = np.sqrt((self.xpos - x)**2 + (self.ypos - y)**2)
        return self.behaviour.openFire(hasLineOfSight, distanceToPlayer)
    
    #this function returns the target of the robot
    def getTarget(self):
        return self.target_x, self.target_y

    #this function is supposed to get the angle from the robot to acceleration specific point relative to the x-axis
    def getAlpha(self, x, y):
        c_x = self.xpos-self.radius
        c_y = self.ypos-self.radius
        self.alpha = -np.arctan2(y - c_y, x - c_x)

    #apply a status effect to the robot
    def applyEffect(self, effect: tuple[str, int]):
        if self.appliedEffects[effect[0]] < 100 and time.time() > self.cdApplyEffect:
            if self.appliedEffects[effect[0]] + effect[1] > 100:
                self.appliedEffects[effect[0]] = 100
            else:
                self.appliedEffects[effect[0]] = self.appliedEffects[effect[0]] + effect[1]
            self.cdApplyEffect = time.time() + self.delayApplyEffect

    #time status effects down
    def tickDownEffects(self):
        if time.time() > self.cdRemoveEffect:
            for key in self.appliedEffects:
                if self.appliedEffects[key] > 0:
                    if self.appliedEffects[key] - 10 < 0:
                        self.appliedEffects[key] = 0
                    else:
                        self.appliedEffects[key] = self.appliedEffects[key] - 10
            self.cdRemoveEffect = time.time() + self.delayRemoveEffect
    
    #speed the robot up
    def accelerate(self):
        if self.speed + self.acceleration <= self.speed_max and time.time() > self.cdAccelerate:
            self.speed += self.acceleration
            self.cdAccelerate = time.time() + self.delayAccelerate

    #slow the robot down
    def decelerate(self):
        if self.speed - self.acceleration >= 0 and time.time() > self.cdDeccelerate:
            self.speed -= self.acceleration
            self.cdDeccelerate = time.time() + self.delayDeccelerate

    #applies up to 50% Slow/Speedup based on the stack count of "Slow"
    def getV(self):
        return self.speed*(200 - self.appliedEffects['Slow'] + self.appliedEffects['Speedup'])/200

    #checks whether a bullet hits the robot or not
    def collidesWithBullet(self, bullet : bullets.Bullet) -> bool:
        distance_squared: float = (bullet.xpos - self.xpos)**2 + (bullet.ypos - self.ypos)**2
        return distance_squared <= (self.radius + bullet.radius)**2

    #applies up to 50% extra damage based on the stack count of "Corrosion"
    def applyDamage(self, damage):
        if time.time() > self.cdDamage:
            self.health = self.health - (damage * (200 - self.appliedEffects['Corrosion'])/200)
            self.cdDamage = time.time() + self.delayDamage
            if self.health <= 0:
                self.is_dead = True

    #unused currently, but implemented for later use with item pickups
    def applyHealing(self, healing):
        if time.time() > self.cdHealing:
            if self.health + healing <= 100:
                self.health = self.health + healing
            else:
               self.health = 100
            self.cdHealing = time.time() + self.delayHealing
    
    #'revives' the player and adds a 3 second invulnerability
    def revive(self):
        self.health = 100
        self.is_dead = False
        self.cdDamage = time.time() + 3

    #handles the firing of a bullet and the associated offsets for player and enemy models, so that bullets may spawn at the correct location of the model
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