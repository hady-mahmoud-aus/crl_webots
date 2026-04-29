from controller import Robot


def getMotors(robot: Robot) -> dict:
    return {
        'right': robot.getDevice('right wheel motor'),
        'left': robot.getDevice('left wheel motor')
    }


def setVelocityAll(motors: dict, velocity):
    for motor in motors.values():
        motor.setVelocity(velocity)