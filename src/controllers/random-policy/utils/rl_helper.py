import torch

from .sensors import readSensors, readHeading
from .cell_tracker import GridTracker



def getObservation(distance_sensors: dict, inertial_unit, tracker: GridTracker):
    distances = readSensors(distance_sensors, "distance")
    headings = readHeading(inertial_unit)
    flags = tracker.getLocalVisitedFlags()
    
    return torch.tensor(distances+headings+flags, dtype=torch.float32)

# dwell_steps refers to n steps taken in a cell past 2 steps
def getReward(cell_status, collision=0, dwell_steps=0, is_revealed=0):
    match cell_status:
        case GridTracker.CELL_UNVISITED:
            c_status = 1.0

        case GridTracker.CELL_VISITED:
            c_status = -0.1

        case GridTracker.CELL_SAME:
            c_status = 0.0

    return c_status - collision - (dwell_steps * 0.1) + (is_revealed * 10)
        