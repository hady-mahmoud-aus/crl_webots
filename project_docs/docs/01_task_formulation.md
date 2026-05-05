# 01 — Task Formulation

## Sequential task setting

Define a sequence of three tasks:

$$
\mathcal{T} = (T_1, T_2, T_3)
$$

where the robot and learned policy are shared across tasks.

Recommended scene sequence:

- $T_1$: empty room
- $T_2$: static obstacles
- $T_3$: moving obstacles, or a harder static-obstacle layout if dynamic obstacles are not stable in time

This is a continual RL problem because the observation/action spaces remain fixed while scene layouts and transition distributions change.

## Task objective

The task is **target-revealing navigation with learned post-reveal approach**.

The policy must:

1. explore previously unseen regions before target reveal,
2. avoid excessive revisits, small loops, dwell, and collisions,
3. reveal a hidden target once close enough,
4. after reveal, use target distance and bearing to approach the target,
5. reach the target before the maximum decision-step limit.

The main continual-learning objective is target reveal. Target reaching after reveal is also logged and can be used as a final episode success metric.

## Full state vs policy observation

The simulator has a full environment state, but the policy receives a compact partial observation.

Use this wording:

> The simulator defines the full environment state, but the learned policy receives a compact observation consisting of local visited/blocked-cell indicators, dwell and loop features, proximity sensors, heading features, and target-relative features. During pre-reveal search, target-relative distance and bearing are zeroed so that the target remains hidden. After reveal, target-relative distance and bearing are enabled for the learned target-approach regime.

## Observation vector

The current code uses a 19-dimensional observation:

$$
o_t =
[v_f,v_r,v_l,v_b,
 d_{dwell},
 \ell,
 p_0,\dots,p_7,
 \sin\theta_t,\cos\theta_t,
 \hat d_t,
 \sin\phi_t,\cos\phi_t]
$$

where:

- $v_f,v_r,v_l,v_b$: heading-aligned local visited-or-blocked flags for front, right, left, and back,
- $d_{dwell}$: normalized dwell feature,
- $\ell$: recent-loop score,
- $p_0,\dots,p_7$: normalized proximity readings,
- $(\sin\theta_t,\cos\theta_t)$: robot heading representation,
- $\hat d_t$: normalized target distance,
- $(\sin\phi_t,\cos\phi_t)$: target bearing representation.

Before target reveal:

$$
\hat d_t=0,
\qquad
\sin\phi_t=0,
\qquad
\cos\phi_t=0.
$$

After target reveal, these target-relative features are computed from the current robot pose and the target position.

## Action space

The current code uses the simplest reliable macro-action set:

$$
\mathcal{A}=\{
\texttt{forward},
\texttt{rotate\_right},
\texttt{rotate\_left}
\}
$$

The action-index order is:

| Action index | Code action |
|---:|---|
| 0 | `forward` |
| 1 | `rotate_right` |
| 2 | `rotate_left` |

Do not add diagonal actions until the three-action version trains and evaluates.

## GPS-based visited-cell tracking

GPS is used for environment-side bookkeeping, not as raw global input to the policy.

The current code uses a fixed origin:

$$
(x_0,y_0)=(0,-0.9)
$$

and cell size:

$$
c=0.1\text{ m}.
$$

Given current position $(x_t,y_t)$:

$$
\Delta x_t=x_t-x_0,
\qquad
\Delta y_t=y_t-y_0.
$$

The grid cell is assigned with centered rounding:

$$
i_t=\mathrm{round\_half\_away\_from\_zero}\left(\frac{\Delta x_t}{c}\right),
\qquad
j_t=\mathrm{round\_half\_away\_from\_zero}\left(\frac{\Delta y_t}{c}\right).
$$

Visited cells and blocked cells are stored as Python sets.

## Cell status categories

The current code uses four cell-status categories:

| Status | Meaning |
|---|---|
| `same` | robot remains in the current cell |
| `unvisited` | robot entered a new cell |
| `visited` | robot entered an old cell not in the recent-cell window |
| `recent` | robot entered a recently visited cell |

A small recent-cell deque is used to detect short loops.

## Loop score

The current loop score is:

$$
\ell = 1 - \frac{|\mathrm{unique}(C_{recent})|}{|C_{recent}|}
$$

where $C_{recent}$ is the recent-cell window. Higher values indicate more repetitive local motion.

## Dwell feature

The code tracks how many consecutive decision steps the robot remains in the same cell. The first two same-cell steps are tolerated, and the observation uses:

$$
d_{dwell}=\frac{\min(\max(0,dwell\_count-2),5)}{5}.
$$

Collision steps do not increase the observed dwell feature.

## Target reveal and reach

The target is hidden before reveal. It becomes revealed when:

$$
d_t \le R_{reveal}
$$

with:

$$
R_{reveal}=0.35\text{ m}.
$$

After reveal:

- the episode dictionary marks `revealed=True`,
- target distance and bearing become available in the observation,
- the reward switches to the target-approach reward,
- the same learned policy continues selecting actions.

The target is reached when:

$$
d_t \le R_{reach}
$$

with:

$$
R_{reach}=0.15\text{ m}.
$$

## Search reward before reveal

The pre-reveal reward is:

$$
r_t^{search}
= c_t
-2\mathbf{1}_{collision}
-0.2\,dwell_t
-0.5\,\ell_t\,\mathbf{1}_{loopPenalty}
+10\mathbf{1}_{revealed}.
$$

The cell-status term $c_t$ is:

| Cell status | Reward term |
|---|---:|
| `unvisited` | `+1.0` |
| `visited` | `-0.1`, or `0.0` in escape mode |
| `recent` | `-0.1` |
| `same` | `0.0` |

If a collision occurs, the cell-status term is forced to `0.0`, and collision becomes the dominant penalty.

The loop penalty is applied when the step is not a collision and the cell is not unvisited.

## Escape mode

Escape mode is enabled when all local front/right/left/back cells in the previous observation are already visited or blocked. In escape mode, the normal visited-cell penalty is removed to avoid trapping the policy in a fully explored neighborhood.

## Target-approach reward after reveal

After reveal, the code uses:

$$
r_t^{approach}
=
-0.02
-3\mathbf{1}_{collision}
-0.5\,dwell_t
+5(d_{prev}-d_t)
+10\mathbf{1}_{reached}.
$$

Here $d_t$ is the normalized target distance. The progress term rewards movement toward the target after reveal.

## Success and termination conditions

### Reveal success

An episode counts as successful for the main continual-learning metric when:

- the target is revealed.

### Reach success

An episode counts as final target-reaching success when:

- the target is reached after reveal.

### Episode termination

The current code ends the episode when:

- the target is reached, or
- the maximum decision-step limit is reached.

The terminal DQN transition is represented by `next_state=None`.

The current timeout flag is named `timeout` in the logger. It indicates that the episode hit the max decision-step limit before reaching the target. A future cleanup can split this into separate pre-reveal and post-reveal timeout fields.
