# Change Summary — Deterministic Homing Simplification

## Core change

The project has been changed from dual RL search-and-homing to:

> RL for target-revealing search + deterministic post-reveal homing.

## User decisions applied

- RL policy stops acting once the target is revealed.
- The Webots episode waits for homing to complete before final episode completion.
- RL reward is for target reveal, not target reaching.
- Main success definition is target reveal.
- Main evaluation metric is target reveal rate.
- Homing uses a simple deterministic controller: turn toward target, move forward, repeat.
- Homing collision behavior uses simple recovery instead of RL penalty.
- Report framing explicitly describes the continual RL problem as search/exploration, with homing handled by a fixed controller.

## Files updated

- `README.md`
- `00_project_scope_and_decisions.md`
- `01_task_formulation.md`
- `02_webots_environment_interface.md`
- `03_method_math.md`
- `04_implementation_layers.md`
- `05_training_and_evaluation.md`
- `06_paper_alignment.md`

## Important implementation implication

DQN replay should contain search-phase transitions only. Once target reveal occurs, the transition is terminal for RL training. Deterministic homing may still run to complete the Webots episode and produce auxiliary metrics, but homing controller steps should not be inserted into the replay buffer.
