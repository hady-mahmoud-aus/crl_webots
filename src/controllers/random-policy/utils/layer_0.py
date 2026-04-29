# Target Generation
#########################

import random

arena_size = 2;

def getTarget() -> tuple:
    limit = (arena_size / 2) - 0.1 # so target is not on a wall
    
    number = lambda : round(random.uniform(-limit, limit), 2)
    return (number(), number())

#########################


# Episode Position Reset
#########################

from controller import Supervisor

origin = [0, 0, 0] # [x, y, z]

def resetPosition(robot: Supervisor, x=None, y=None):
    node = robot.getSelf()
    
    position = origin if x is None or y is None else [x, y, 0]
    
    translation = node.getField('translation')
    translation.setSFVec3f(position)
    node.resetPhysics()

#########################


# Collision handling (needs refinement for practical use)
#########################

from .sensors import collision_value, front_sensor_names, readSensors
from .actions import forward_step_radians, forward_velocity
from .motors import setVelocityAll

def reverse(motors: dict, position_sensors: dict):
    setVelocityAll(motors, forward_velocity / 2)

    readings = readSensors(position_sensors)

    reverse_radians = forward_step_radians * 0.25

    targets = {
        "left": readings["left"] - reverse_radians,
        "right": readings["right"] - reverse_radians
    }

    motors["left"].setPosition(targets["left"])
    motors["right"].setPosition(targets["right"])

    return targets


def onCollision(distance_sensors: dict, position_sensors: dict,  motors: dict) -> dict: 
    front_sensors = {name: sensor for name, sensor in distance_sensors.items() if name in front_sensor_names}
    distance_readings = readSensors(front_sensors, "distance").values()
    
    if any(value >= collision_value for value in distance_readings):
        return reverse(motors, position_sensors)
    
    return None

#########################