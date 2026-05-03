import torch

from .sensor_actuator.sensors import readSensors, readHeading
from .cell_tracker import CellTracker



def getObservation(distance_sensors: dict, inertial_unit, tracker: CellTracker, dwell_count):
    
    flags = tracker.getLocalVisitedFlags()
    
    dwell  = max(0, dwell_count - 2)
    dwell_feature = min(dwell, 5) / 5.0
    
    distances = readSensors(distance_sensors, "distance")
    headings = readHeading(inertial_unit)
    
    return torch.tensor(flags+[dwell_feature]+distances+headings, dtype=torch.float32)

# dwell_steps refers to n steps taken in a cell past 2 steps (think about the reason)
def getReward(cell_status, collision=0, dwell_steps=0, is_revealed=0, escape_mode = False):
    match cell_status:
        case CellTracker.CELL_UNVISITED:
            c_status = 1.0

        case CellTracker.CELL_VISITED:
            c_status = -0.1 if not escape_mode else 0

        case CellTracker.CELL_SAME:
            c_status = 0.0
            
    dwell_penalty = 0.2
    target_bonus = 10

    return c_status - collision - (dwell_steps * dwell_penalty) + (is_revealed * target_bonus)
        