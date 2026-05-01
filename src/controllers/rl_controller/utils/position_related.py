# Target
#########################

import random
from math import dist, pi, atan2

from .cell_tracker import origin
from .sensors import readGPS, readHeading


arena_size = 1.4;
buffer = arena_size * 0.05

min_distance_from_origin = 0.3

reveal_radius = 0.2
reach_radius = 0.07


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
    
    def getDistance(self):
        position = readGPS(self.gps)
        return dist(position, self.target) 
    
    def isRevealed(self) -> bool:
        return self.getDistance() <= reveal_radius
    
    def isReached(self) -> bool: 
        return self.getDistance() <= reach_radius
    
    def getBearing(self):
        position = readGPS(self.gps)

        dx = self.target[0] - position[0]
        dy = self.target[1] - position[1]

        target_angle = atan2(dy, dx)
        robot_angle = self.inertial_unit.getRollPitchYaw()[2]

        bearing = target_angle - robot_angle

        while bearing > pi:
            bearing -= 2 * pi

        while bearing < -pi:
            bearing += 2 * pi

        return bearing
    
    def __str__(self):
        return f'Target: {self.target}'

#########################


# Episode Position Reset
#########################

from controller import Supervisor

def resetPosition(robot: Supervisor, x=None, y=None):
    node = robot.getSelf()
    
    position = origin if x is None or y is None else [x, y]
    
    translation = node.getField('translation')
    translation.setSFVec3f([*position, 0])
    
    rotation = node.getField('rotation')
    rotation.setSFRotation([0, 0, 1, 0])
    
    node.resetPhysics()

#########################