# Target
#########################

from controller import Supervisor
import random
from math import dist, sin, cos, atan2

from .cell_tracker import origin
from .misc.sensors import readGPS


arena_size = 2;
buffer = arena_size * 0.05

min_distance_from_origin = 0.6

reveal_radius = 0.35
reach_radius = 0.15


class TargetManager:
    
    def getTarget(self) -> list:
        limit = (arena_size / 2) - buffer  # so target is not on a wall
        number = lambda: round(random.uniform(-limit, limit), 2)

        while True:
            target = [number(), number()]

            if dist(origin, target) >= min_distance_from_origin:
                return target

    def __init__(self, gps, inertial_unit):
        self.target = self.getTarget()
        self.gps = gps
        self.inertial_unit = inertial_unit
        
    def getNewTarget(self):
        self.target = self.getTarget()
        
        return self.target
    
    def getDistance(self, normalized = True): # [0, 1] normalized
        position = readGPS(self.gps)
        
        distance =  dist(position, self.target) 
        
        return min(distance / reveal_radius, 1.0) if normalized else distance
    
    def isRevealed(self) -> bool:
        return self.getDistance(False) <= reveal_radius
    
    def isReached(self) -> bool: 
        return self.getDistance(False) <= reach_radius
    
    def getBearing(self):
        position = readGPS(self.gps)

        dx = self.target[0] - position[0]
        dy = self.target[1] - position[1]

        target_angle = atan2(dy, dx)
        robot_angle = self.inertial_unit.getRollPitchYaw()[2]

        raw_bearing = target_angle - robot_angle

        # wrap to [-pi, pi]
        bearing = atan2(sin(raw_bearing), cos(raw_bearing))

        return [sin(bearing), cos(bearing)]
    
    def __str__(self):
        return f'Target: {self.target}'

#########################


# Episode Position Reset
#########################

def resetPosition(robot: Supervisor, x=None, y=None):
    node = robot.getSelf()
    
    position = origin if x is None or y is None else [x, y]
    
    translation = node.getField('translation')
    translation.setSFVec3f([*position, 0])
    
    rotation = node.getField('rotation')
    rotation.setSFRotation([0, 0, 1, 0])
    
    node.resetPhysics()

#########################