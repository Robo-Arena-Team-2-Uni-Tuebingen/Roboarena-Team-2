import random
import time

class Behaviour():
    distance_threshold = 0          #needs to be defined for each behaviour, threshold to follow the player
    fire_threshold = 0              #needs to be defined for each behaviour, threshold to open fire at the player
    awareness_threshold = 0         #needs to be defined for each behaviour, threshold to be aware of the player
    awareness_distance = 0          #needs to be defined for each behaviour, threshold for random awareness
    time_until_angle_change = 0
    angle_change_cd = 0             #needs to be defined for each behaviour, cooldown for angle change
    time_until_target_change = 0
    target_change_cd = 0            #needs to be defined for each behaviour, cooldown for target change
    target = False                  #whether the movement target is related to the player(True) or random(False)
    angle = False                   #whether the angle points towards the player(True) or in a random direction(False)
    reload_threshold = 0            #needs to be defined for each behaviour, threshold in percent for manually reloading the weapon
    time_last_contact = 0           #time since the player was last seen

    #pos: own position, ppos: player position, distance: distance to player, hasLineOfSight: LineOfSight to Player, isDamaged: less than maxhp
    def getNewTarget(self, pos: (int, int), ppos: (int, int), distance: float, hasLineOfSight: bool, is_Damaged: bool) -> (int, int) | bool:
        pass

    #fire is opened once the player is close enough and the robot has a line of sight
    def openFire(self, hasLineOfSight: bool, distance: float) -> bool:
        if distance < self.fire_threshold and hasLineOfSight and self.angle:
            return True
        else:
            return False
            
    #determines whether to look towards the player or to a random point in the vicinity
    def getAngle(self, pos: (int, int), hasLineOfSight: bool, distance: float) -> (int, int) | bool:
        x, y = pos
        cur_time = time.time()
        if self.time_until_angle_change < cur_time:
            self.time_until_angle_change = cur_time + self.angle_change_cd
            if distance < self.awareness_threshold and hasLineOfSight:
                self.time_last_contact = cur_time
                self.angle = True
                return True
            else:
                self.angle = False
                new_x = random.randint(x - self.awareness_distance, x + self.awareness_distance)
                new_y = random.randint(y - self.awareness_distance, y + self.awareness_distance)
                return (new_x, new_y)
        return False
    
    #should the robot accelerate (only used for scout)
    def accelerate(self) -> bool:
        False
    
    #should the robot decelerate (only used for scout)
    def decelerate(self) -> bool:
        False

    #reloads the weapon if the reload threshold is larger than the ammo left in the weapon (in percent)
    def reload(self, ammo_left: float) -> bool:
        if self.reload_threshold > ammo_left:
            return True
        else: False

    def getTimeLastContact(self) -> None:
        return self.time_last_contact

#standard enemy, randomly walks the map until the player comes to close
class Standard(Behaviour):
    distance_threshold = 200
    fire_threshold = 250
    awareness_threshold = 300
    awareness_distance = 200
    angle_change_cd = 1
    target_change_cd = 2

    #charges towards the player once it gets close
    def getNewTarget(self, pos: (int, int), ppos: (int, int), distance: float, hasLineOfSight: bool, is_Damaged: bool) -> (int, int) | bool:
        x, y = pos
        cur_time = time.time()
        if self.time_until_target_change < cur_time:
            if distance < self.distance_threshold and hasLineOfSight:
                self.target = True
                return True
            else:
                self.target = False
                return ppos
        return False

#patrols an area around his spawning point randomly, opens fire when the player comes close
class Patroller(Behaviour):
    distance_threshold = 0
    fire_threshold = 100
    patrol_radius = 100
    awareness_threshold = 200
    awareness_distance = 150
    angle_change_cd = 3
    target_change_cd = 5
    reload_threshold = 25
    initial_x = 0
    initial_y = 0

    #Patroller is initialized with the initial coordinates of the robot
    def __init__(self, initial_x: int, initial_y: int) -> None:
        super().__init__()
        self.initial_x = initial_x
        self.initial_y = initial_y

    #new target is chosen independent from the players action
    def getNewTarget(self, pos: (int, int), ppos: (int, int), distance: float, hasLineOfSight: bool) -> (int, int) | bool:
        cur_time = time.time()
        if self.time_until_target_change < cur_time:
            self.time_until_target_change = cur_time + self.target_change_cd
            x, y = pos
            new_x = random.randint(x - self.patrol_radius, x + self.patrol_radius)
            new_y = random.randint(y - self.patrol_radius, y + self.patrol_radius)
            return (new_x, new_y)
        return False
    
