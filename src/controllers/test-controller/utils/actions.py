from numpy import pi

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


def forward(motors: dict, current_position: dict):
    setVelocityAll(motors, forward_velocity)
    
    for name, motor in motors.items():
        current = current_position[name]
        
        motor.setPosition(current + forward_step_radians)


def right(motors: dict, current_position: dict, velocity=turn_velocity):
    setVelocityAll(motors, turn_velocity)
    
    current_right = current_position['right']
    current_left = current_position['left']
    
    motors['right'].setPosition(current_right - turn_radians)
    motors['left'].setPosition(current_left + turn_radians)


def left(motors: dict, current_position: dict):
    setVelocityAll(motors, turn_velocity)
    
    current_right = current_position['right']
    current_left = current_position['left']
    
    motors['right'].setPosition(current_right + turn_radians)
    motors['left'].setPosition(current_left - turn_radians)


def action(action_code: int, motors: dict, current_postion: dict):
    actions = [forward, right, left]
    actions[action_code](motors, current_postion)