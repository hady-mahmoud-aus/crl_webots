# PROJECT_CONTRACTS.md

## Purpose

Contracts that prevent subtle bugs in observations, actions, rewards, metrics, and checkpoints.

Changing a contract requires updating this file, tests, and checkpoint/run metadata.

## Observation contract

Default observation version: `obs_v1`.

Default vector:

| Index | Feature | Notes |
|---:|---|---|
| 0-7 | proximity sensors `ps0` to `ps7` | normalized |
| 8 | `sin(theta)` | Compass-derived heading |
| 9 | `cos(theta)` | Compass-derived heading |
| 10 | `visited_front` | 0 or 1 |
| 11 | `visited_left` | 0 or 1 |
| 12 | `visited_right` | 0 or 1 |
| 13 | `visited_back` | 0 or 1 |
| 14 | `target_revealed` | 0 or 1 |
| 15 | `target_distance` | 0 before reveal |
| 16 | `sin(target_bearing)` | 0 before reveal |
| 17 | `cos(target_bearing)` | 0 before reveal |

Default observation dimension: `18`.

Before target reveal:

```text
target_revealed = 0
target_distance = 0
sin(target_bearing) = 0
cos(target_bearing) = 0
```

Rules:

- Do not change observation order without incrementing `obs_version`.
- Do not change observation dimension without updating tests, configs, and checkpoint metadata.
- Observation values must be finite.
- Unit tests must verify shape, no NaN/inf, and before/after reveal behavior.

## Action contract

Default action-set version: `three_action`.

Core action IDs are stable:

| ID | Action | Required |
|---:|---|---|
| 0 | `forward` | yes |
| 1 | `rotate_left` | yes |
| 2 | `rotate_right` | yes |

Optional extended action-set version: `five_action`.

| ID | Action | Required |
|---:|---|---|
| 0 | `forward` | yes |
| 1 | `rotate_left` | yes |
| 2 | `rotate_right` | yes |
| 3 | `forward_left` | optional |
| 4 | `forward_right` | optional |

Rules:

- Do not change IDs 0-2.
- Do not add diagonal actions unless `action_set=five_action` or a new explicit version is configured.
- Checkpoints must record `action_set_version` and action dimension.
- Tests must verify action IDs, wheel target signs, timeout behavior, and invalid action handling.
- Manual Webots verification is required after changing macro-actions.

## Reward contract

Search reward must be additive:

```text
r_search =
  + new_cell * r_new
  - revisit * r_revisit
  - collision * r_collision
  - dwell * r_dwell
```

Homing reward:

```text
r_home =
  alpha_home * (previous_distance - current_distance)
  - collision * r_collision
  + reached * r_goal
```

Reward-change safety gate:

Any reward change requires:

- unit tests for reward signs,
- component-level reward logging,
- one random-policy sanity run,
- review of reward component logs before training.

## Metric contract

Use stable metric names:

```text
success
target_revealed
target_reached
episode_return
decision_steps
controller_steps
coverage_count
coverage_ratio_offline
collision_count
dwell_count
loss_dqn
loss_ewc
loss_total
epsilon
forgetting
```

Do not rename metrics without updating logging, plotting, tests, and docs.

## Checkpoint compatibility contract

Checkpoints must include:

```text
obs_version
obs_dim
action_set_version
action_dim
model_state_dict
target_model_state_dict
optimizer_state_dict
config
scene_id
variant
seed
```

If observation or action dimensions change, old checkpoints are incompatible unless a migration is explicitly implemented.

Do not silently load incompatible checkpoints.
