import torch

from .sensor_actuator.sensors import readSensors, readHeading
from .cell_tracker import CellTracker
from .position_related import TargetManager



def getObservation(distance_sensors: dict, inertial_unit, cell_tracker: CellTracker, target_manager: TargetManager, dwell_count, loop_score, homing=False):
    
    flags = cell_tracker.getLocalVisitedFlags()
    
    dwell  = max(0, dwell_count - 2)
    dwell_feature = [min(dwell, 5) / 5.0]
    
    distance_readings = readSensors(distance_sensors, "distance")
    headings = readHeading(inertial_unit)
    
    if homing:
        target_distance = [target_manager.getDistance()]
        bearing = target_manager.getBearing()
    else: target_distance, bearing = [[0.0], [0.0, 0.0]]
    
    observation = flags + dwell_feature + [loop_score] + distance_readings + headings + target_distance + bearing
    
    return torch.tensor(observation, dtype=torch.float32)

# dwell_steps refers to n steps taken in a cell past 2 steps (think about the reason)
def getReward(target_manager: TargetManager, cell_status, collision, dwell_steps, loop_score, previous_distance, escape_mode = False, homing=False):
    match cell_status:
        case CellTracker.CELL_UNVISITED:
            c_status = 1.0

        case CellTracker.CELL_VISITED:
            c_status = -0.1 if not escape_mode else 0.0
            
        case CellTracker.CELL_RECENT:
            c_status = -0.1

        case CellTracker.CELL_SAME:
            c_status = 0.0
            
    c_status = c_status if not collision else 0.0
            
    is_revealed = int(target_manager.isRevealed()) if not homing else 0.0
    is_reached = int(target_manager.isReached())
    
    if homing:
        distance = target_manager.getDistance()
        progress = previous_distance - distance
    else: distance, progress = [0.0, 0.0]
    
    collision_penalty = 1.0      
    dwell_penalty = 0.2 if not collision else 0
    
    loop_penalty = (
        0.5
        if (not collision and cell_status != CellTracker.CELL_UNVISITED)
        else 0.0
    )
    
    reveal_bonus = 10.0
    progress_bonus = 2.0
    reach_bonus = 10.0

    return (
        c_status
        - (collision * collision_penalty)
        - (dwell_steps * dwell_penalty)
        - (loop_score * loop_penalty) 
        + (is_revealed * reveal_bonus)
        + (progress * progress_bonus)
        + (is_reached * reach_bonus)
    ), distance
        