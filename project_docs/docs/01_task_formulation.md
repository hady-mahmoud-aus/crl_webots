# 01 — Task Formulation

## Sequential task setting

Define a sequence of three tasks:

$$
\mathcal{T} = (T_1, T_2, T_3)
$$

where the robot and policy are shared across tasks.

Recommended scene sequence:

- $T_1$: empty room
- $T_2$: static obstacles
- $T_3$: moving obstacles, or a harder static-obstacle layout if dynamic obstacles are not stable in time

This is a continual RL problem because the observation/action spaces remain fixed while scene layouts and transition distributions change.

## Task objective

The task is coverage-oriented search followed by homing.

The robot must:

1. explore previously unseen regions,
2. avoid excessive revisits,
3. avoid collisions and stalling,
4. reveal a hidden target once close enough,
5. approach the target after reveal.

## Full state vs policy observation

The simulator has a full environment state, but the policy receives only a compact partial observation.

Use this wording:

> The simulator defines the full environment state, but the policy receives a compact partial observation consisting of proximity sensors, heading features, local visited-cell indicators, and target-relative features after reveal.

## Observation vector

Use a fixed-size vector:

$$
o_t =
[p_0,\dots,p_7,
\sin\theta_t,\cos\theta_t,
v_{front},v_{left},v_{right},v_{back},
g_t,d_t,\sin\phi_t,\cos\phi_t]
$$

where:

- $p_0,\dots,p_7$: normalized proximity readings
- $(\sin\theta_t,\cos\theta_t)$: heading representation
- $v_{front},v_{left},v_{right},v_{back}$: heading-aligned visited-cell indicators
- $g_t$: target revealed flag
- $d_t$: target distance after reveal
- $(\sin\phi_t,\cos\phi_t)$: target bearing after reveal

Before reveal:

$$
g_t=0,\quad d_t=0,\quad \sin\phi_t=0,\quad \cos\phi_t=0
$$

After reveal, fill in the real target-relative values.

## Action space

Start with the simplest reliable action set:

$$
\mathcal{A}=
\{\texttt{forward},\texttt{rotate\_left},\texttt{rotate\_right}\}
$$

Optional later extension:

$$
\mathcal{A}=
\{\texttt{forward},\texttt{rotate\_left},\texttt{rotate\_right},
\texttt{forward\_left},\texttt{forward\_right}\}
$$

Do not add diagonal actions until the three-action version trains and evaluates.

## GPS-based visited-cell tracking

GPS is used for environment-side bookkeeping, not as raw global input to the policy.

Let the robot spawn position be $(x_0,y_0)$, and current position be $(x_t,y_t)$:

$$
\Delta x_t=x_t-x_0,\qquad \Delta y_t=y_t-y_0
$$

Use centered rounding:

$$
i_t=\mathrm{round}\left(\frac{\Delta x_t}{c}\right),\qquad
j_t=\mathrm{round}\left(\frac{\Delta y_t}{c}\right)
$$

Recommended initial cell size:

$$
c=0.2\text{ m}
$$

Store visited cells as a Python set:

```python
visited = set()
visited.add((i, j))
```

## Target reveal

The target is hidden during search.

It becomes revealed when:

$$
d_t \le R_{reveal}
$$

After reveal:

- $g_t = 1$
- target distance is included
- target bearing is included
- reward switches from search reward to homing reward

## Reward design

### Search reward

Use additive search rewards:

$$
r_t^{search}
=
\mathbf{1}_{new}r_{new}
-
\mathbf{1}_{revisit}r_{rev}
-
\mathbf{1}_{collision}r_{coll}
-
\mathbf{1}_{dwell}r_{dwell}
$$

Recommended starting values:

- $r_{new}=1.0$
- $r_{rev}=0.1$
- $r_{coll}=1.0$
- $r_{dwell}=0.1$

### Homing reward

Use progress-based homing reward:

$$
r_t^{home}
=
\alpha(d_{t-1}-d_t)
-
\mathbf{1}_{collision}r_{coll}
+
\mathbf{1}_{reached}r_{goal}
$$

Recommended starting values:

- $\alpha=1.0$
- $r_{goal}=5.0$

## Termination conditions

End an episode if:

- target is reached,
- maximum decision steps are reached,
- optionally, unrecoverable collision occurs.

Use “decision step” to mean one completed macro-action, not one Webots controller step.
