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

## Heading from InertialUnit

Use the Webots `InertialUnit` to estimate robot heading for the policy observation and deterministic homing.
Enable it at reset/setup time and read roll, pitch, and yaw with:

```python
roll, pitch, yaw = inertial_unit.getRollPitchYaw()
theta = yaw
sin_theta = math.sin(theta)
cos_theta = math.cos(theta)
```

Use `sin_theta` and `cos_theta` as the heading features in the RL observation vector.

## Robot constants

Use the e-puck constants from the PROTO:

$$
r=0.020\text{ m}
$$

$$
b=0.052\text{ m}
$$

where:

- $r$: wheel radius
- $b$: wheel separation / axle length

## Controller step vs decision step

Use two time scales:

- **Controller step:** one Webots simulation update.
- **Decision step:** one completed macro-action selected by the DQN during search.

A DQN transition corresponds to one search-phase decision step.

After target reveal, deterministic homing may use its own lower-level control loop. Homing controller steps should not be stored as DQN transitions.

## Initial RL action set

Start with:

1. `forward`
2. `rotate_left`
3. `rotate_right`

For straight movement of distance $s$:

$$
\Delta\varphi=\frac{s}{r}
$$

For in-place rotation by angle $\alpha$:

$$
\Delta\varphi_L=-\frac{b\alpha}{2r},
\qquad
\Delta\varphi_R=\frac{b\alpha}{2r}
$$

For the opposite rotation direction, swap the signs.

## Recommended RL action parameters

Use:

- forward distance: one grid cell, $s=c$
- rotate left/right: $\alpha=\pi/2$

For $c=0.2\text{ m}$:

$$
\Delta\varphi_{forward}=\frac{0.2}{0.020}=10\text{ rad}
$$

$$
|\Delta\varphi_{90}|=
\frac{0.052(\pi/2)}{2(0.020)}
\approx 2.04\text{ rad}
$$

## Search macro-action execution

A search macro-action should:

1. read current wheel positions,
2. compute target wheel positions,
3. command wheel targets,
4. step the simulator until completion, search-phase collision, target reveal, or timeout,
5. accumulate search reward,
6. read GPS, InertialUnit, and proximity sensors,
7. update visited cells,
8. check whether the target is revealed,
9. return the next observation and transition data.

If target reveal occurs during or after the macro-action, mark the search transition as terminal for DQN training and then run deterministic homing outside the replay buffer.

## Search collision handling

Initial simple version during the RL search phase:

- monitor proximity sensors during macro-action execution,
- if threshold is exceeded:
  - stop motors,
  - mark collision,
  - apply search collision penalty,
  - end the macro-action early.

This is safer than letting a forward command continue after impact.

## Deterministic homing controller

After target reveal, stop asking the DQN for actions and call a deterministic homing routine.

Recommended control loop:

```python
def run_deterministic_homing(max_homing_steps):
    recovery_count = 0

    for _ in range(max_homing_steps):
        d, phi = compute_target_distance_and_bearing()

        if d <= goal_radius:
            stop_motors()
            return {"target_reached": True, "homing_timeout": False,
                    "homing_recovery_count": recovery_count}

        if homing_collision_detected():
            recovery_count += 1
            simple_homing_recovery()
            continue

        if abs(phi) > heading_tolerance:
            rotate_toward(phi)
        else:
            move_forward_short()

    stop_motors()
    return {"target_reached": False, "homing_timeout": True,
            "homing_recovery_count": recovery_count}
```

A simple recovery routine can be:

```python
def simple_homing_recovery():
    stop_motors()
    reverse_short_distance()
    rotate_away_from_strongest_proximity_sensor()
```

Do not assign RL penalty for homing collisions. Log them separately as homing diagnostics.

Recommended initial homing parameters:

- heading tolerance: `10` to `15` degrees
- short forward distance: `0.05` to `0.10 m`
- goal radius: choose smaller than or equal to the reveal radius, for example `0.05` to `0.10 m`
- homing timeout: fixed number of controller steps or macro-equivalent steps

## Grid-cell assignment

Use centered rounding:

```python
i = round((x - x0) / cell_size)
j = round((y - y0) / cell_size)
```

Use optional cell locking to reduce boundary flicker:

```python
if new_cell != current_cell:
    if new_cell == candidate_cell:
        steps_in_candidate += 1
    else:
        candidate_cell = new_cell
        steps_in_candidate = 1

    if steps_in_candidate >= k:
        current_cell = new_cell
        visited.add(current_cell)
else:
    candidate_cell = None
    steps_in_candidate = 0
```

Recommended:

```python
k = 2
```

## Heading-aligned visited flags

Compute a coarse heading direction:

```python
if abs(cos_theta) > abs(sin_theta):
    dx, dy = sign(cos_theta), 0
else:
    dx, dy = 0, sign(sin_theta)
```

Then:

```python
front = (i + dx, j + dy)
back  = (i - dx, j - dy)
left  = (i - dy, j + dx)
right = (i + dy, j - dx)
```

Observation flags:

```python
visited_front = int(front in visited)
visited_back  = int(back in visited)
visited_left  = int(left in visited)
visited_right = int(right in visited)
```

## Environment API target

Aim for a small API that Claude Code can implement and test:

```python
obs = env.reset(scene_id=1, seed=0)
obs, reward, done, info = env.step(action)
metrics = env.get_episode_metrics()
env.close()
```

The `done` flag returned to the training loop should become true when the search phase terminates, including successful target reveal or maximum search steps.

If `target_revealed=True`, the environment may internally run deterministic homing before returning final episode metrics, but homing steps should not be inserted into the DQN replay buffer.

The `info` dictionary should include:

```python
{
    "scene_id": int,
    "phase": "search" or "homing_complete",
    "collision": bool,
    "new_cell": bool,
    "revisit": bool,
    "dwell": bool,
    "target_revealed": bool,
    "rl_success": bool,
    "target_reached": bool,
    "homing_timeout": bool,
    "homing_recovery_count": int,
    "cell": (int, int),
    "duration": int,
}
```

Recommended convention:

- `rl_success = target_revealed`
- `target_reached` is an auxiliary post-reveal metric
- homing collisions/recoveries are auxiliary diagnostics and do not affect DQN reward
