# Target
#########################

import random
from math import dist

from .sensors import readGPS


arena_size = 2;
buffer = arena_size * 0.05
reveal_radius = 0.2

class TargetManager:
    
    def getTarget(self) -> list:
        limit = (arena_size / 2) - buffer # so target is not on a wall

        number = lambda : round(random.uniform(-limit, limit), 2)
        return [number(), number()]

    def __init__(self, gps):
        self.target = self.getTarget()
        self.gps = gps
        
    def getNewTarget(self):
        self.target = self.getTarget()
        
        return self.target
    
    def isRevealed(self):
        position = readGPS(self.gps)
        
        if dist(position, self.target) <= reveal_radius: return True
        
        return False


#########################


# Episode Position Reset
#########################

from controller import Supervisor
from .cell_tracking import origin

def resetPosition(robot: Supervisor, x=None, y=None):
    node = robot.getSelf()
    
    position = origin if x is None or y is None else [x, y]
    
    translation = node.getField('translation')
    translation.setSFVec3f([*position, 0])
    node.resetPhysics()

#########################