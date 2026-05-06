import torch

from .misc.sensors import readSensors, readHeading
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


# dwell_steps refers to n steps taken in a cell past 2 steps
def getReward(target_manager: TargetManager, cell_status, collision, dwell_steps,
            loop_score, previous_distance, escape_mode=False, homing=False):
    if homing:
        return homingReward(
            target_manager=target_manager,
            collision=collision,
            previous_distance=previous_distance,
            dwell_steps=dwell_steps
        )

    return searchReward(
        target_manager=target_manager,
        cell_status=cell_status,
        collision=collision,
        dwell_steps=dwell_steps,
        loop_score=loop_score,
        escape_mode=escape_mode
    )


def searchReward(target_manager: TargetManager, cell_status, collision, dwell_steps,
                loop_score, escape_mode=False):
    match cell_status:
        case CellTracker.CELL_UNVISITED:
            c_status = 1.0

        case CellTracker.CELL_VISITED:
            c_status = 0.0 if escape_mode else -0.1

        case CellTracker.CELL_RECENT:
            c_status = -0.1

        case CellTracker.CELL_SAME:
            c_status = 0.0

    # On collision, make reward about collision only, not cell status/dwell/loop
    if collision:
        c_status = 0.0

    is_revealed = int(target_manager.isRevealed())

    collision_penalty = 2.0
    dwell_penalty = 0.2 if not collision else 0.0

    loop_penalty = (
        0.5
        if (not collision and cell_status != CellTracker.CELL_UNVISITED)
        else 0.0
    )

    reveal_bonus = 10.0

    reward = (
        c_status
        - (collision * collision_penalty)
        - (dwell_steps * dwell_penalty)
        - (loop_score * loop_penalty)
        + (is_revealed * reveal_bonus)
    )

    return reward, 0.0


def homingReward(target_manager: TargetManager, collision, previous_distance, dwell_steps):
    distance = target_manager.getDistance()
    progress = previous_distance - distance

    is_reached = int(target_manager.isReached())

    collision_penalty = 3.0
    progress_bonus = 5.0
    reach_bonus = 10.0
    step_penalty = 0.02
    dwell_penalty = 0.5 if not collision else 0.0

    reward = (
        - step_penalty
        - (collision * collision_penalty)
        - (dwell_steps * dwell_penalty)
        + (progress * progress_bonus)
        + (is_reached * reach_bonus)
    )

    return reward, distance

