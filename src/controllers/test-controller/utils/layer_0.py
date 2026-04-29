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

from .sensors import collision_value, front_sensor_names
from .actions import forward_step_radians, forward_velocity
from .motors import setVelocityAll

def reverse(motors: dict, current_position: dict):
    setVelocityAll(motors, forward_velocity / 2)
    
    reverse_radians = forward_step_radians * 0.25
    
    for name, motor in motors.items():
        current = current_position[name]
        
        motor.setPosition(current - reverse_radians)


def onCollision(values: dict, motors: dict, current_position: dict) -> bool: 
    front_sensors = {name: value for name, value in values.items() if name in front_sensor_names}.values()
    
    if any(value > collision_value for value in front_sensors):
        reverse(motors, current_position)
        
        return True
    
    return False

#########################