# 02 — Webots Environment Interface

## Required e-puck devices

Use these Webots devices:

- distance sensors: `ps0` to `ps7`
- GPS
- Compass
- left wheel motor
- right wheel motor
- left wheel position sensor
- right wheel position sensor

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
- **Decision step:** one completed macro-action selected by the DQN.

A DQN transition corresponds to one decision step.

## Initial action set

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

## Recommended action parameters

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

## Macro-action execution

A macro-action should:

1. read current wheel positions,
2. compute target wheel positions,
3. command wheel targets,
4. step the simulator until completion, collision, or timeout,
5. accumulate low-level rewards if needed,
6. read GPS, Compass, and proximity sensors,
7. update visited cells,
8. return the next observation and transition data.

## Collision handling

Initial simple version:

- monitor proximity sensors during macro-action execution,
- if threshold is exceeded:
  - stop motors,
  - mark collision,
  - apply collision penalty,
  - end the macro-action early.

This is safer than letting a forward command continue after impact.

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

The `info` dictionary should include:

```python
{
    "scene_id": int,
    "collision": bool,
    "new_cell": bool,
    "revisit": bool,
    "dwell": bool,
    "target_revealed": bool,
    "target_reached": bool,
    "cell": (int, int),
    "duration": int,
}
```
