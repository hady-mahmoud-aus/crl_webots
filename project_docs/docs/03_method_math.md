# 03 — Method and Math

## Method summary

The method is:

> Custom PyTorch Double DQN + selective episodic replay inspired by OPR + DQN-compatible online EWC approximation inspired by KGCRL.

This is an inspired-by adaptation, not an exact implementation of either paper.

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

The output dimension equals the number of discrete actions.

## Double DQN target for macro-actions

Each macro-action transition is:

$$
(s_t,a_t,R_t,s_{t+n},done,n)
$$

where $n$ is the number of Webots controller steps inside the macro-action.

The accumulated reward is:

$$
R_t=
\sum_{\ell=0}^{n-1}\gamma^\ell r_{t+\ell}
$$

The Double DQN target is:

$$
y=
\begin{cases}
R_t, & \text{if done}\\
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

## Current replay buffer

Store macro-action transitions:

```python
transition = {
    "state": state,
    "action": action,
    "reward_sum": reward_sum,
    "next_state": next_state,
    "done": done,
    "duration": duration,
    "info": info,
}
```

## Selective episodic replay

After each scene, store top-$K$ high-quality episodes.

Episode quality should prioritize:

1. success,
2. high coverage,
3. low collisions,
4. shorter time or higher return.

Example episode record:

```python
episode = {
    "scene_id": scene_id,
    "transitions": [...],
    "metrics": {
        "success": bool,
        "coverage_count": int,
        "coverage_ratio_offline": float,
        "collisions": int,
        "decision_steps": int,
        "return": float,
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

1. `finetune`: Double DQN only
2. `replay`: Double DQN + selective replay
3. `ewc`: Double DQN + online EWC
4. `replay_ewc`: Double DQN + selective replay + online EWC

The final comparison should include at least `finetune` and `replay`. Add `ewc` and `replay_ewc` after the base system is stable.
