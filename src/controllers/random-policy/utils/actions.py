from numpy import pi

from .sensors import readSensors
from .motors import setVelocityAll

# CONSTANTS
#########################

wheel_radius = 0.0205
axle_length = 0.052

forward_step_length = 0.2
forward_error = -4.76

# currently covers 0.1m (oddly)
forward_step_radians = (forward_step_length / wheel_radius) + forward_error

rotation_angle = pi / 2
rotation_error = 0.242
turn_radians = (axle_length * rotation_angle) / (2 * wheel_radius) + rotation_error

forward_velocity = 6
turn_velocity = 3

#########################


def forward(motors: dict, position_sensors: dict):
    setVelocityAll(motors, forward_velocity)
    
    readings = readSensors(position_sensors, verbose=True)
    
    targets = {
        "right": readings["right"] + forward_step_radians,
        "left": readings["left"] + forward_step_radians
    }

    motors["right"].setPosition(targets["right"])
    motors["left"].setPosition(targets["left"])
    
    return targets


def right(motors: dict, position_sensors: dict):
    setVelocityAll(motors, turn_velocity)
    
    readings = readSensors(position_sensors, verbose=True)
    
    targets = {
        "right": readings["right"] - turn_radians,
        "left": readings["left"] + turn_radians
    }
    
    motors['right'].setPosition(targets['right'])
    motors['left'].setPosition(targets['left'])
    
    return targets


def left(motors: dict, position_sensors: dict):
    setVelocityAll(motors, turn_velocity)
    
    readings = readSensors(position_sensors, verbose=True)
    
    targets = {
        "right": readings["right"] + turn_radians,
        "left": readings["left"] - turn_radians
    }
    
    motors['right'].setPosition(targets['right'])
    motors['left'].setPosition(targets['left'])

    return targets


def action(action_code: int, motors: dict, position_sensors: dict):
    actions = [forward, right, left]
    
    return actions[action_code](motors, position_sensors)


def actionComplete(targets: dict, position_sensors: dict, tolerance=0.02):
    readings = readSensors(position_sensors, verbose=True)

    for name, target in targets.items():
        current = readings[name]

        if abs(current - target) > tolerance:
            return False

    return True