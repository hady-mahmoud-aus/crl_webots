import torch

from .sensors import readSensors, readHeading
from .cell_tracker import CellTracker



def getObservation(distance_sensors: dict, inertial_unit, tracker: CellTracker):
    distances = readSensors(distance_sensors, "distance")
    headings = readHeading(inertial_unit)
    flags = tracker.getLocalVisitedFlags()
    
    return torch.tensor(distances+headings+flags, dtype=torch.float32)

# dwell_steps refers to n steps taken in a cell past 2 steps (think about the reason)
def getReward(cell_status, collision=0, dwell_steps=0, is_revealed=0):
    match cell_status:
        case CellTracker.CELL_UNVISITED:
            c_status = 1.0

        case CellTracker.CELL_VISITED:
            c_status = -0.1

        case CellTracker.CELL_SAME:
            c_status = 0.0

    return c_status - collision - (dwell_steps * 0.1) + (is_revealed * 10)
        