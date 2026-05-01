from random import randint

from controller import Supervisor

from utils.actions import action, actionComplete
from utils.motors import setVelocityAll
from utils.layer_0 import onCollision
from utils.position_related import resetPosition
from utils.cell_tracker import GridTracker
from utils.component_manager import ComponentManager


robot = Supervisor()
timestep = int(robot.getBasicTimeStep())

# SENSOR / ACTUATOR INITIALIZATION
#########################

component_manager = ComponentManager(
    robot, timestep, 
    distance=True, 
    position=True, 
    gps=True, 
    inertial_unit=True, 
    motors=True
    ).enable()

distance_sensors = component_manager['distance']
position_sensors = component_manager['position']
gps = component_manager['gps']
inertial_unit = component_manager['inertial_unit']
motors = component_manager['motors']

#########################


# OBJECT INITIALIZATION
#########################

tracker = GridTracker(gps, inertial_unit)

#########################


# FLAGS
#########################

current_target = None
start_time = None

#########################

# CONTROL LOOP
while robot.step(timestep) != -1:

    # 5 seconds elapsed since collision
    if (start_time is not None) and (robot.getTime() - start_time) >= 5:
        setVelocityAll(motors, 0.0)
        resetPosition(robot)
        print(f"Visited cells: {tracker.getCoverage()}")
        break

    if current_target is None:  # if no action is taking place
        current_target = onCollision(distance_sensors, position_sensors, motors)

        if current_target is not None:  # if onCollision returned
            start_time = robot.getTime() if start_time is None else start_time # does not reset on collision

        else:
            cell_status = tracker.checkCell() # current cell status
            print(f'Current cell: {tracker.current_cell}, {cell_status}')
            print(tracker.getLocalVisitedFlags(verbose=True))
            
            action_code = randint(0, 2) # generate random action
            current_target = action(action_code, motors, position_sensors)

    else:
        if actionComplete(current_target, position_sensors):
            setVelocityAll(motors, 0.0)
            current_target = None  # next action