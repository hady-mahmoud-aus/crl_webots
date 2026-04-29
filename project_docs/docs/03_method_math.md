# 03 — Method and Math

## Method summary

The method is:

> Custom PyTorch Double DQN for search + selective episodic replay inspired by OPR + DQN-compatible online EWC approximation inspired by KGCRL, with deterministic post-reveal homing.

This is an inspired-by adaptation, not an exact implementation of either paper.

The learned RL component solves the search problem only. It learns to explore and reveal the hidden target. Once the target is revealed, the learned policy stops and a deterministic homing controller takes over.

## Q-network

Use a compact MLP:

$$
o_t
\rightarrow
\mathrm{FC}(128)
\rightarrow
\mathrm{ReLU}
\rightarrow
\mathrm{FC}(128)
\rightarrow
\mathrm{ReLU}
\rightarrow
Q(o_t,\cdot)
$$

The output dimension equals the number of discrete search actions.

## Double DQN target for search macro-actions

Each search macro-action transition is:

$$
(s_t,a_t,R_t,s_{t+n},done_{search},n)
$$

where $n$ is the number of Webots controller steps inside the search macro-action.

The accumulated search reward is:

$$
R_t=
\sum_{\ell=0}^{n-1}\gamma^\ell r^{search}_{t+\ell}
$$

The search terminal flag $done_{search}$ is true if:

- the target is revealed,
- the maximum number of search decision steps is reached,
- optionally, an unrecoverable search-phase failure occurs.

The Double DQN target is:

$$
y=
\begin{cases}
R_t, & \text{if } done_{search}\\
R_t+\gamma^n Q_{target}
\left(
s',
\arg\max_{a'}Q_{online}(s',a')
\right), & \text{otherwise}
\end{cases}
$$

The DQN loss is:

$$
L_{DQN}
=
\mathbb{E}
\left[
\left(
Q_{online}(s,a)-y
\right)^2
\right]
$$

Do not add deterministic homing rewards to $R_t$.

## Current replay buffer

Store search macro-action transitions:

```python
transition = {
    "state": state,
    "action": action,
    "reward_sum": reward_sum,
    "next_state": next_state,
    "done_search": done_search,
    "duration": duration,
    "info": info,
}
```

Homing controller steps after reveal should not be stored as DQN transitions.

## Selective episodic replay

After each scene, store top-$K$ high-quality search episodes.

Episode quality should prioritize:

1. target revealed / `rl_success`,
2. high coverage,
3. low search-phase collisions,
4. shorter search time or higher search return.

Example episode record:

```python
episode = {
    "scene_id": scene_id,
    "transitions": [...],
    "metrics": {
        "rl_success": bool,
        "target_reveal_rate": float,
        "coverage_count": int,
        "coverage_ratio_offline": float,
        "search_collisions": int,
        "decision_steps_to_reveal": int,
        "search_return": float,
        "target_reached_after_homing": bool,
        "homing_recovery_count": int,
    },
}
```

During later scenes, sample minibatches using:

$$
80\%\text{ current replay} + 20\%\text{ old selective replay}
$$

## Online EWC approximation

Use online EWC, not multi-anchor EWC.

The total loss is:

$$
L =
L_{DQN}
+
L_{EWC}
$$

with:

$$
L_{EWC}
=
\frac{\lambda}{2}
\sum_i
F_i^{acc}
(\theta_i-\theta_i^*)^2
$$

where:

- $\theta^*$: latest saved parameter anchor after a scene,
- $F_i^{acc}$: accumulated diagonal parameter-importance estimate,
- $\lambda$: EWC strength.

After each scene:

$$
F_i^{acc}
\leftarrow
\rho F_i^{acc}+F_i^{new}
$$

$$
\theta^*
\leftarrow
\theta^{*(k)}
$$

## Parameter importance estimate

Use squared gradients of the DQN loss:

$$
F_i^{new}
\approx
\mathbb{E}
\left[
\left(
\frac{\partial L_{DQN}}
{\partial \theta_i}
\right)^2
\right]
$$

Call this a:

> DQN-compatible diagonal EWC approximation.

Do not call it the exact KGCRL Fisher estimate.

## Training variants

Implement in this order:

1. `finetune`: Double DQN search only
2. `replay`: Double DQN search + selective replay
3. `ewc`: Double DQN search + online EWC
4. `replay_ewc`: Double DQN search + selective replay + online EWC

The final comparison should include at least `finetune` and `replay`. Add `ewc` and `replay_ewc` after the base system is stable.

## Deterministic homing is not part of the RL loss

The homing controller is useful for completing episodes and producing demos, but it is not optimized by the DQN objective.

Report homing metrics separately from RL search metrics. The main continual-learning score should be based on target reveal rate.
