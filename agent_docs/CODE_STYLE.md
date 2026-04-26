# CODE_STYLE.md

## Priority

> Modular, functional, efficient, readable code.

## Architecture style

Use functional core / imperative shell.

Pure functions should own:

- grid-cell assignment,
- heading-aligned neighbor lookup,
- reward calculation,
- target reveal checks,
- action-to-wheel-target conversion,
- observation vector construction,
- Double DQN target calculation,
- episode ranking,
- metric aggregation.

Stateful shell code should own:

- Webots sensor reads,
- Webots motor commands,
- Webots stepping,
- file I/O,
- training orchestration,
- checkpointing.

Do not mix Webots API calls with DQN loss, replay logic, reward math, plotting, or experiment analysis.

## Config style

Use YAML config files externally.

Load YAML into Python dataclasses internally.

Avoid passing nested dictionaries throughout the code.

## Type hints

Require type hints on:

- public functions,
- public classes,
- dataclasses,
- module-boundary functions,
- functions used across files.

Internal short helpers can be flexible.

## Modules

Use medium-small modules with clear ownership.

Refactor when a file mixes unrelated responsibilities, not merely because of length.

## Dependencies

Allowed baseline dependencies:

```text
torch
numpy
pandas
matplotlib
pyyaml
pytest
black
ruff
```

Do not add other dependencies without user approval.

If requesting a dependency, explain:

- why it is needed,
- simpler alternative,
- Windows/Webots impact,
- exact install command.

## Comments

Use minimal comments for normal Python.

Document Webots-specific assumptions inline:

- device names,
- motor position-control behavior,
- controller step vs decision step,
- GPS bookkeeping,
- collision thresholds,
- macro-action timeout behavior,
- world/controller path assumptions.

## Efficiency

Prioritize clarity first.

DQN updates must use batched tensor operations:

- sample replay batches,
- convert batches to tensors,
- compute Q-values in batch,
- compute Double DQN targets in batch,
- perform one optimizer step per batch.

Avoid one gradient update per transition.

## Formatting

Use:

```powershell
black .
ruff check .
```

Do not do large formatting-only rewrites unless asked.

## Error handling

Fail loudly for invalid assumptions.

Do not silently ignore:

- missing Webots devices,
- invalid sensor values,
- NaN observations,
- NaN rewards,
- invalid actions,
- failed checkpoint saves,
- missing config keys.
