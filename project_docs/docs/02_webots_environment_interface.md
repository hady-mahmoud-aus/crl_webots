# 02 — Webots Environment Interface

## Required e-puck devices

Use these Webots devices:

- distance sensors: `ps0` to `ps7`
- GPS
- InertialUnit
- left wheel motor
- right wheel motor
- left wheel position sensor
- right wheel position sensor

The current `ComponentManager` enables distance sensors, position sensors, GPS, and InertialUnit, and retrieves the wheel motors.

## Heading from InertialUnit

Use the Webots `InertialUnit` to estimate robot heading for the policy observation and target-relative bearing.

```python
roll, pitch, yaw = inertial_unit.getRollPitchYaw()
theta = yaw
sin_theta = math.sin(theta)
cos_theta = math.cos(theta)
```

The policy observation uses `sin(theta)` and `cos(theta)`.

## Robot constants

The current action code uses:

$$
r=0.0205\text{ m}
$$

$$
b=0.052\text{ m}
$$

where:

- $r$: wheel radius,
- $b$: wheel separation / axle length.

## Controller step vs decision step

Use two time scales:

- **Controller step:** one Webots simulation update.
- **Decision step:** one completed macro-action selected by the DQN.

A DQN transition corresponds to one macro-action decision step.

## Current RL action set

The current action functions are:

1. `forward`
2. `right`
3. `left`

In method descriptions, these can be written as:

1. `forward`
2. `rotate_right`
3. `rotate_left`

## Current action parameters

The code uses manually calibrated wheel targets.

### Forward

Variables:

```text
forward_step_length = 0.1
forward_error = -4.75603
forward_step_radians = (0.2 / wheel_radius) + forward_error
forward_velocity = 6
```

Although the expression uses `0.2 / wheel_radius`, the manual calibration currently makes the action cover about `0.1 m` according to the code comments.

### Rotation

Variables:

```text
rotation_angle = pi / 2
rotation_error = 0.2404
turn_radians = (axle_length * rotation_angle) / (2 * wheel_radius) + rotation_error
turn_velocity = 3
```

The intended macro-rotation is approximately 90 degrees.

## Macro-action execution

A macro-action should:

1. read current wheel positions,
2. compute target wheel positions,
3. set motor velocities,
4. command motor position targets,
5. step Webots until action completion, collision interruption, or episode termination,
6. stop motors at completion,
7. read sensors and update the observation on the next decision step.

## Action completion

The current code checks position-sensor readings against target wheel positions with tolerance:

```text
tolerance = 0.02
```

When all wheel-position errors are within tolerance, the macro-action is complete.

## Collision handling

The current collision detector uses the front distance sensors:

```text
front_sensor_names = ['ps0', 'ps7']
collision_value = 0.1
```

During a forward action, if a front collision is detected:

1. motor velocities are set to zero,
2. the cell in front of the robot is added to `blocked_cells`,
3. `is_collision` is set,
4. collision count is incremented,
5. the current macro-action ends early.

The `reverse` helper exists but the current forward-collision interruption path uses `react=False`, so it detects collision without executing automatic reverse recovery.

## Grid-cell assignment

The current code uses:

```text
cell_size = 0.1
origin = (0, -0.9)
```

Cell assignment uses centered half-away-from-zero rounding:

```python
if value >= 0:
    return int(floor(value + 0.5))
else:
    return int(ceil(value - 0.5))
```

## Heading-aligned local flags

The current code computes a coarse heading direction from `sin(theta)` and `cos(theta)`:

```python
if abs(cos_theta) > abs(sin_theta):
    dx, dy = sign(cos_theta), 0
else:
    dx, dy = 0, sign(sin_theta)
```

Then it defines local cells:

```python
front = (i + dx, j + dy)
right = (i + dy, j - dx)
left  = (i - dy, j + dx)
back  = (i - dx, j - dy)
```

The observation flag is `1` if the local cell is already visited or blocked.

## Target management

The target is sampled inside a square arena with:

```text
arena_size = 2
buffer = arena_size * 0.05
min_distance_from_origin = 0.6
reveal_radius = 0.35
reach_radius = 0.15
```

Target positions are sampled uniformly within the buffered arena until they are far enough from the origin.

The target is not exposed to the observation before reveal. After reveal, normalized distance and bearing are included.

## Current controller structure

The current top-level controller:

1. initializes Webots devices,
2. reads environment variables,
3. creates the `TargetManager`, `DQnManager`, and `DQnPolicy`,
4. runs episodes inside the Webots control loop,
5. appends episode metrics to a dataframe,
6. saves logs and model parameters after all episodes,
7. quits Webots.

Relevant environment variables:

| Variable | Purpose |
|---|---|
| `SEED` | random seed |
| `NUM_EPISODES` | number of episodes |
| `POLICY` | save-directory label |
| `SCENE_ID` | current scene id |
| `PARENT_SCENE` | parent/previous scene label for filenames |
| `EVAL` | evaluation flag |
| `PARAMS_NAME` | checkpoint filename under `runs/<POLICY>/` |
| `SELECTIVE_REPLAY_NAME` | SSER artifact filename under `runs/<POLICY>/` |
| `EWC_STATE_NAME` | EWC state filename under `runs/<POLICY>/` |

## Current episode log fields

The logger currently tracks:

| Field | Meaning |
|---|---|
| `episode` | episode index |
| `scene_id` | scene identifier |
| `seed` | random seed |
| `revealed` | whether target was revealed |
| `reached` | whether target was reached |
| `timeout` | max decision-step limit reached before target reach |
| `unique_cells_covered` | number of visited cells |
| `reward` | total episode reward |
| `collisions` | search/control collision count |
| `decision_steps` | number of macro-actions |

## Future environment API target

The code is currently policy-driven rather than using a clean Gym-style environment API. A future refactor may expose:

```python
obs = env.reset(scene_id=1, seed=0)
obs, reward, done, info = env.step(action)
metrics = env.get_episode_metrics()
env.close()
```

This is a refactor target, not the current code structure.
