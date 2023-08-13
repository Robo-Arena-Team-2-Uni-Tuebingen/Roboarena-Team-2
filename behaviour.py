import random
import time
import numpy as np

class Behaviour():
    distance_threshold = 0          #needs to be defined for each behaviour, threshold to follow the player
    minimum_distance = 60            #minimum distance kept to prevent clipping into the player
    fire_threshold = 0              #needs to be defined for each behaviour, threshold to open fire at the player
    awareness_threshold = 0         #needs to be defined for each behaviour, threshold to be aware of the player
    awareness_distance = 0          #needs to be defined for each behaviour, threshold for random awareness
    time_until_angle_change = 0     #time until robot can switch to random angle position
    angle_change_cd = 0             #needs to be defined for each behaviour, cooldown for angle change
    time_until_target_change = 0    #time until robot can switch to new movement target
    target_change_cd = 0            #needs to be defined for each behaviour, cooldown for target change
    target = False                  #whether the movement target is related to the player(True) or random(False)
    angle = False                   #whether the angle points towards the player(True) or in a random direction(False)
    reload_threshold = 0            #needs to be defined for each behaviour, threshold in percent for manually reloading the weapon
    time_last_contact = 0           #time since the player was last seen
    initial_x = 0                   #initial coordinates for behaviour relating to them
    initial_y = 0                   #initial coordinates for behaviour relating to them
    lowerbound = 0 + 15             #edge of map + radius of the robot
    upperbound = 960 - 15           #edge of map - radius of the robot


    def __init__(self, initial_x, initial_y) -> None:
        self.initial_x = initial_x
        self.initial_y = initial_y

    #pos: own position, ppos: player position, distance: distance to player, hasLineOfSight: LineOfSight to Player, isDamaged: less than maxhp
    def getNewTarget(self, pos: (int, int), ppos: (int, int), distance: float, hasLineOfSight: bool):
        pass

    #fire is opened once the player is close enough and the robot has a line of sight
    def openFire(self, hasLineOfSight: bool, distance: float) -> bool:
        if distance < self.fire_threshold and hasLineOfSight and self.angle:
            return True
        else:
            return False
            
    #determines whether to look towards the player or to a random point in the vicinity
    def getAngle(self, pos: (int, int), hasLineOfSight: bool, distance: float):
        x, y = pos
        cur_time = time.time()
        if distance < self.awareness_threshold and hasLineOfSight:
                self.time_last_contact = cur_time
                self.angle = True
                return pos
        elif self.time_until_angle_change < cur_time:
            self.time_until_angle_change = cur_time + self.angle_change_cd
            self.angle = False
            return self.generateRandomPoint(x, y, self.awareness_distance)
        return False
    
    #generates a random point within the boundaries of the arena, the point is not guaranteed to be reachable, upperbound and lowerbound need to be changed for changing map sizes
    def generateRandomPoint(self, x, y, z):
        new_x = min(self.upperbound, max(self.lowerbound, random.randint(int(x - z), int(x + z))))
        new_y = random.randint(int(y - z), int(y + z))
        return (new_x, new_y)

    #should the robot accelerate (only used for scout)
    def accelerate(self, speed: int, distance: float, hasLineOfSight: bool) -> bool:
        return False
    
    #should the robot decelerate (only used for scout)
    def decelerate(self, speed: int, distance: float, hasLineOfSight: bool) -> bool:
        return False

    #reloads the weapon if the reload threshold is larger than the ammo left in the weapon (in percent) and if the robot does not aim at the player
    def reload(self, ammo_left: float) -> bool:
        if self.reload_threshold > ammo_left and not self.angle:
            return True
        else: False

    #was intended to be used to switch behaviours but this will remain unimplemented
    def getTimeLastContact(self) -> None:
        return self.time_last_contact
    
    #for debugging purposes
    def getDistanceThreshold(self) -> int:
        return self.distance_threshold
    
    #for debugging purposes
    def getFireThreshold(self) -> int:
        return self.fire_threshold
    
    #for debugging purposes
    def getAwarenessThreshold(self) -> int:
        return self.awareness_threshold

#standard enemy, randomly walks the map until the player comes to close
class Standard(Behaviour):
    distance_threshold = 400
    fire_threshold = 250
    awareness_threshold = 400
    awareness_distance = 200
    angle_change_cd = 0.06
    target_change_cd = 2
    patrol_radius = 200

    #charges towards the player once it gets close
    def getNewTarget(self, pos: (int, int), ppos: (int, int), distance: float, hasLineOfSight: bool):
        x, y = pos
        cur_time = time.time()
        if self.time_until_target_change < cur_time:
            self.time_until_target_change = cur_time + self.target_change_cd
            if distance < self.distance_threshold and distance > self.minimum_distance and hasLineOfSight:
                self.target = True
                return ppos
            elif distance < self.minimum_distance:
                return pos
            else:
                self.target = False
                return self.generateRandomPoint(x, y, self.patrol_radius)
        return False

