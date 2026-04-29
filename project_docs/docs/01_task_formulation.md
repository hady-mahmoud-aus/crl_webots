# 01 — Task Formulation

## Sequential task setting

Define a sequence of three tasks:

$$
\mathcal{T} = (T_1, T_2, T_3)
$$

where the robot and search policy are shared across tasks.

Recommended scene sequence:

- $T_1$: empty room
- $T_2$: static obstacles
- $T_3$: moving obstacles, or a harder static-obstacle layout if dynamic obstacles are not stable in time

This is a continual RL problem because the observation/action spaces remain fixed while scene layouts and transition distributions change.

## Task objective

The task is **coverage-oriented search with deterministic post-reveal homing**.

The RL policy must:

1. explore previously unseen regions,
2. avoid excessive revisits,
3. avoid collisions and stalling during search,
4. reveal a hidden target once close enough.

After the target is revealed, the RL policy no longer acts. A deterministic homing controller then:

1. turns toward the target,
2. moves forward,
3. repeats until the target is reached or a homing timeout occurs,
4. attempts simple recovery if a collision is detected.

The main RL objective is target reveal, not target reaching.

## Full state vs policy observation

The simulator has a full environment state, but the policy receives only a compact partial observation for search.

Use this wording:

> The simulator defines the full environment state, but the RL policy receives a compact partial observation consisting of proximity sensors, heading features, and local visited-cell indicators. Target-relative distance and bearing are used by the deterministic homing controller after reveal, not by the learned search policy.

## Observation vector

Use a fixed-size search observation vector:

$$
o_t =
[p_0,\dots,p_7,
\sin\theta_t,\cos\theta_t,
v_{front},v_{left},v_{right},v_{back}]
$$

where:

- $p_0,\dots,p_7$: normalized proximity readings
- $(\sin\theta_t,\cos\theta_t)$: heading representation
- $v_{front},v_{left},v_{right},v_{back}$: heading-aligned visited-cell indicators

The target is hidden during the RL phase. Do not provide target-relative distance or bearing to the policy during search.

The environment may still compute target distance and bearing internally for:

- checking whether the target has been revealed,
- controlling deterministic homing after reveal,
- auxiliary logging.

## Action space

Start with the simplest reliable RL action set:

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

- the RL policy stops acting,
- the search episode is counted as successful,
- the final RL transition receives a reveal reward,
- the deterministic homing controller takes over,
- the Webots episode continues until deterministic homing reaches the target or times out.

## Reward design

### Search reward

Use additive search rewards with a target-reveal bonus:

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
+
\mathbf{1}_{revealed}r_{reveal}
$$

Recommended starting values:

- $r_{new}=1.0$
- $r_{rev}=0.1$
- $r_{coll}=1.0$
- $r_{dwell}=0.1$
- $r_{reveal}=5.0$

The reward is for revealing the target, not for reaching it during deterministic homing.

### Homing reward

Do not use a learned homing reward in the first working version.

After reveal, deterministic homing is environment-side control. Its progress, collisions, recovery attempts, and final target reaching may be logged as auxiliary metrics, but they should not create additional DQN training rewards.

## Deterministic homing controller

Use a simple controller after target reveal:

1. compute target-relative bearing $\phi_t$ and distance $d_t$,
2. if $|\phi_t|$ is above a heading tolerance, rotate toward the target,
3. otherwise move forward a short distance,
4. repeat until $d_t \le R_{goal}$ or a homing timeout occurs,
5. if a collision is detected, perform simple recovery and continue.

Initial recovery behavior can be:

1. stop motors,
2. reverse a short distance,
3. rotate away from the strongest proximity reading,
4. resume homing.

Do not penalize the RL agent for collisions that occur during deterministic homing. Keep them as auxiliary diagnostic logs only.

## Success and termination conditions

### RL success

An episode counts as successful for RL evaluation when:

- the target is revealed.

### Webots episode termination

The Webots episode ends when:

- deterministic homing reaches the target after reveal,
- homing times out after reveal,
- maximum search decision steps are reached without target reveal,
- optionally, unrecoverable search-phase collision occurs.

Use “decision step” to mean one completed RL macro-action, not one Webots controller step.

For DQN training, the terminal search transition should be the transition that reveals the target or reaches the maximum search-step limit. The deterministic homing rollout after reveal should not be added to the DQN replay buffer.
