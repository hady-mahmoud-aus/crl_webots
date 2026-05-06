from math import ceil, floor
from collections import deque

from .misc.sensors import readGPS, readHeading

# CONSTANTS
#########################

cell_size = 0.1
origin = (0, -0.9)  # [x, y] | fixed for now

#########################

# for escaping small loops
loop_window_length = 4

class CellTracker:
    CELL_SAME = 'same'
    CELL_RECENT = 'recent'
    CELL_UNVISITED = 'unvisited'
    CELL_VISITED = 'visited'

    def __init__(self, gps, inertial_unit):
        self.gps = gps
        self.inertial_unit = inertial_unit

        self.origin = origin
        self.current_cell = (0, 0)
        
        self.visited_cells = {self.current_cell}
        self.blocked_cells = set()
        
        self.recent_cells = deque(maxlen=loop_window_length)
        self.recent_cells.append(self.current_cell)

    def roundToNearestCell(self, value):
        if value >= 0:
            return int(floor(value + 0.5))
        else:
            return int(ceil(value - 0.5))

    def gpsToCell(self):
        x, y = readGPS(self.gps)

        dx = x - self.origin[0]
        dy = y - self.origin[1]

        i = self.roundToNearestCell(dx / cell_size)
        j = self.roundToNearestCell(dy / cell_size)

        return (i, j)

    def checkCell(self) -> str:
        index = self.gpsToCell()
        
        if index == self.current_cell:
            return self.CELL_SAME
        
        was_recent = index in self.recent_cells
        self.recent_cells.append(index)
        
        self.current_cell = index

        if index not in self.visited_cells:
            self.visited_cells.add(index)
            return self.CELL_UNVISITED

        if was_recent:
            return self.CELL_RECENT
        
        return self.CELL_VISITED

    def getLocalVisitedFlags(self, verbose=False):
        
        i, j = self.current_cell
        dx, dy = self.getDiscreteHeading()

        front = (i + dx, j + dy)
        right = (i + dy, j - dx)
        left = (i - dy, j + dx)
        back = (i - dx, j - dy)
        
        front = int((front in self.visited_cells) or (front in self.blocked_cells))
        right = int((right in self.visited_cells) or (right in self.blocked_cells))
        left = int((left in self.visited_cells) or (left in self.blocked_cells))
        back = int((back in self.visited_cells) or (back in self.blocked_cells))
        

        if not verbose: return[front, right, left, back]
        
        return {
            "front": front,
            "right": right,
            "left": left,
            "back": back,
        }
        
    # if robot is stuck in a closed loop of cells; high score -> worse
    def getLoopScore(self):
        n_unique = len(set(self.recent_cells)) 
        return 1 - (n_unique / len(self.recent_cells)) 
    
    def blockForward(self):
        i, j = self.current_cell
        dx, dy = self.getDiscreteHeading()
        
        front = (i + dx, j + dy)
        
        self.blocked_cells.add(front)
        

    def getCoverage(self):
        return len(self.visited_cells)

    def reset(self):
        self.current_cell = (0, 0)
        self.visited_cells = {self.current_cell}
        self.blocked_cells.clear()
        
        self.recent_cells.clear()
        self.recent_cells.append(self.current_cell)
        
    def getDiscreteHeading(self):
        
        def sign(value):
            if value >= 0:
                return 1
            return -1
        
        heading = readHeading(self.inertial_unit)

        sin_theta = heading[0]
        cos_theta = heading[1]

        if abs(cos_theta) > abs(sin_theta):
            dx = sign(cos_theta)
            dy = 0
        else:
            dx = 0
            dy = sign(sin_theta)
            
        return (dx, dy)
        
