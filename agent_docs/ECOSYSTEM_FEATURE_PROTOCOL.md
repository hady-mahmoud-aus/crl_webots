# ECOSYSTEM_FEATURE_PROTOCOL.md

## Purpose

How agents should add, modify, or remove durable agent ecosystem features.

An ecosystem feature is a rule that changes how agents work in this repository.

Examples:

- testing gates,
- manual Webots verification,
- dependency policy,
- file ownership,
- logging requirements,
- coding conventions,
- experiment integrity.

## Location convention

`AGENTS.md` stays at repository root.

All other ecosystem files live in `agent_docs/`.

When updating supporting files from this protocol, use paths such as:

```text
agent_docs/MEMORY.md
agent_docs/TEST_PLAN.md
```


## Core rule

Do not place a durable rule in only one file.

At minimum, update:

1. `AGENTS.md`
2. `MEMORY.md`
3. `README_AGENT_FILES.md`

Then update specialized files.

## Routing

| Feature type | Also update |
|---|---|
| Code style | `CODE_STYLE.md` |
| Testing gate | `TEST_PLAN.md`, `IMPLEMENTATION_STATUS.md` |
| Webots manual verification | `MANUAL_WEBOTS_VERIFICATION.md`, `RUNBOOK.md` |
| Repo/file ownership | `REPO_MAP.md` |
| Commands/workflow | `RUNBOOK.md`, `TODO.md` |
| Dependencies | `CODE_STYLE.md`, `RUNBOOK.md` |
| Experiments/logging/reproducibility | `EXPERIMENT_PROTOCOL.md`, `PROJECT_CONTRACTS.md` if metrics/contracts change |
| Observation/action/reward/metrics | `PROJECT_CONTRACTS.md`, `TEST_PLAN.md` |
| Known risks | `KNOWN_ISSUES.md` |
| Paper claims | `PAPER_NOTES.md` |

## Process

1. Identify the feature category.
2. Add high-level rule to `AGENTS.md`.
3. Add durable decision to `MEMORY.md`.
4. Update specialized files.
5. Add status/checklist items if needed.
6. Add TODOs if follow-up work is needed.
7. Update `README_AGENT_FILES.md` if a file is added/removed.
8. Summarize changed files and why.

## Do not

- hide durable rules in `TODO.md` only,
- weaken safety/file-ownership rules without user approval,
- add dependencies without approval,
- create new files without indexing them.
