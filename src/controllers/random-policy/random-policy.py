from random import randint

from controller import Supervisor

from utils.actions import action, actionComplete
from utils.sensors import getDistanceSensors, getPositionSensors, enableSensors
from utils.motors import getMotors, setVelocityAll
from utils.layer_0 import onCollision, resetPosition


robot = Supervisor()
timestep = int(robot.getBasicTimeStep())

# SENSOR / ACTUATOR INITIALIZATION
#########################

distance_sensors = getDistanceSensors(robot)
enableSensors(distance_sensors, timestep)

position_sensors = getPositionSensors(robot)
enableSensors(position_sensors, timestep)

gps = robot.getDevice('gps')
gps.enable(timestep)

inertial_unit = robot.getDevice('inertial unit')
inertial_unit.enable(timestep)

motors = getMotors(robot)

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
        break

    if current_target is None:  # if no action is taking place
        current_target = onCollision(distance_sensors, position_sensors, motors)

        if current_target is not None:  # if onCollision returned
            start_time = robot.getTime() if start_time is None else start_time # does not reset on collision

        else:
            action_code = randint(0, 2)
            current_target = action(0, motors, position_sensors)

    else:
        if actionComplete(current_target, position_sensors):
            setVelocityAll(motors, 0.0)
            current_target = None  # next action