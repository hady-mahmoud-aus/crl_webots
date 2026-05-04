from controller import Supervisor
import math

robot = Supervisor()
timestep = int(robot.getBasicTimeStep())

# Get all obstacle nodes
obstacles = []
for i in range(11):
    node = robot.getFromDef(f"box_{i}")
    if node:
        obstacles.append(node)
        

# Store initial positions and assign movement axes
initial_positions = []
for node in obstacles:
    pos = node.getField("translation").getSFVec3f()
    initial_positions.append(pos)

# Amplitude and speed
AMPLITUDE = 0.1  # how far they move from starting point
SPEED = 0.5      # how fast they move

time = 0

while robot.step(timestep) != -1:
    time += timestep / 1000.0  # convert to seconds

    for i, node in enumerate(obstacles):
        x0, y0, z0 = initial_positions[i]
        offset = AMPLITUDE * math.sin(SPEED * time + i)  # i offsets phase so they don't all move in sync

        # Alternate: even-indexed boxes move along X, odd along Z
        if i % 2 == 0:
            new_pos = [x0 + offset, y0, z0]
        else:
            new_pos = [x0, y0 + offset, z0]

        node.getField("translation").setSFVec3f(new_pos)