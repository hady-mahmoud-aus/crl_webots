# Agent Ecosystem Files

Copy `AGENTS.md` into the repository root and copy all other files into `agent_docs/`.

Recommended root:

```text
C:\dev\AI Project\CRL
```

## Layout

```text
CRL/
  AGENTS.md
  agent_docs/
    README_AGENT_FILES.md
    MEMORY.md
    REPO_MAP.md
    CODE_STYLE.md
    PROJECT_CONTRACTS.md
    EXPERIMENT_PROTOCOL.md
    RUNBOOK.md
    TEST_PLAN.md
    MANUAL_WEBOTS_VERIFICATION.md
    IMPLEMENTATION_STATUS.md
    TODO.md
    KNOWN_ISSUES.md
    PAPER_NOTES.md
    ECOSYSTEM_FEATURE_PROTOCOL.md
```

## Files

| File | Purpose |
|---|---|
| `AGENTS.md` | Main operating instructions for agentic coding assistants |
| `MEMORY.md` | Durable project facts and decisions |
| `REPO_MAP.md` | Repo layout, editable areas, and path rules |
| `CODE_STYLE.md` | Modular/functional code style and tooling |
| `PROJECT_CONTRACTS.md` | Observation, action, reward, metric, and checkpoint contracts |
| `EXPERIMENT_PROTOCOL.md` | Config, logging, reproducibility, and experiment integrity |
| `RUNBOOK.md` | Practical commands, workflows, debugging ladder, and handoff format |
| `TEST_PLAN.md` | Automated and manual verification requirements |
| `MANUAL_WEBOTS_VERIFICATION.md` | Manual Webots verification rules and checklists |
| `IMPLEMENTATION_STATUS.md` | Layer-by-layer progress tracker |
| `TODO.md` | Concrete task list |
| `KNOWN_ISSUES.md` | Bugs, fragile assumptions, and workarounds |
| `PAPER_NOTES.md` | Safe implementation-relevant paper claims |
| `ECOSYSTEM_FEATURE_PROTOCOL.md` | How agents should add future ecosystem features |

## First instruction for any agent

Read root-level `AGENTS.md` first. It points to the supporting files in `agent_docs/`.

The root `AGENTS.md` also carries durable cleanup policy for removing transient stage-completion artifacts without deleting evidence or experiment outputs.

The root `AGENTS.md` also requires stage-completion evidence to be stored in a concise, highly condensed form unless raw artifacts must be preserved for reproducibility.

The root `AGENTS.md` also allows conservative post-stage structural cleanup inside `src/`, including needed renames or moves, while preserving valid Webots controller/world wiring.