#patrols an area around his spawning point randomly, opens fire when the player comes close
class Patrolling(Behaviour):
    distance_threshold = 0
    fire_threshold = 300
    patrol_radius = 100
    awareness_threshold = 400
    awareness_distance = 150
    angle_change_cd = 0.12
    target_change_cd = 5
    reload_threshold = 25

    #new target is chosen independent from the players action
    def getNewTarget(self, pos: (int, int), ppos: (int, int), distance: float, hasLineOfSight: bool):
        cur_time = time.time()
        if self.time_until_target_change < cur_time and distance > self.minimum_distance:
            self.time_until_target_change = cur_time + self.target_change_cd
            x, y = pos
            return self.generateRandomPoint(x, y, self.patrol_radius)
        #hold position if distance is smaller than the minimum distance
        elif distance < self.minimum_distance:
            return pos
        return False

#This enemy is stationary and tries to engage the player at long range at every available chance
class Stationary(Behaviour):
    distance_threshold = 0
    fire_threshold = 500
    awareness_threshold = 600
    awareness_distance = 100
    angle_change_cd = 0.36
    target_change_cd = 0 #Stationary Enemy
    reload_threshold = 0

    def getNewTarget(self, pos: (int, int), ppos: (int, int), distance: float, hasLineOfSight: bool):
        return (self.initial_x, self.initial_y)

#This enemy engages over long distances and stops moving to do so
class Sniping(Behaviour):
    distance_threshold = 100
    fire_threshold = 700
    awareness_threshold = 800
    awareness_distance = 200
    angle_change_cd = 0.72
    target_change_cd = 5
    reload_threshold = 75
    firing = False
    patrol_radius = 50

    #tries to back away when the player comes to close
    def getNewTarget(self, pos: (int, int), ppos: (int, int), distance: float, hasLineOfSight: bool):
        x, y = pos
        cur_time = time.time()
        if self.time_until_target_change < cur_time and not self.firing:
            self.time_until_target_change = cur_time + self.target_change_cd
            if distance < self.distance_threshold and distance > self.minimum_distance and hasLineOfSight:
                self.target = True
                a, b = ppos
                l = np.sqrt((x - a)**2 + (y - b)**2)
                #return a position opposite to the player normed to length 20
                new_x = min(self.upperbound, max(self.lowerbound, -a*20/l))
                new_y = min(self.upperbound, max(self.lowerbound, -b*20/l))
                return (new_x, new_y)
            else:
                self.target = False
                return self.generateRandomPoint(x, y, self.patrol_radius)
        elif self.firing:
            self.time_until_target_change = cur_time + self.target_change_cd
            return pos
        return False
    
    def openFire(self, hasLineOfSight: bool, distance: float) -> bool:
        if distance < self.fire_threshold and hasLineOfSight and self.angle:
            self.firing = True
            return True
        else:
            self.firing = False
            return False

#This enemy is supposed to scout for the player and tries to intercept the player at the players target
class Scouting(Behaviour):
    distance_threshold = 1000
    fire_threshold = 80
    awareness_threshold = 300
    awareness_distance = 200
    angle_change_cd = 0.03
    target_change_cd = 1
    reload_threshold = 25
    accelerate = False
    decelerate = False

    #enemy is supposed to traverse the map at random and lock onto the player once line of sight is established
    def getNewTarget(self, pos: (int, int), ppos: (int, int), distance: float, hasLineOfSight: bool):
        x, y = pos
        a, b = ppos
        distanceToTarget = distance = np.sqrt((a - x)**2 + (b - y)**2)
        cur_time = time.time()
        if self.time_until_target_change < cur_time:
            self.time_until_target_change = cur_time + self.target_change_cd
            if distanceToTarget < self.distance_threshold and distance > self.minimum_distance and hasLineOfSight:
                self.target = True
                return ppos
            elif distance < self.minimum_distance:
                return pos
            else:
                rand = random.randint(0, 20)
                self.target = False
                return self.generateRandomPoint(x, y, rand)
        else:
            return False

    #speed the robot up depending on how close it is
    def accelerate(self, speed: int, distance: float, hasLineOfSight: bool) -> bool:
        accThreshold1Speed = 4
        accThreshold2Speed = 5
        accThreshold3Speed = 6
        accThreshold1Dist = 400
        accThreshold2Dist = 300
        accThreshold3Dist = 200

        if hasLineOfSight:
            if speed <= accThreshold1Speed and distance < accThreshold1Dist:
                return True
            elif speed <= accThreshold2Speed and distance < accThreshold2Dist:
                return True
            elif speed <= accThreshold3Speed and distance < accThreshold3Dist:
                return True
        return False
    
    def decelerate(self, speed: int, distance: float, hasLineOfSight: bool) -> bool:
        decThreshold1Speed = 4
        decThreshold2Speed = 5
        decThreshold3Speed = 6
        decThreshold1Dist = 450
        decThreshold2Dist = 350
        decThreshold3Dist = 250

        if hasLineOfSight:
            if speed >= decThreshold1Speed and distance > decThreshold1Dist:
                return True
            elif speed >= decThreshold2Speed and distance > decThreshold2Dist:
                return True
            elif speed >= decThreshold3Speed and distance > decThreshold3Dist:
                return True
        return False