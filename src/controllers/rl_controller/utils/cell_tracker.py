from math import ceil, floor

from .sensors import readGPS, readHeading

# CONSTANTS
#########################

cell_size = 0.1
origin = (0, 0)  # [x, y] | fixed for now

#########################


class CellTracker:
    CELL_SAME = 'same'
    CELL_UNVISITED = 'unvisited'
    CELL_VISITED = 'visited'

    def __init__(self, gps, inertial_unit):
        self.gps = gps
        self.inertial_unit = inertial_unit

        self.origin = origin
        self.current_cell = (0, 0)
        self.visited_cells = {self.current_cell}

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

        self.current_cell = index

        if index not in self.visited_cells:
            self.visited_cells.add(index)
            return self.CELL_UNVISITED

        return self.CELL_VISITED

    def getLocalVisitedFlags(self, verbose=False):
        heading = readHeading(self.inertial_unit)

        sin_theta = heading[0]
        cos_theta = heading[1]

        i, j = self.current_cell

        def sign(value):
            if value >= 0:
                return 1
            return -1

        if abs(cos_theta) > abs(sin_theta):
            dx = sign(cos_theta)
            dy = 0
        else:
            dx = 0
            dy = sign(sin_theta)

        front = (i + dx, j + dy)
        right = (i + dy, j - dx)
        left = (i - dy, j + dx)
        back = (i - dx, j - dy)
        
        front = int(front in self.visited_cells)
        right = int(right in self.visited_cells)
        left = int(left in self.visited_cells)
        back = int(back in self.visited_cells)
        

        if not verbose: return[front, right, left, back]
        
        return {
            "front": front,
            "right": right,
            "left": left,
            "back": back,
        }

    def getCoverage(self):
        return len(self.visited_cells)

    def reset(self):
        self.current_cell = (0, 0)
        self.visited_cells = {self.current_cell}