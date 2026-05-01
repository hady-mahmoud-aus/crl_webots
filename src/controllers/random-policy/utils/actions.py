from math import pi

from .sensors import readSensors
from .motors import setVelocityAll

# CONSTANTS
#########################

wheel_radius = 0.0205
axle_length = 0.052

forward_step_length = 0.1
forward_error = -4.75603 # manually calibrated

# currently covers 0.1m (oddly)
forward_step_radians = (0.2 / wheel_radius) + forward_error

rotation_angle = pi / 2
rotation_error = 0.2404 # manually calibrated to 5 decimal points
turn_radians = (axle_length * rotation_angle) / (2 * wheel_radius) + rotation_error

forward_velocity = 6
turn_velocity = 3

#########################

# DISCRETE ACTIONS

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

#########################


# Collision handling 
#########################

from .sensors import collision_value, front_sensor_names


def reverse(motors: dict, position_sensors: dict):
    setVelocityAll(motors, forward_velocity / 2)

    readings = readSensors(position_sensors, verbose=True)

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
    distance_readings = readSensors(front_sensors, "distance")
    
    if any(value >= collision_value for value in distance_readings):
        return reverse(motors, position_sensors)
    
    return None

#########################


# VARIABLE ACTIONS
#########################
def getTurnWheelRadians(angle_radians: float):
    return turn_radians * (angle_radians / pi / 2)

def turnByAngle(angle_radians: float, motors: dict, position_sensors: dict, threshold=None):
    if threshold:
        if angle_radians < threshold: return None
    
    setVelocityAll(motors, turn_velocity)

    readings = readSensors(position_sensors, verbose=True)

    wheel_delta = getTurnWheelRadians(angle_radians)

    targets = {
        "right": readings["right"] + wheel_delta,
        "left": readings["left"] - wheel_delta
    }

    motors["right"].setPosition(targets["right"])
    motors["left"].setPosition(targets["left"])

    return targets


def getForwardWheelRadians(distance_meters: float):
    return forward_step_radians * (distance_meters / forward_step_length)

def forwardByDistance(distance_meters: float, motors: dict, position_sensors: dict):
    setVelocityAll(motors, forward_velocity)

    readings = readSensors(position_sensors, verbose=True)

    wheel_delta = getForwardWheelRadians(distance_meters)

    targets = {
        "right": readings["right"] + wheel_delta,
        "left": readings["left"] + wheel_delta
    }

    motors["right"].setPosition(targets["right"])
    motors["left"].setPosition(targets["left"])

    return targets