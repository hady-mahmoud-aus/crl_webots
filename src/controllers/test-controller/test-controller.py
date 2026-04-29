from controller import Robot, Supervisor
from utils.actions import *
from utils.sensors import *
from utils.motors import getMotors
from utils.layer_0 import onCollision, resetPosition

robot = Supervisor()
timestep = int(robot.getBasicTimeStep())

distance_sensors = getDistanceSensors(robot)
enableSensors(distance_sensors, timestep)

position_sensors = getPositionSensors(robot)
enableSensors(position_sensors, timestep)

gps = robot.getDevice('gps')
gps.enable(timestep)

inertial_unit = robot.getDevice('inertial unit')
inertial_unit.enable(timestep)

motors = getMotors(robot)

collision = False
once = False
current_time = float('inf')

while robot.step(timestep) != -1:
    
    sensor_values = readSensors(distance_sensors)
    current_position = readSensors(position_sensors)
    
    print(readHeading(inertial_unit))

    if not once: 
        boolean = onCollision(sensor_values, motors, current_position)
        collision, once = (boolean, boolean)
        
        if once: current_time = robot.getTime()

    if not collision:
        action(0, motors, current_position)
        
    if robot.getTime() - current_time >= 5:
        resetPosition(robot)

