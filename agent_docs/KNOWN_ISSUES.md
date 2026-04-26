# KNOWN_ISSUES.md

## Purpose

Track bugs, fragile assumptions, failed checks, and workarounds.

## Template

```md
### ISSUE-YYYYMMDD-N

Status: Open / Fixed / Workaround / Won't fix

Layer:

Affected files:

Description:

Expected behavior:

Actual behavior:

Steps to reproduce:

Workaround:

Resolution:
```

## Current known issues

### ISSUE-20260426-1

Status: Open

Layer: Documentation / repo organization

Affected files:

```text
procect_docs/
```

Description:

The project docs folder appears to be misspelled.

Expected behavior:

Use `project_docs/`.

Workaround:

Treat `procect_docs/` as active docs until renamed.

### ISSUE-20260426-2

Status: Open

Layer: Layer 0 / Layer 1 collision sensing

Affected files:

```text
src/controllers/**
src/worlds/test world.wbt
```

Description:

The current project plan uses a proximity-threshold collision detector based on `ps0`-`ps7`. This may prove noisy or may miss true contact events depending on robot pose and obstacle geometry.

Expected behavior:

Proximity readings should reliably trigger early-stop collision handling before sustained wall impact.

Actual behavior:

Layer 0 smoke-test verification showed early collision stopping working, but broader reliability across later scenes is not yet established.

Steps to reproduce:

Run the Layer 0 smoke-test controller in `src/worlds/test world.wbt` and observe whether collision events trigger consistently near obstacles.

Workaround:

Tune the threshold first. If the approach remains unreliable after manual verification, propose a dedicated bumper/contact-style sensor through explicit scope review before editing the world again.

### ISSUE-20260426-3

Status: Workaround

Layer: Tooling / local test workflow

Affected files:

```text
pytest.ini
agent_docs/RUNBOOK.md
agent_docs/TEST_PLAN.md
AGENTS.md
```

Description:

Pytest cache-provider writes can fail on this Windows setup when pytest attempts to create temporary cache directories under the repo root.

Expected behavior:

`pytest` should run without creating inaccessible temporary cache folders.

Actual behavior:

Plain `pytest` can emit cache warnings and create permission-blocked `pytest-cache-files-*` directories even though the repository itself is writable. If those folders remain, pytest may also try to collect them during discovery.

Steps to reproduce:

Run `pytest` without disabling the cache provider.

Workaround:

Use `pytest -p no:cacheprovider`, keep the same default in `pytest.ini`, and exclude `pytest-cache-files-*` plus `.pytest_cache` from test discovery.

Resolution:

Investigate and remove the local Windows temp/cache permission issue before re-enabling the cache provider.
