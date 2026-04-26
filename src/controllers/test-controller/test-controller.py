from controller import Robot

def position_all(position, *args):
    for motor in args:
        motor.setPosition(position)

def velocity_all(velocity, *args):
    for motor in args:
        motor.setVelocity(velocity)

robot = Robot()

# get the time step of the current world.
timestep = int(robot.getBasicTimeStep())

motor_left = robot.getDevice('left wheel motor')
motor_right = robot.getDevice('right wheel motor')

position_all(float('inf'), motor_right, motor_left)

while robot.step(timestep) != -1:
    
    velocity_all(2, motor_right, motor_left)
