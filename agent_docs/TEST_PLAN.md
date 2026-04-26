# TEST_PLAN.md

## Purpose

Pass/fail checks before claiming milestones.

## Testing principles

- Pure logic requires automated tests.
- Webots-facing features require manual Webots verification.
- Mock tests do not count as Webots verification.
- Do not expand RL complexity while current-layer tests are failing.

## Code quality checks

Run when code changes:

```powershell
black .
ruff check .
pytest -p no:cacheprovider
```

The repo-level `pytest.ini` also excludes `pytest-cache-files-*` and `.pytest_cache` from test discovery.

## Pure logic tests

Prioritize:

```text
tests/test_grid.py
tests/test_rewards.py
tests/test_observations.py
tests/test_actions.py
tests/test_replay_buffer.py
tests/test_selective_memory.py
tests/test_dqn_targets.py
tests/test_ewc.py
```

## Layer 0 checks

Pass if:

- required Webots devices are found,
- sensors return finite values,
- motors accept commands,
- wheel position sensors change,
- scripted forward/left/right actions work,
- collision threshold can be logged,
- smoke-test log is written,
- manual Webots verification passes.

## Layer 1 checks

Pass if:

- `reset()` and `step(action)` work,
- observation follows `PROJECT_CONTRACTS.md`,
- all core actions work,
- rewards have correct signs,
- random policy runs multiple episodes,
- metrics are saved,
- manual Webots verification passes.

## Reward-change safety gate

Any reward change requires:

- unit tests for reward signs,
- reward component logging,
- random-policy sanity run,
- inspection of reward component logs,
- status update in `IMPLEMENTATION_STATUS.md`.

## Observation/action contract checks

Any observation or action change requires:

- contract update,
- unit tests,
- config update,
- checkpoint metadata update,
- manual Webots verification if action execution changed.

## Layer 2+ checks

Pass if:

- replay batches have correct tensor shapes,
- Double DQN loss is finite,
- target updates run,
- checkpoints save/load,
- short training completes,
- evaluation logs are produced.

## Completion rule

A task is not complete unless the agent reports:

- files changed,
- tests run,
- manual Webots status if applicable,
- outputs/logs produced,
- limitations.

When outputs or evidence are saved for completion, they should be concise and contain only the necessary data needed to justify the result. If a larger raw artifact must be preserved, the completion record should reference it rather than duplicate it.
